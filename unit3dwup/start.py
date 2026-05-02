# -*- coding: utf-8 -*-
import asyncio
import hashlib
import inspect
import json
import os
import time

from contextlib import asynccontextmanager
from pathlib import Path

from unit3dwup.config import get_settings
from unit3dwup.config import MediaStatus
from unit3dwup.config import get_logger

from unit3dwup.repositories.job_repos import JobRedisRepo
from unit3dwup.repositories.db_online import Tmdb, Tvdb

from unit3dwup.services.media_service import MediaService, MediaService2
from unit3dwup.services.itt_tracker_service import ITTtrackerService
from unit3dwup.services.auto_async_service import AsyncMediaManager
from unit3dwup.services.interfaces import TrackerServiceInterface
from unit3dwup.services.lifespan_service import update_mounted_paths, checking_env_file

from unit3dwup.use_case.scan_media_usecase import ScanMediaUseCase
from unit3dwup.use_case.process_all_usecase import ProcessAllUseCase
from unit3dwup.use_case.upload_usecase import UploadUseCase
from unit3dwup.use_case.seed_usecase import SeedUseCase
from unit3dwup.use_case.make_torrent_usecase import MakeTorrentUseCase

from unit3dwup.external.websocket import WebSocketManager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import WebSocket
from fastapi import FastAPI
from fastapi import status
from pydantic import BaseModel, Field
from dotenv import load_dotenv, dotenv_values

import aiohttp
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


async def update_poster(msg: str, job_id: str, field_id: str, new_id: str):
    # Fix the DB ID with the received one
    await app.state.job.update_job(job_id=job_id, new_data={field_id: new_id})

    # Update the Media status
    await app.state.job.update_job(job_id=job_id, new_data={'status': str(MediaStatus.DB_IDENTIFIED)})

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Console message
    logger.info(f"-> Update {msg} JOB_ID: {job_id}\n")

    # Send log to the client
    await app.state.ws_manager.broadcast({
        "type": "log",
        "level": "success",
        "message": f"Update {msg} JOB_ID {job_id}",
    })


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


# Initialize FastApi
app = FastAPI(lifespan=lifespan)

# TODO middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:PORT"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    path: str = Field(..., description="Filesystem path to scan")


class ProcessAllRequest(BaseModel):
    job_list_id: str = Field(..., description="ID of the job list")


class JobRequest(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")


class UpdatePosterRequest(BaseModel):
    job_id: str
    field_id: str
    new_id: str


class ClearJobListRequest(BaseModel):
    job_list_id: str


class SetEnvRequest(BaseModel):
    key: str
    value: str


class FilterRequest(BaseModel):
    title: str


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """
    :param ws: websocket connection.Currently used to report the progress of the process (%)
    URL:
        ws://host:8000/ws

    Purpose:
        Push notifications from backend to frontend.

    Events sent by server:
        {
            "type": "log",
            "level": "success | error | warn | info",
            "message": "text"
        }

        {
            "type": "progress",
            "job_id": "abc123",
            "value": 45
        }

    """

    manager = app.state.ws_manager
    await manager.connect(ws)

    try:
        while True:
            # TODO for the moment websocket tx only
            await ws.receive_text()  # waiting for new message
    except:
        pass
    finally:
        await manager.disconnect(ws)


@app.post("/cjoblist")
async def clear_job_list_id(payload: ClearJobListRequest):
    """
        This endpoint deletes a job list and all related posters

        Required:
        - job_list_id: identifier of the job list

        Returns:
        - status: operation result
        """

    # Load the job list
    # Carica la joblist per ottenere il percorso e inviarlo a log. Mi sembra troppo per una stampa
    job_list = await app.state.job.get_job_list(job_id=payload.job_list_id)
    results = [json.loads(await app.state.job.get_job(job_id)) for job_id in job_list]

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Delete the job list
    # TODO: delete all job ids
    await app.state.job.delete_job_list(job_id=payload.job_list_id)

    if results:
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "success",
            "message": f"Clear JobList {payload.job_list_id} {results[0]['folder']}",
        })
        logger.info(f"-> Clear JobList ID° {payload.job_list_id} {results[0]['folder']}\n")
    else:
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "error",
            "message": f"Clear JobList : JobList id not found",
        })
        logger.info(f"-> Clear JobList : JobList ID non trovato\n")


