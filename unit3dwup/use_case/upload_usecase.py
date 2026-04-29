# -*- coding: utf-8 -*-
import json
import asyncio
from typing import Any

from unit3dwup.services.interfaces import TrackerServiceInterface
from unit3dwup.services.itt_tracker_service import ITTtrackerService
from unit3dwup.models.media import Media
from unit3dwup.config.logger import get_logger

import aiohttp
from fastapi import FastAPI


class UploadUseCase:

    def __init__(self, app: FastAPI, job_id: str | None = None):
        """
        :param app: the FastAPI app
        :param job_id: the job id. Used for a single service upload
        """

        self.media_list: list[Media] | None = None
        self.app = app
        self.job_id = job_id
        self.logger = get_logger(self.__class__.__name__)

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
            self.logger.debug(f"Start Uploaded Torrents {uploaded_torrents}")

            # Send a message to frontend for each uploaded media
            await self.broadcast_messages(uploaded_torrents=uploaded_torrents)

        # Overall execution outcome: True iff every torrent reported HTTP 200.
        return all(_is_successful(t) for t in uploaded_torrents)

    async def broadcast_messages(self, uploaded_torrents: tuple[Any]) -> None:
        """
        :param uploaded_torrents: results message from the uploaded torrents
        :return:
        """
        for torrent in uploaded_torrents:
            await self.app.state.ws_manager.broadcast({
                "type": "posterLogMessage",
                "job_id": torrent['job_id'],
                # Distinguish success from failure so the frontend can colour
                # the poster correctly and clients listening on /ws can react
                # to an error without having to parse `message` heuristically.
                "level": "success" if _is_successful(torrent) else "error",
                "message": f"{torrent['message']}"})


def _is_successful(torrent: dict) -> bool:
    """A torrent dict from `ITTtrackerService.upload` reports `status: '200'`
    on success and `'404'` / `'409'` (or other non-2xx) on failure."""
    status = str(torrent.get('status') or '')
    return status.startswith('2')
