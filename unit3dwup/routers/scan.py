# -*- coding: utf-8 -*-
import hashlib
import inspect
import json
import time

import aiohttp

from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import JSONResponse

from unit3dwup.config import get_logger, Settings
from unit3dwup.config.limiter import limiter

from unit3dwup.repositories.db_online import Tmdb, Tvdb

from unit3dwup.services.media_service import MediaService, MediaService2
from unit3dwup.services.auto_async_service import AsyncMediaManager

from unit3dwup.use_case.scan_media_usecase import ScanMediaUseCase
from unit3dwup.schemas import ScanRequest
from unit3dwup.external.websocket import WebSocketManager
from unit3dwup.external.auth import get_current_user

from unit3dwup.routers.dependencies import (
    load_settings,
    get_job_repo,
    get_ws_manager,
)

router = APIRouter()

from typing import Annotated



@router.post("/scan")
@limiter.limit("5/minute")
async def scan(payload: ScanRequest, request: Request,
               # 05/07/2026 - creare una pagina di login prima di andare avanti
               user: Annotated[str, Depends(get_current_user)],
               settings: Settings = Depends(load_settings),
               job_repo=Depends(get_job_repo),
               ws_manager: WebSocketManager = Depends(get_ws_manager),

               ) -> JSONResponse:
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

    app = request.app

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
    job_list_id = hashlib.sha256(settings.prefs.SCAN_PATH.encode()).hexdigest()
    logger.info(f"Current joblist_id {job_list_id} {settings.prefs.SCAN_PATH}")

    # Load the jobs list using the previous id
    job_list = await job_repo.get_job_list(job_id=job_list_id)

    # Load Media for each job id from the job_list
    job_list_results = []
    for job_id in job_list:
        job = await job_repo.get_job(job_id)
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
        await ws_manager.broadcast({
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
            await job_repo.create_job_list(
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
