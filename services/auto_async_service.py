# -*- coding: utf-8 -*-

import os
import asyncio
import json
from pathlib import Path

from repositories.media_info_factory import MediaFileFactory
from services.utility import ManageTitles
from config.constants import MediaStatus
from config.logger import get_logger
from models.media import Media

from fastapi import FastAPI

class AsyncMediaManager:
    """
    Process files and folder
    Every file or folder is converted in a Media Object
    Every Media object receives additional values
    """

    def __init__(self, path: str, app: FastAPI, job_id_list: str, force_category: int = None):
        """
        :param path: The user path
        :param force_category: force category to movie or series
        """
        self.path = os.path.normpath(path)
        self.job_id_list = job_id_list
        self.app = app
        self.mode = 'auto'
        self.force_category = force_category
        self.is_dir = os.path.isdir(self.path)
        self.media_list: list[Media] = []
        self.sem = asyncio.Semaphore(60)
        self.logger = get_logger(self.__class__.__name__)

    @staticmethod
    def scan_folder(path: Path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file() and ManageTitles.filter_ext(entry.name):
                    yield entry

    async def process_all(self) -> list[Media]:
        """
        start method to process all files

        :returns:
            list[str]: a list of media objects
        """
        if os.path.isfile(self.path):
            self.mode = "man"

        if self.mode in ["man", "folder"]:
            self.media_list = await self.upload()
        else:  # modalità 'auto'
            self.media_list = await self.scan()

        tasks = [self.process_media(media) for media in self.media_list]

        results = await asyncio.gather(*tasks)
        return [m for m in results if m]

    async def scan(self) -> list[Media]:
        """
        process all files or folders ( 1 subfolder only) ( auto)

        :returns:
            list[str]: a list of media objects
        """
        if not os.path.exists(self.path):
            self.logger.warning(f"Path not found {self.path}")
            return []

        if not self.is_dir:
            self.logger.warning(f"We can't scan a file {self.path}")
            return []

        entries = await asyncio.to_thread(os.listdir, self.path)
        if not entries:
            self.logger.warning(f"Folder {self.path} is empty")

        files = [Path(self.path) / e for e in entries if
                 os.path.isfile(Path(self.path) / e) and ManageTitles.filter_ext(e)]
        subfolders = [Path(self.path) / e for e in entries if os.path.isdir(Path(self.path) / e)]

        async def safe_create(path):
            async with self.sem:
                return await self._create_media_list([path])

        tasks = [safe_create(p) for p in files + subfolders]
        media_list = await asyncio.gather(*tasks)
        # Clean the list, remove None object
        return [m for sublist in media_list for m in sublist if m]

    async def upload(self) -> list[Media]:
        """
            process only one file or folder

        :returns:
            list[str]: a list of media objects
        """

        if self.is_dir:
            files = await asyncio.to_thread(os.listdir, self.path)
            video_files = [Path(self.path) / f for f in files if ManageTitles.filter_ext(f)]

            if self.mode == "man":
                return await self._create_media_list(video_files)
            if self.mode == "folder":
                return await self._create_media_list([self.path])
            return []
        else:
            return await self._create_media_list([self.path])

    async def _create_media_list(self, paths: list[str]) -> list[Media]:
        """
        create a Media object for each single file or single folder encountered
                      files inside subfolders are not converted in Media objects
        :param paths: list of file path
        :return:  list[Media]: a list of media objects based on user path
        """

        return [
            Media(folder=self.path, subfolder=os.path.basename(_path),
                  torrent_archive_path=self.app.state.torrent_archive_path)
            for _path in paths
            if _path is not None
        ]

    async def process_media(self, media: Media) -> Media | None:
        """
        start method to process media object ( file or folder)

        :param media: single Media object
        :return:
        """
        path = media.torrent_path
        if self.force_category:
            media.category = self.force_category

        if os.path.isdir(path):
            success = await self.process_folder(media)
        elif os.path.isfile(path):
            success = await self.process_file(media)
        else:
            self.logger.warning("Process Media return None")
            return None

        # Add a Mediainfo object
        if success:
            media.mediafile = await MediaFileFactory.from_path(media.file_name)
            assert media.mediafile is not None, "MediaFileFactory ha restituito None"
            await self.app.state.ws_manager.broadcast({
                "type": "log",
                "level": "success",
                "message": f"Process media -> {media.display_name}",
            })
            return media

        return None

    async def process_file(self, media: Media) -> bool:
        """
        process media object file

        :param media: single Media object
        :return: success or failure
        """
        media.status = MediaStatus.INDEXED
        media.job_id_list = self.job_id_list
        media.file_name = media.torrent_path
        media.display_name, _ = os.path.splitext(os.path.basename(media.file_name))
        media.display_name = ManageTitles.clean_text(media.display_name)
        media.torrent_name = os.path.basename(media.file_name)
        media.doc_description = media.file_name

        # Read file size value
        async with self.sem:
            media.size = await asyncio.to_thread(lambda: os.stat(media.file_name).st_size)

        # Convert PosixPath to str and build info
        media.metainfo = json.dumps([{"length": media.size, "path": [str(media.file_name)]}], indent=4)
        return True

    async def process_folder(self, media: Media) -> bool:
        """
        process media object folder

        :param media: single Media object
        :return: success or failure
        """
        # Read the folder and create a list of files
        # TODO forse ha poco senso asyncio.to_thread qui
        entries = await asyncio.to_thread(os.listdir, media.torrent_path)
        files = [my_file for my_file in entries if ManageTitles.filter_ext(my_file)]

        if not files:
            return False

        files.sort()
        media.status = MediaStatus.INDEXED
        media.job_id_list = self.job_id_list
        media.file_name = Path(media.torrent_path) / files[0]
        media.display_name = ManageTitles.clean_text(Path(media.torrent_path).name)
        media.torrent_name = Path(media.torrent_path).name
        media.doc_description = "\n".join(files)

        entries = await asyncio.to_thread(lambda: list(self.scan_folder(media.torrent_path)))
        sizes = [e.stat().st_size for e in entries]
        files = [e.name for e in entries]

        # Build metainfo
        media.size = sum(sizes)
        media.metainfo = json.dumps([{"length": s, "path": [f]} for f, s in zip(files, sizes)], indent=4)
        return True
