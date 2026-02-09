# -*- coding: utf-8 -*-
import json
from typing import Any

from services.interfaces import TrackerServiceInterface
from services.itt_tracker_service import ITTtrackerService
from models.media import Media

import asyncio
import aiohttp
from fastapi import FastAPI
from config import logger


class UploadUseCase:

    def __init__(self, app: FastAPI, job_id: str | None = None):
        """
        :param app: the FastAPI app
        :param job_id: the job id. Used for a single service upload
        """

        self.media_list: list[Media] | None = None
        self.app = app
        self.job_id = job_id

    async def execute(self, media_list: list[Media] | None = None) -> bool:
        """
        Execute the seed use case : load one or more jobs, login to tracker, upload the torrents,
                                    send message to the frontend

        :param media_list: list of media to upload used when shared with other services
        :return: true or false
        """
        self.media_list = media_list
        # Create the media list for single torrent
        if self.job_id and not self.media_list:
            results = await self.app.state.job.get_job(job_id=self.job_id)
            self.media_list = [
                Media.from_dict(item)
                for item in [json.loads(results)]
            ]

        async with aiohttp.ClientSession() as session:

            # Tracker instance
            tracker_service: TrackerServiceInterface = ITTtrackerService(session, self.app)

            # Build a list of media
            tasks = [tracker_service.upload(media) for media in self.media_list]

            # Concurrent execution
            uploaded_torrents = await asyncio.gather(*tasks)
            logger.debug(f"Start Uploaded Torrents {uploaded_torrents}")

            # Send a message to frontend for each uploaded media
            await self.broadcast_messages(uploaded_torrents=uploaded_torrents)

            for torrent in uploaded_torrents:
                await self.app.state.ws_manager.broadcast({
                    "type": "posterLogMessage",
                    "job_id": torrent['job_id'],
                    "message": f"{torrent['message']}"})
        return True

    async def broadcast_messages(self, uploaded_torrents: tuple[Any]) -> None:
        """
        :param uploaded_torrents: results message from the uploaded torrents
        :return:
        """
        for torrent in uploaded_torrents:
            await self.app.state.ws_manager.broadcast({
                "type": "posterLogMessage",
                "job_id": torrent['job_id'],
                "message": f"{torrent['message']}"})
