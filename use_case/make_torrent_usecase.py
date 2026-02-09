# -*- coding: utf-8 -*-
import json
from pathlib import Path

from services.torrent_service import TorrentService
from models.media import Media
from fastapi import FastAPI


class MakeTorrentUseCase:
    def __init__(self, app: FastAPI, job_id: str | None = None):
        """
        Create one or more torrents

        :param app: the fastapi app
        :param job_id: the job id
        """
        self.media_list = None
        self.app = app
        self.job_id = job_id

    async def execute(self, media_list: list[Media] | None = None) -> bool:
        """
        Execute the torrent use case: create one or more torrents , notify to frontend
        :param media_list: list of media objects used to create torrents
        :return:
        """

        # Create the media list for single torrent based on the job_id
        if self.job_id and not media_list:
            results = await self.app.state.job.get_job(job_id=self.job_id)
            self.media_list = [
                Media.from_dict(item)
                for item in [json.loads(results)]
            ]
        else:
            # Receive a list
            self.media_list = media_list

        # FILTER: filter for existing torrent. Ensures that only new torrents are created
        filtered_torrent_list = []
        for media in self.media_list:
            if Path.exists(Path(media.torrent_file_path)):
                # notify the frontend
                await self.send_message(media=media, message=f"Torrent file exists")
            else:
                # Add media objects for the new torrents
                filtered_torrent_list.append(media)

        if filtered_torrent_list:
            torrent_service = TorrentService(app=self.app)
            await torrent_service.start(media_list=filtered_torrent_list)
            return True

        return False

    async def send_message(self, media: Media, message: str):
        """
        :param media: The current Media object
        :param message: Send the message to single poster
        :return:
        """
        await self.app.state.ws_manager.broadcast({
            "type": "posterLogMessage",
            "job_id": media.job_id,
            "message": message})
