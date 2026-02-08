# -*- coding: utf-8 -*-
import json
from pathlib import Path

from models.media import Media
from services.interfaces import TorrentClientServiceInterface
from services.torrent_client_service import QbittorrentClientService


class SeedUseCase:
    def __init__(self, app, job_list: list[str], client: str):
        """
        :param app: the fastapi app
        :param job_list: list of jobs id
        :param client: torrent client name
        """
        self.app = app
        self.job_list = job_list
        self.client = client

    async def execute(self) -> bool:

        # Load each poster contained in the job list
        results = [json.loads(await self.app.state.job.get_job(job_id)) for job_id in self.job_list]
        media_list = [
            Media.from_dict(item)
            for item in results
        ]

        torr_client_service: TorrentClientServiceInterface = await self.get_fact_client(name=self.client)
        response = await torr_client_service.login()

        # Login failed
        if not response:
            for job_id in self.job_list:
                await self.app.state.ws_manager.broadcast({
                    "type": "posterLogMessage",
                    "job_id": job_id,
                    "message": f"{self.client} Login failed"})
            return False

        # Verify that the *.torrent file still exists
        results = [m.torrent_file_path for m in media_list if Path.exists(Path(m.torrent_file_path))]

        # Get the data path ( scan path)
        save_path = media_list[0].folder

        # Add to the torrent client
        execution = await torr_client_service.add_torrents(results, save_path, app=self.app)
        if execution:
            for job_id in self.job_list:
                await self.app.state.ws_manager.broadcast({
                    "type": "posterLogMessage",
                    "job_id": job_id,
                    "message": f"added to seeding"})
            return True
        return False

    @staticmethod
    async def get_fact_client(name: str) -> TorrentClientServiceInterface | None:
        if name == "qbittorrent":
            return QbittorrentClientService()
        # TODO: aggiungere un altro client mantenendo gli stessi metodi
        # in attesa di essere aggiunti
        # if name == "deluge": return DelugeClientService(...)
        # if name == "transmission": return TransmissionClientService(...)
        return None
