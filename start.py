# -*- coding: utf-8 -*-
# 07/02/2026
import asyncio
import hashlib
import json
import os
import time

from contextlib import asynccontextmanager
from pathlib import Path

from config.settings import Load, DEFAULT_JSON_PATH
from config.constants import MediaStatus
from config import logger
from repositories.job_repos import JobRedisRepo
from repositories.db_online import Tmdb, Tvdb

from services.interfaces import TrackerServiceInterface, TorrentClientServiceInterface
from services.torrent_client_service import QbittorrentClientService
from services.media_service import MediaService, MediaService2
from services.itt_tracker_service import ITTtrackerService
from services.auto_async_service import AsyncMediaManager
from services.torrent_service import TorrentService

from use_case.scan_media_usecase import ScanMediaUseCase
from use_case.seed_usecase import SeedUseCase
from use_case.upload_usecase import UploadUseCase

from external.websocket import WebSocketManager
from models.media import Media

from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import status
import aiohttp
import uvicorn

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

REDIS_URL = "redis://localhost:6379"


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

    while True:
        event = await queue.get()
        try:
            app.state.folder_event = event
            # TODO:
            # For the moment the watcher folder is hardcoded
            relative = Path(app.state.folder_event['path']).relative_to(Path("/home/parzival/ts watcher"))
            new_path = os.path.join("/home/parzival/ts watcher", relative.parts[0])

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
    app.state.config = Load().load_config()

    # Create a new state for the watcher queue
    app.state.redis_events = asyncio.Queue()

    # Connect to redis
    job = JobRedisRepo(url=REDIS_URL)
    await job.connect(app=app)

    # Store the job reference to app.state
    app.state.job = job

    # Create a new profile from user_preferences Job_id is '0'
    # Later will be recalled from the setting endpoint
    await job.create_profile(dict(config.user_preferences))

    # The WebSocket. Send to client progress bar value( Torrent creation) and short log message
    app.state.ws_manager = WebSocketManager()

    # Watcher zone
    # Shared event
    app.state.folder_event = None
    # back to watcher
    observer = Observer()
    # Callback
    handler = RedisEventHandler(app)
    # Start to watch
    # TODO:
    # For the moment the watcher folder is hardcoded
    observer.schedule(handler, "/home/parzival/ts watcher", recursive=True)
    observer.start()

    # Create a consumer that works in the background
    consumer_task = asyncio.create_task(redis_event_consumer(app))

    # Goes..
    yield

    # Come back to clean and close
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


