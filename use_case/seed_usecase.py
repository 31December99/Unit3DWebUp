# -*- coding: utf-8 -*-
import json
from pathlib import Path

from services.interfaces import TorrentClientServiceInterface
from services.torrent_client_service import QbittorrentClientService
from models.media import Media
from fastapi import FastAPI


class SeedUseCase:
    def __init__(self, app: FastAPI, client: str, job_id: str | None = None):
        """
        :param app: the fastapi app
        :param job_id: the job id
        :param client: torrent client name
        """
        self.media_list = None
        self.app = app
        self.job_id = job_id
        self.client = client

    async def execute(self, media_list: list[Media] | None = None) -> bool:
        """
        Execute the seed use case : load one or more jobs, login to client, verify torrent files,
                                    add torrents file to the client

        :param media_list: list of media to upload used when shared with other services
        :return:
        """

        self.media_list = media_list
        # Create the media list for single torrent
        if self.job_id and not self.media_list:
            results = await self.app.state.job.get_job(job_id=self.job_id)
            self.media_list = [
                Media.from_dict(item)
                for item in [json.loads(results)]
            ]

        torr_client_service: TorrentClientServiceInterface = await self.get_fact_client(name=self.client)
        response = await torr_client_service.login()

        # Login failed
        if not response:
            await self.send_message(f"{self.client} Login failed")
            return False

        # Verify that the *.torrent file still exists
        results = [m.torrent_file_path for m in self.media_list if Path.exists(Path(m.torrent_file_path))]

        # Get the data path ( scan path)
        save_path = self.media_list[0].folder

        # Add torrents to the client
        execution = await torr_client_service.add_torrents(results, save_path, app=self.app)
        if execution:
            await self.send_message(f"Added to {self.client}")
            return True
        return False

    @staticmethod
    async def get_fact_client(name: str) -> TorrentClientServiceInterface | None:
        """
        :param name: name of the default torrent client
        :return:
        """

        if name == "qbittorrent":
            return QbittorrentClientService()
        # TODO: aggiungere un altro client mantenendo gli stessi metodi
        # in attesa di essere aggiunti
        # if name == "deluge": return DelugeClientService(...)
        # if name == "transmission": return TransmissionClientService(...)
        return None

    async def send_message(self, message: str):
        """
        :param message: message to send to the frontend
        :return:
        """
        for media in self.media_list:
            await self.app.state.ws_manager.broadcast({
                "type": "posterLogMessage",
                "job_id": media.job_id,
                "message": message})