@app.post("/scan")
async def scan(payload: ScanRequest) -> JSONResponse:
    """
    This endpoint scans the local files and creates a Media object for each associating it with its description

    Required
    - path: user path for the scan process, filesystem path on the hdd

    Prerequisite
    - path must be valid and accessible

    Http response
    - status: http status code
    - source: indicates source of the posters local hdd or remote tracker
    - results: dictionary containing source and list of Media objects

    Websocket events
    - type: log type for frontend display
    - level: result of the process success or error
    - message: message displayed in the frontend console
    """

    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    if app.state.restart_docker:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "source": "local",
                "message": "Please restart the Docker container",
            }
        )

    start_time = time.perf_counter()

    # Get the id for the current path
    job_list_id = hashlib.sha256(app.state.settings.prefs.SCAN_PATH.encode()).hexdigest()
    logger.info(f"Current joblist_id {job_list_id} {app.state.settings.prefs.SCAN_PATH}")

    # Load the jobs list using the previous id
    job_list = await app.state.job.get_job_list(job_id=job_list_id)

    # Load the jobs list using the previous id
    job_list = await app.state.job.get_job_list(job_id=job_list_id)

    # Load Media for each job id from the job_list
    job_list_results = []
    for job_id in job_list:
        job = await app.state.job.get_job(job_id)
        if job:
            job_list_results.append(json.loads(job))

    # New session
    async with aiohttp.ClientSession() as session:

        manager = AsyncMediaManager(
            path=app.state.scan_path,
            app=app,
            job_id_list=job_list_id
        )

        # Instance repo ( or gateway..?) for each db online (TVDB, TMDB). Read imdb id from the tvdb remote_ids list
        tvdb_repo = Tvdb(session=session)
        tmdb_repo = Tmdb(session=session)

        # Pass the repository to the MediaService class for async task purposes
        media_service = MediaService(tmdb_repo)
        media_service2 = MediaService2(tvdb_repo)

        # Create a use_case
        use_case = ScanMediaUseCase(
            manager=manager,
            media_service=media_service,
            media_service2=media_service2,
            job_repo=app.state.job,
            session=session,
            job_list=job_list
        )

        # Run all
        results = await use_case.execute()

        # Send a message to the frontend by ws
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "success",
            "message": f"Scan completato in {time.perf_counter() - start_time:.2f} secondi",
        })

        # Analyze the results and build a new job_list with the new and old posters
        build_results = []
        new_job_list = []

        for media in results:
            # The current media object has no description because the job_id is already in the job_list
            if not media.description:
                for job in job_list_results:
                    if job['job_id'] == media.job_id:
                        build_results.append(job)
                        # append the old poster
                        new_job_list.append(job['job_id'])
            else:
                # new description. This is a new job_id
                build_results.append(media.to_dict())
                new_job_list.append(media.job_id)

        if new_job_list:
            # Save the new job_list
            await app.state.job.create_job_list(
                job_id=job_list_id,
                job_list=new_job_list
            )

        # return to frontend the new posters
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "source": "local",
                "results": build_results,
            }
        )


@app.post("/processall")
async def process_all(payload: ProcessAllRequest):
    """
    Start a chain load the joblist filter for existing torrent create torrent upload the complete joblist

    Required
    - job_list_id identifies the list created by the scan endpoint

    Prerequisite
    - valid description status media class attribute

    Return
    - none
    """

    use_case = ProcessAllUseCase(app=app, job_list_id=payload.job_list_id,
                                 torrent_client_name=app.state.settings.torrent.TORRENT_CLIENT)
    await use_case.execute()


@app.post("/maketorrent")
async def make(payload: JobRequest):
    """
    Create one or more torrent files

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """
    torrent_service = MakeTorrentUseCase(app=app, job_id=payload.job_id)
    await torrent_service.execute()


@app.post("/upload")
async def upload(payload: JobRequest):
    """
    Upload a single torrent file

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none

    WebSocket events emitted
    - posterLogMessage: sent for each uploaded torrent
    - job_id: media identifier
    - message: upload result message
    """

    upload_service = UploadUseCase(app=app, job_id=payload.job_id)
    await upload_service.execute()


@app.post("/seed")
async def seed(payload: JobRequest) -> JSONResponse:
    """
    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    use_case = SeedUseCase(app=app, client=app.state.settings.torrent.TORRENT_CLIENT, job_id=payload.job_id)
    return await use_case.execute()


@app.post("/settmdbid")
async def set_poster_id(payload: UpdatePosterRequest):
    """
    Set a Tmdb id for example when tmdb returns an empty result

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(msg="TMDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/settvdbid")
async def set_tvdb_id(payload: UpdatePosterRequest):
    """
    Set a TVdb id for example when tvdb returns an empty result

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(msg="TVDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/setimdbid")
async def set_imdb_id(payload: UpdatePosterRequest):
    """
    Set an Imdb id for example when the remote list of tvdb is empty

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(msg="IMDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/setposterurl")
async def set_poster_url(payload: UpdatePosterRequest):
    """
    Set a poster url for example when tmdb returns an empty result only for frontend

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(msg="TMDB Poster Url", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/setposterdname")
async def set_poster_dname(payload: UpdatePosterRequest):
    """
    Set a poster display name for example if you dont like it
    Display name is the name shown on the dedicated torrent page

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(msg="Update DisplayName", job_id=payload.job_id, field_id=payload.field_id,
                        new_id=payload.new_id)


