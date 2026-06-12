# -*- coding: utf-8 -*-
import inspect
import json
import os

from fastapi import APIRouter, Request, status,  Depends
from fastapi.responses import JSONResponse

from dotenv import load_dotenv, dotenv_values

from unit3dwup.config import get_settings
from unit3dwup.config import get_logger, Settings

from unit3dwup.services.lifespan_service import update_mounted_paths

from unit3dwup.schemas import SetEnvRequest


from unit3dwup.external.websocket import WebSocketManager
from unit3dwup.routers.dependencies import (
    load_settings,
    get_job_repo,
    get_ws_manager,
)

router = APIRouter()

@router.post("/setting")
async def configuration(request: Request,
                        settings: Settings = Depends(load_settings),
                        job_repo=Depends(get_job_repo),
                        ws_manager: WebSocketManager = Depends(get_ws_manager),
                        ):
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
    job_data = await job_repo.get_job(job_id='0')


    # /// Check main paths
    if settings.prefs.SCAN_PATH == os.getcwd():
        logger.warning("SCAN PATHS NO SET")
        await ws_manager.broadcast({
            "type": "log",
            "level": "warn",
            "message": f"{frame.f_code.co_name} Scan Path not set",
        })
    if settings.prefs.TORRENT_ARCHIVE_PATH == os.getcwd():
        logger.warning("TORRENT ARCHIVE PATH NOT SET")
        await ws_manager.broadcast({
            "type": "log",
            "level": "warn",
            "message": f"{frame.f_code.co_name} Torrent archive path not set",
        })
    if os.getcwd() in [settings.prefs.WATCHER_DESTINATION_PATH, settings.prefs.WATCHER_PATH]:
        logger.warning("WATCHER PATHS NO SET")
        await ws_manager.broadcast({
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


@router.post("/setenv")
async def set_env(payload: SetEnvRequest, request: Request,
                  settings: Settings = Depends(load_settings),
                  job_repo=Depends(get_job_repo),
                  ws_manager: WebSocketManager = Depends(get_ws_manager),
                  ):
    """
    Set the environment variables from the frontend
    User need to restart the docker

    Required
    - Key: dictionary key
    - Value: new value for the environment variable

    Return
    - none
    """

    app = request.app

    # Load env file
    load_dotenv(dotenv_path=app.state.env_file, override=True)

    # Edit file env
    # Replace set_key in python dotenv
    # Permission denied when tries to create a temporary file but it fails because the container is not running as root
    # set_key(str(app.state.env_file), payload.key, payload.value)

    # Current variables value
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

    # Call and Refresh the lru cache
    app.state.settings = get_settings()

    # This key requires a Docker restart
    if payload.key.upper() in ["PREFS__WATCHER_DESTINATION_PATH", "PREFS__WATCHER_PATH", "PREFS__TORRENT_ARCHIVE_PATH",
                               "PREFS__SCAN_PATH"] and os.getenv("DOCKER") == "true":
        app.state.restart_docker = True

    # Update mounted path strings. Changes paths require restarting docker when DOCKER == 1
    await update_mounted_paths(app=app)

    # Ricreate profile (overwrite -> it uses hset command)
    await job_repo.create_profile(dict(settings.prefs))


    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Console message
    logger.info(f"-> Update {payload.key} value -> {payload.value}\n")

    # Send log to the client
    await ws_manager.broadcast({
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