class HttpRequest(BaseModel):
    """
       Represents the payload of a request for uploading or processing jobs.

       Attributes:
           title (str | None): Used to search title in the tracker
           path (str | None): the user path for the scan endpoint
           job_id (str | None): Identifier for a single job. Corresponds to Media.job_id (Poster)
                                Received from the frontend
           field_id (str | None): Identifier for a specific field related to the job
           new_id (str | None): Optional new identifier for updates
           job_list_id (str | None): Identifier for a list of jobs received from the frontend
       """

    title: str | None = None
    path: str | None = None
    job_id: str | None = None
    field_id: str | None = None
    new_id: str | None = None
    job_list_id: str | None = None


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """
    :param ws: websocket connection.Currently used to report the progress of the process (%)
    :return: None
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
async def clear_job_list_id(payload: HttpRequest):
    """
    :param payload: Job_list id
    :return: None
     Client request to delete a job_list ( the home page where the poster are displayed )
    """
    # Load the job list
    # Carica la joblist per ottenere il percorso e inviarlo a log. Mi sembra troppo per una stampa
    job_list = await app.state.job.get_job_list(job_id=payload.job_list_id)
    results = [json.loads(await app.state.job.get_job(job_id)) for job_id in job_list]

    # Delete the job List
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
async def scan(payload: HttpRequest) -> JSONResponse:
    """
    # This endpoint scans the local files and creates a Media object for each associating it with its descriptione
    :param payload: HttpRequest payload
        - path: User path for the scan process. The path on the hdd

    :prerequisite: path

    :return http:
            - status: the http status code
            - source: Set a flag for the source of the poster Local(hdd) or remote(Tracker)
            - results: Dict that contains source and a list of Media objects (poster)

    :return websocket:
            - type: a type of log for the frontend. Color changes based on the type
            - level: result of the process ( success, error ecc)
            - message: what the frontend should write in the console window
    """

    start_time = time.perf_counter()

    # Get the id for the current path
    job_list_id = hashlib.sha256(payload.path.encode()).hexdigest()

    # Load the jobs list using the previous id
    job_list = await app.state.job.get_job_list(job_id=job_list_id)

    # Load Media for each job id from the job_list
    job_list_results = [
        json.loads(await app.state.job.get_job(job_id))
        for job_id in job_list
    ]

    # New session
    async with aiohttp.ClientSession() as session:

        manager = AsyncMediaManager(
            path=payload.path,
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
async def process_all(payload: HttpRequest):
    """
    Start a 'chain' : Load the joblist , Filter for existing torrent, create torrent, upload the complete joblist

    :param payload: HttpRequest payload
        - job_id: Identifies each poster. Corresponds to Media.job_id
        - job_list_id: Identifies the list created by the scan endpoint

    :prerequisite: a valid Description status ( Media Class attribute)
    :return: none
    """

    start_time = time.perf_counter()
    # Load a list of jobs from the cache based on the job_list_id received from the frontend
    job_list = await app.state.job.get_job_list(job_id=payload.job_list_id)

    # Load each poster contained in the job list
    results = [json.loads(await app.state.job.get_job(job_id)) for job_id in job_list]
    media_list = [
        Media.from_dict(item)
        for item in results
    ]

    # TORRENT : Create one or more torrent file based on media_list list
    torrent_service = TorrentService(media_list=media_list, app=app)
    await torrent_service.start()
    end_time = time.perf_counter()
    logger.debug(f"Terminato in {end_time - start_time:.2f} secondi\n")

    # UPLOAD: Upload one or more torrent file based on media_list list
    upload_service = UploadUseCase(media_list=media_list, app=app)
    await upload_service.execute()

    # SEED: seed one or more torrent file based on media_list list
    use_case = SeedUseCase(app=app, media_list=media_list, client=config.torrent_client_config.TORRENT_CLIENT)
    await use_case.execute()


@app.post("/maketorrent")
async def make(payload: HttpRequest):
    results = [json.loads(await app.state.job.get_job(payload.job_id))]
    media_list = [
        Media.from_dict(item)
        for item in results
    ]

    torrent_service = TorrentService(media_list=media_list, app=app)
    await torrent_service.start()


@app.post("/upload")
async def upload(payload: HttpRequest):
    """
     Upload a single torrent file

    :param payload: - job_id: Identifies each poster. Corresponds to Media.job_id -
    :return: none
    """

    # Upload the single poster
    upload_service = UploadUseCase(app=app, job_id=payload.job_id)
    await upload_service.execute()


@app.post("/seed")
async def seed(payload: HttpRequest):
    """
    :param payload:  - job_id: Identifies each poster. Corresponds to Media.job_id
    :return:
    """
    use_case = SeedUseCase(app=app, client=config.torrent_client_config.TORRENT_CLIENT, job_id=payload.job_id)
    await use_case.execute()


@app.post("/setting")
async def configuration(payload: HttpRequest):
    # Load json settings and return it to the client
    job_data = await app.state.job.get_job(job_id='0')

    # Get data
    user_prefs = json.loads(job_data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"userPreferences": user_prefs}
    )


@app.post("/settmdbid")
async def set_poster_id(payload: HttpRequest):
    # Update TMDB ID
    await update_poster(msg="TMDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/settvdbid")
async def set_tvdb_id(payload: HttpRequest):
    # Update TVDB ID
    await update_poster(msg="TVDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/setimdbid")
async def set_imdb_id(payload: HttpRequest):
    # Update IMDB ID
    await update_poster(msg="IMDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/setposterurl")
async def set_poster_url(payload: HttpRequest):
    # Update TMDB Poster url
    await update_poster(msg="TMDB Poster Url", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@app.post("/setposterdname")
async def set_poster_dname(payload: HttpRequest):
    # Update TMDB Poster url
    await update_poster(msg="Update DisplayName", job_id=payload.job_id, field_id=payload.field_id,
                        new_id=payload.new_id)


@app.post("/filter")
async def filter_search(payload: HttpRequest):
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


config = Load().load_config()


def main():
    logger.info("\nChecking Unit3D configuration file..\n")
    logger.info(f"Configuration       -> '{DEFAULT_JSON_PATH}'")
    logger.info(f"torrent Archive     -> '{config.user_preferences.TORRENT_ARCHIVE_PATH}'")
    logger.info(f"Images,Tmdb cache   -> '{config.user_preferences.CACHE_PATH}'")
    logger.info(f"Watcher Path        -> '{config.user_preferences.WATCHER_PATH}'")
    logger.info(f"Watcher Dest. Path  -> '{config.user_preferences.WATCHER_DESTINATION_PATH}'\n")

    uvicorn.run("start:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
