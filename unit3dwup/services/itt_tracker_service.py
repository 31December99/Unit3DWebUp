# -*- coding: utf-8 -*-
from pathlib import Path

import requests
from unit3dwup.config.constants import MediaStatus
from unit3dwup.config.trackers import TRACKData
from unit3dwup.config.settings import get_settings

from unit3dwup.services.interfaces import TrackerServiceInterface
from unit3dwup.services.itt_tracker_helper import Unit3D
from unit3dwup.models.media import Media

from fastapi import FastAPI
import aiohttp


class ITTtrackerService(TrackerServiceInterface):
    """
    a Class to interact with tracker
    """

    def __init__(self, session: aiohttp.ClientSession, app: FastAPI):
        """
        :param session: aiohttp.ClientSession
        :param app: FastAPI
        """
        self.session = session
        self.app = app
        self.tracker_name = "ITT"
        self.tracker_data = TRACKData.load_from_module(self.tracker_name)
        self.tracker = Unit3D(tracker_name=self.tracker_name, session=session)

    async def prepare_payload(self, media: Media) -> dict:
        """
        :param media: The Media object processed
        :return:

        The Media object processed helps to build the payload for the tracker
        """
        settings = get_settings()
        return {
            "name": media.display_name,
            "tmdb": media.tmdb_id or 0,
            "imdb": media.imdb_id_from_tvdb or 0,
            "tvdb": media.tvdb_id if media.tvdb_id and media.category == 'series' else None,
            "keywords": media.keyword,
            "category_id": self.tracker_data.category.get(media.category),
            "anonymous": int(settings.prefs.ANON),
            "resolution_id": self.tracker_data.resolution.get(media.resolution),
            "mediainfo": media.media_to_string,
            "description": media.description,
            "sd": media.is_hd,
            "type_id": self.tracker_data.filter_type(media.file_name),
            "season_number": media.guess_season,
            "episode_number": media.guess_episode,
            "personal_release": int(settings.prefs.PERSONAL_RELEASE)
        }

    async def upload(self, media: Media) -> dict:
        """
        :param media: Media object processed
        :return:
        """
        # Payload ready
        payload = await self.prepare_payload(media)
        # Load the file and send to the tracker
        response = await self.tracker.upload_t(data=payload, torrent_path=media.torrent_file_path)

        # Wait for response
        if not response:
            media.status = MediaStatus.TRACKER_NOT_UPLOADED
            return {'status': '404', 'message': 'Torrent file not found !', 'file': media.torrent_file_path,
                    'job_id': media.job_id}

        if response.get('success', None):
            self.download_file(url=response.get('data'), destination_path=media.torrent_file_path)

            media.status = MediaStatus.TRACKER_UPLOADED
            await self.app.state.job.update_job(job_id=media.job_id, new_data=media.to_dict())


            return {'status': '200', 'message': 'Torrent uploaded', 'file': media.torrent_file_path,
                    'job_id': media.job_id}
        else:
            media.status = MediaStatus.TRACKER_NOT_UPLOADED
            await self.app.state.job.update_job(job_id=media.job_id, new_data=media.to_dict())
            return {'status': '409', 'message': response.get('data', None),
                    'file': media.torrent_file_path, 'job_id': media.job_id}

    async def search(self, query: str) -> dict:
        return await self.tracker.name(query)


    @staticmethod
    def download_file(url: str, destination_path: Path) -> bool:
        download = requests.get(url)
        if download.status_code == 200:
            # File archived
            with open(destination_path, "wb") as file:
                file.write(download.content)
            return True
        return False