@app.post("/setting")
async def configuration():
    """
    Load setting from the local configuration file

    Required
    - job_id is fixed to zero

    Return
    - none
    """

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Load json settings and return it to the client
    job_data = await app.state.job.get_job(job_id='0')

    # /// Check main paths
    if app.state.settings.prefs.SCAN_PATH == os.getcwd():
        logger.warning("SCAN PATHS NO SET")
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "warn",
            "message": f"{frame.f_code.co_name} Scan Path not set",
        })
    if app.state.settings.prefs.TORRENT_ARCHIVE_PATH == os.getcwd():
        logger.warning("TORRENT ARCHIVE PATH NOT SET")
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "warn",
            "message": f"{frame.f_code.co_name} Torrent archive path not set",
        })
    if os.getcwd() in [app.state.settings.prefs.WATCHER_DESTINATION_PATH, app.state.settings.prefs.WATCHER_PATH]:
        logger.warning("WATCHER PATHS NO SET")
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "warn",
            "message": f"{frame.f_code.co_name} Watcher Paths not set",
        })

    # Get data
    user_prefs = json.loads(job_data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"userPreferences": user_prefs}
    )


@app.post("/setenv")
async def set_env(payload: SetEnvRequest):
    """
    Set the environment variables from the frontend
    User need to restart the docker

    Required
    - Key: dictionary key
    - Value: new value for the environment variable

    Return
    - none
    """

    # Load env file
    load_dotenv(dotenv_path=app.state.env_file, override=True)

    # Edit file env
    # Replace set_key in python dotenv
    # Permission denied when tries to create a temporary file but it fails because the container is not running as root
    # set_key(str(app.state.env_file), payload.key, payload.value)

    # Current variabiles value
    env_vars = dotenv_values(str(app.state.env_file))
    # update the key
    env_vars[payload.key] = payload.value
    # Rewrite file env
    with open(str(app.state.env_file), "w", encoding="utf-8") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

    # Refresh memory
    os.environ[payload.key] = payload.value

    # Clear cache and reload
    get_settings.cache_clear()

    # Refresh the lru cache
    settings = get_settings()

    # Update the fast api app state
    app.state.settings = settings

    # This key requires a Docker restart
    if payload.key.upper() in ["PREFS__WATCHER_DESTINATION_PATH", "PREFS__WATCHER_PATH", "PREFS__TORRENT_ARCHIVE_PATH",
                               "PREFS__SCAN_PATH"] and os.getenv("DOCKER") == "true":
        app.state.restart_docker = True

    # Update mounted path strings. Changes paths require restarting docker when DOCKER == 1
    await update_mounted_paths(app=app)

    # Ricreate profile (overwrite -> it uses hset command)
    await app.state.job.create_profile(dict(settings.prefs))

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Console message
    logger.info(f"-> Update {payload.key} value -> {payload.value}\n")

    # Send log to the client
    await app.state.ws_manager.broadcast({
        "type": "log",
        "level": "success",
        "message": f"-> Update {payload.key} value -> {payload.value}\n",
    })

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "source": "local",
            "docker": os.getenv("DOCKER"),
            "message": f"Saved {payload.key}",
        }
    )


@app.post("/filter")
async def filter_search(payload: FilterRequest):
    """
    Search words or title in the tracker

    Required
    - title: title or part of it

    Return
    - none
    """

    # Search for a title in the tracker
    async with aiohttp.ClientSession() as session:
        # A new ITT tracker instance with interface
        tracker_service: TrackerServiceInterface = ITTtrackerService(session, app=app)

        # Search
        data = await tracker_service.search(payload.title)

        # Return the source as remote ( change the bottom line color on the poster)
        # job_id not applicable
        # Extract attributes field for each data found
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "source": "remote",
                "job_id": '-1',
                "results": [c['attributes'] for c in data['data']],
            }
        )


def main():
    print("Run -> uvicorn unit3dwup.start:app")

if __name__ == "__main__":
    main()
