# -*- coding: utf-8 -*-
import os
from pathlib import Path

from config.constants import MediaStatus
from config.trackers import TRACKData
from config.settings import Load

from services.interfaces import TrackerServiceInterface
from services.itt_tracker_helper import Unit3D

from models.media import Media

from fastapi import FastAPI
import aiohttp

config = Load().load_config()


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
        return {
            "name": media.display_name,
            "tmdb": media.tmdb_id,
            "imdb": media.imdb_id_from_tvdb or 0,
            "tvdb": media.tvdb_id or 0,
            "keywords": media.keyword,
            "category_id": self.tracker_data.category.get(media.category),
            "anonymous": int(config.user_preferences.ANON),
            "resolution_id": self.tracker_data.resolution.get(media.resolution),
            "mediainfo": media.media_to_string,
            "description": media.description,
            "sd": media.is_hd,
            "type_id": self.tracker_data.filter_type(media.file_name),
            "season_number": media.guess_season or "",
            "episode_number": media.guess_episode or "",
            "personal_release": int(config.user_preferences.PERSONAL_RELEASE)
        }

    async def upload(self, media: Media) -> dict:
        """
        :param media: Media object processed
        :return:
        """
        # Payload ready
        payload = await self.prepare_payload(media)

        # Build the torrent file path
        archive = os.path.join(config.user_preferences.TORRENT_ARCHIVE_PATH, self.tracker_name)
        torrent_filepath: Path = (Path(archive) / f"{media.torrent_name}.torrent")

        # Load the file and send to the tracker
        response = await self.tracker.upload_t(data=payload, torrent_path=torrent_filepath)

        # Wait for response
        if not response:
            media.status = MediaStatus.TRACKER_NOT_UPLOADED
            return {'status': '404', 'message': 'Torrent file not found !', 'file': torrent_filepath,
                    'job_id': media.job_id}

        if response.get('success', None):
            media.status = MediaStatus.TRACKER_UPLOADED
            await self.app.state.job.update_job(job_id=media.job_id, new_data=media.to_dict())
            return {'status': '200', 'message': response.get('message'), 'file': torrent_filepath,
                    'job_id': media.job_id}
        else:
            media.status = MediaStatus.TRACKER_NOT_UPLOADED
            await self.app.state.job.update_job(job_id=media.job_id, new_data=media.to_dict())
            return {'status': '409', 'message': response.get('data', None),
                    'file': torrent_filepath, 'job_id': media.job_id}

    async def search(self, query: str) -> dict:
        return await self.tracker.name(query)
