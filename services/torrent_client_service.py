# -*- coding: utf-8 -*-
import asyncio
import logging

from fastapi import FastAPI

logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

from services.interfaces import TorrentClientServiceInterface
from config.settings import get_settings
from config.logger import get_logger

import qbittorrentapi
from qbittorrentapi import APIConnectionError

settings = get_settings()


class QbittorrentClientService(TorrentClientServiceInterface):
    """
        Qbittorrent client service
    """

    def __init__(self):
        self.qbt_client = None
        self._logged = False
        self.logger = get_logger(self.__class__.__name__)

    async def login(self) -> bool:
        """
        :return: True = success, False = fail
        """
        if self._logged and self.qbt_client and self.qbt_client.is_logged_in:
            return True

        conn_info = dict(
            host=settings.torrent.QBIT_HOST,
            port=settings.torrent.QBIT_PORT,
            username=settings.torrent.QBIT_USER,
            password=settings.torrent.QBIT_PASS,
        )

        self.qbt_client = qbittorrentapi.Client(**conn_info)

        try:
            await asyncio.to_thread(self.qbt_client.auth_log_in)
            self._logged = True
            self.logger.info("Login successfully")
            return True

        except qbittorrentapi.LoginFailed as e:
            self.logger.error(e)
            return False
        except APIConnectionError as e:
            self.logger.error(e)
            return False

    async def add_torrents(self, torrent_paths: list[str], save_path: str, app: FastAPI) -> bool:
        """
        Add torrents to torrent client

        :param torrent_paths: If Docker = true, torrent_path must refer the docker mounted path
        :param save_path: The folder with data file, host path
        :param app: app.state
        :return: success or fail
        """
        if not self.qbt_client or not self.qbt_client.is_logged_in:
            await self.login()

        try:
            await asyncio.to_thread(
            self.qbt_client.torrents_add,
            torrent_files=torrent_paths, # Docker
            save_path=save_path, # Host
            autoTMM=False,
            paused=False,
            is_skip_checking=True
            )
        except qbittorrentapi.exceptions.TorrentFileError as e:
            logging.info(f"Add torrents {e}")
            return False

        return True

    async def list_torrents(self) -> list:
        pass

    async def remove_torrent(self, torrent_id: str) -> bool:
        pass
