# -*- coding: utf-8 -*-

from services.interfaces import TrackerServiceInterface
from services.itt_tracker_service import ITTtrackerService
from models.media import Media

import asyncio
import aiohttp
from fastapi import FastAPI
from config import logger

class UploadService:

    def __init__(self, media_list: list[Media], app: FastAPI):
        self.media_list = media_list
        self.app = app

    async def start(self):

        async with aiohttp.ClientSession() as session:
            tracker_service: TrackerServiceInterface = ITTtrackerService(session, self.app)
            tasks = [tracker_service.upload(media) for media in self.media_list]
            uploaded_torrents = await asyncio.gather(*tasks)
            logger.debug(f"Start Uploaded Torrents {uploaded_torrents}")

            for torrent in uploaded_torrents:
                if torrent['status'] == '409':
                    await self.app.state.ws_manager.broadcast({
                        "type": "progress",
                        "level": "progress",
                        "job_id": torrent['job_id'],
                        "process": "error",
                        "progress": 100.0,
                        "message": f"{torrent['message']} {torrent['file']}"})

                if torrent['status'] == '200':
                    await self.app.state.ws_manager.broadcast({
                        "type": "progress",
                        "level": "progress",
                        "job_id": torrent['job_id'],
                        "process": "Uploaded",
                        "progress": 100.0,
                        "message": f"{torrent['message']} {torrent['file']}"})
