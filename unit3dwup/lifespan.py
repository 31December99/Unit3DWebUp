# -*- coding: utf-8 -*-
import asyncio
import os

from contextlib import asynccontextmanager
from pathlib import Path

from unit3dwup.config import get_settings
from unit3dwup.config import get_logger

from unit3dwup.repositories.job_repos import JobRedisRepo

from unit3dwup.services.lifespan_service import update_mounted_paths, checking_env_file

from unit3dwup.external.websocket import WebSocketManager

from fastapi import FastAPI

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RedisEventHandler(FileSystemEventHandler):
    """
        Watch only a specific folder
        This event is shared by app.state FastApi
        it uses a queue 'redis_event'
     """

    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        self.app.state.redis_events.put_nowait({
            "type": "created",
            "path": event.src_path,
        })

    def on_deleted(self, event):
        self.app.state.redis_events.put_nowait({
            "type": "deleted",
            "path": event.src_path,
        })


async def redis_event_consumer(app: FastAPI):
    """
    :param app: it is mr FastApi
    :return: None

    It is a consumer. Wait for any news from the queue and extract the new path created or deleted
    """

    # > The queue :|
    queue = app.state.redis_events

    # Logger
    logger = get_logger("settings_logger")

    while True:
        event = await queue.get()
        try:
            app.state.folder_event = event
            relative = Path(app.state.folder_event['path']).relative_to(Path(app.state.watcher_path))
            new_path = Path(app.state.settings.prefs.WATCHER_PATH) / relative.parts[0]

            # Send logs to the client
            await app.state.ws_manager.broadcast({
                "type": "log",
                "level": "info",
                "message": f"{app.state.folder_event['type']} {new_path}",
            })
        except Exception as e:
            logger.debug("Consumer Folder error", e)
        finally:
            queue.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan initialize DB and app configuration
    We need to shared state
    https://fastapi.tiangolo.com/advanced/events/

    :param app: FastAPI
    :return: None
    """
    # Load the configuration file
    settings = get_settings()
    app.state.settings = settings

    # Check configuration file
    await checking_env_file(app=app)

    # Create a new state for the watcher queue
    app.state.redis_events = asyncio.Queue()

    # Environment variabile in the container backend
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))

    # Build redis url
    REDIS_URL = f"redis://{redis_host}:{redis_port}"

    # Connect to redis
    job = JobRedisRepo(url=REDIS_URL)
    await job.connect(app=app)

    # Store the job reference to app.state
    app.state.job = job

    # RestartDocker notify
    # Set flag to true when setEnv is called from the frontend
    app.state.restart_docker = False

    # Create a new profile from user_preferences Job_id is '0'
    # Later will be recalled from the setting endpoint
    await job.create_profile(dict(settings.prefs))

    # The WebSocket. Send to client progress bar value( Torrent creation) and short log message
    app.state.ws_manager = WebSocketManager()

    # Update mounted paths string
    await update_mounted_paths(app=app)

    # Watcher zone
    # Shared event
    app.state.folder_event = None

    # back to watcher
    observer = Observer()

    # Callback
    handler = RedisEventHandler(app)

    # Start to watch
    observer.schedule(handler, app.state.watcher_path, recursive=True)
    if app.state.settings.prefs.WATCHER_DESTINATION_PATH != os.getcwd():
        observer.start()

    # Create a consumer that works in the background
    consumer_task = asyncio.create_task(redis_event_consumer(app))

    # Goes..
    yield

    # Come back to clean and close
    if app.state.settings.prefs.WATCHER_DESTINATION_PATH != os.getcwd():
        observer.stop()
        observer.join()

    consumer_task.cancel()
    await job.close()
