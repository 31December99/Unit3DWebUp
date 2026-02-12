# -*- coding: utf-8 -*-
import asyncio
import logging

from fastapi import FastAPI

logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

from services.interfaces import TorrentClientServiceInterface
from config.settings import get_settings

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
            print("Login successfully")
            return True

        except qbittorrentapi.LoginFailed:
            print("Login failed")
            return False
        except APIConnectionError:
            print("Qbittorrent not respond")
            return False

    async def add_torrents(self, torrent_paths: list[str], save_path: str, app: FastAPI) -> bool:
        """
        :param torrent_paths: The files .torrent path
        :param save_path: The folder with data file
        :param app: app.state
        :return: success or fail
        """
        if not self.qbt_client or not self.qbt_client.is_logged_in:
            await self.login()

        try:
            await asyncio.to_thread(
                self.qbt_client.torrents_add,
                torrent_files=torrent_paths,
                save_path=save_path,
                autoTMM=False,
                paused=False,
                is_skip_checking=True
            )
        except qbittorrentapi.exceptions.TorrentFileError as e:
            logging.debug(f"Add torrents {e}")
            return False

        return True

    async def list_torrents(self) -> list:
        pass

    async def remove_torrent(self, torrent_id: str) -> bool:
        pass
