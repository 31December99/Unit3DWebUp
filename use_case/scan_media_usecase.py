# -*- coding: utf-8 -*-
import asyncio
import aiohttp

from repositories.interfaces import JobRepositoryInterface
from config.constants import MediaStatus

from services.video_service import VideoService, BuildService
from services.media_service import MediaService, MediaService2
from services.auto_async_service import AsyncMediaManager


class ScanMediaUseCase:
    """
    Manage services to search for ID create screenshots and create descriptions sequentially
    """

    def __init__(
            self,
            manager: AsyncMediaManager,
            media_service: MediaService,
            media_service2: MediaService2,
            job_repo: JobRepositoryInterface,
            session: aiohttp.ClientSession,
            job_list: list[str],
    ):
        """
        :param manager: instance of the scanner
        :param media_service: instance of external service tmdb
        :param media_service2: instance of the external service tvdb
        :param job_repo: instance of the job repository ( redis)
        :param session: aiohttp session
        :param job_list: list of jobs id for the current list
        """
        self.manager = manager
        self.media_services = [media_service, media_service2]
        self.job_repo = job_repo
        self.session = session
        self.job_list = job_list

    async def execute(self):

        # Scan the local files and create a Media object for each one
        media_list = await self.manager.process_all()

        # Process all Media objects concurrently
        return await asyncio.gather(
            *(self._process_media(m) for m in media_list)
        )

    async def _process_media(self, media):
        # job_id already exists in the job_list ?
        # if does -> no description created -> job already exist
        if media.job_id in self.job_list:
            return media

        # We get a new job_id , search for tmdb and tvdb id !
        await self._identify_media(media)

        # ops! ( for example ID not found ) #todo split tmdb and tvdb case
        if media.status == MediaStatus.DB_ERROR:
            return media

        # return if ffmpeg fail
        if not await self._generate_video(media):
            return media

        # Pass the screenshot to the image host and build a html description for the tracker
        await self._build_description(media)

        # Save to redis
        await self._save(media)

        # return the current media object
        return media

    async def _identify_media(self, media):
        media.status = MediaStatus.DB_NOT_IDENTIFIED

        try:
            # Search id from tmdb, tvdb
            # and search imdb id in the tvdb remote_ids list
            for service in self.media_services:
                success = await service.fetch(media)
                if success:
                    media.status = MediaStatus.DB_IDENTIFIED
        except Exception as e:
            await self._handle_error(media, MediaStatus.DB_ERROR, e)

        # save to redis
        await self._save(media)

    async def _generate_video(self, media):

        try:
            # Extract the screenshots
            video_service = VideoService(media)
            await video_service.generate()
            media.status = MediaStatus.VIDEO_READY
            return True

        except Exception as e:
            await self._handle_error(media, MediaStatus.VIDEO_ERROR, e)
            return False

    async def _build_description(self, media):

        try:
            # Upload the screenshot to imagehost and return a html code for the description
            builder = BuildService(
                media_list=[media],
                session=self.session
            )
            await builder.description()

        except Exception as e:
            await self._handle_error(media, MediaStatus.DESCRIPTION_ERROR, e)

    async def _handle_error(self, media, status, error):
        media.status = status
        media.error = str(error)
        print(status, media.error)
        await self._save(media)

    async def _save(self, media):

        await self.job_repo.create_job(
            job_id=media.job_id,
            data=media.to_dict()
        )
