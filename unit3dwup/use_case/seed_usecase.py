# -*- coding: utf-8 -*-
import json
from pathlib import Path

from unit3dwup.services.interfaces import TorrentClientServiceInterface
from unit3dwup.services.torrent_client_service import QbittorrentClientService
from unit3dwup.models.media import Media
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


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

    async def execute(self, media_list: list[Media] | None = None) -> JSONResponse:
        """
        Execute the seed use case : load one or more jobs, login to client, verify torrent files,
                                    add torrents file to the client

        :param media_list: list of media to upload used when shared with other services
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

        # Verify whether the *.torrent files still exist and notify the frontend
        filtered_torrent_list = []
        for media in self.media_list:
            if not Path.exists(media.torrent_file_path):
                await self.send_message(media=media, message=f"Torrent file not found !")
            else:
                # discard the invalid torrent file
                filtered_torrent_list.append(media)

        # Add torrents to the client
        if filtered_torrent_list:
            # Ok - try to login
            torr_client_service: TorrentClientServiceInterface = await self.get_fact_client(name=self.client)
            response = await torr_client_service.login()

            # Login failed
            if not response:
                await self.broadcast_messages(f"{self.client} Login failed")
                return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={})

            torrent_path_list = [m.torrent_file_path for m in filtered_torrent_list]
            save_path = self.app.state.settings.prefs.SCAN_PATH

            # Try to add torrents
            execution = await torr_client_service.add_torrents(
                torrent_paths=torrent_path_list,  # Docker path
                save_path=save_path,  # Host path
                app=self.app)

            if execution:
                await self.broadcast_messages(f"Added to {self.client}")
                return JSONResponse(status_code=status.HTTP_200_OK, content={})
            else:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={})
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})



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

    async def broadcast_messages(self, message: str):
        """
        :param message: Send the message to all posters
        :return:
        """
        for media in self.media_list:
            await self.app.state.ws_manager.broadcast({
                "type": "posterLogMessage",
                "job_id": media.job_id,
                "message": message})

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
