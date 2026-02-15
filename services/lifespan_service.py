# -*- coding: utf-8 -*-
import os
from pathlib import Path

from fastapi import FastAPI
from config.settings import Settings
from config.logger import get_logger


async def update_mounted_paths(app: FastAPI):
    """
     Updates to mounted path strings are valid only when the backend is running on the host
     When using docker ,docker must also be restarted
    :param app: the FastAPI app
    :return:
    """
    settings = Settings()
    logger = get_logger(__name__)

    # Switch path between dev and Docker
    app.state.watcher_path = "/home/app/watcher" if os.getenv(
        "DOCKER") == "true" else app.state.settings.prefs.WATCHER_PATH
    app.state.watcher_destination_path = "/home/app/watcher_destination_path" if os.getenv(
        "DOCKER") == "true" else app.state.settings.prefs.WATCHER_DESTINATION_PATH

    app.state.scan_path = "/home/app/scan" if os.getenv("DOCKER") == "true" else app.state.settings.prefs.SCAN_PATH
    torrent_archive_path = Path("/home/app/torrent_archive") if os.getenv("DOCKER") == "true" else Path(
        settings.prefs.TORRENT_ARCHIVE_PATH)
    app.state.torrent_archive_path = torrent_archive_path.expanduser().resolve()

    # Env file mount: used to edit Env file from the frontend
    app.state.env_file = Path(".env") if os.getenv("DOCKER") == "true" else Path(os.getenv("ENV_PATH", ""))

    # Main folder
    logger.info("\nChecking Unit3D configuration file..\n")
    logger.info(f"Docker mode          -> '{os.getenv("DOCKER")}'")
    logger.info(f"Scan Path            -> '{app.state.scan_path}'")
    logger.info(f"Env Path             -> '{app.state.env_file}'\n")
    logger.info(f"Torrent Archive Path -> '{app.state.torrent_archive_path}'")
    logger.info(f"Watcher Path         -> '{app.state.watcher_path}'")
    logger.info(f"Watcher Dest. Path   -> '{app.state.watcher_destination_path}'\n")

async def checking_env_file(app: FastAPI):
    settings = Settings()
    logger = get_logger(__name__)

    # Check configuration file (only once because get_settings() is cached)
    for field_name, field in settings.tracker.model_fields.items():
        # optional field (default=None)
        if field.default is None:
            value = getattr(settings.tracker, field_name)
            if value is None:
                logger.warning(f"{field_name} not set in .env – related feature may be disabled")

