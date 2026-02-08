# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Iterable
from fastapi import FastAPI
from models.media import Media


class VideoServiceInterface(ABC):
    @abstractmethod
    async def generate(self) -> None:
        """Extract screenshot"""
        ...


class DescriptionBuilderInterface(ABC):
    @abstractmethod
    async def description(self) -> None:
        """Build a description for the tracker"""
        ...

    @abstractmethod
    async def close(self) -> None: ...


class TorrentServiceInterface(ABC):

    @abstractmethod
    def _create_batch(self, media_list: Iterable[Media], trackers: list[str] = None,
                            workers: int | None = None) -> list[str]:
        """Process groups of media and create for each a torrent file"""
        ...

    @abstractmethod
    def start(self, media_list: list[Media], batch_size=16, workers: int = 2):
        """ Build a list of batches """
        ...


class TrackerServiceInterface(ABC):

    @abstractmethod
    async def prepare_payload(self, media: Media) -> dict:
        """ Build the payload for the tracker """
        pass

    @abstractmethod
    async def upload(self, media: Media) -> dict:
        """Upload the torrent and return a result"""
        pass

    @abstractmethod
    async def search(self, query: str) -> dict:
        """ Search for a title """
        pass


class TorrentClientServiceInterface(ABC):
    """
        Interface for torrent clients
    """
    @abstractmethod
    async def login(self) -> bool: ...

    @abstractmethod
    async def add_torrents(self, torrent_paths: list[str], save_path: str, app: FastAPI) -> bool: ...

    @abstractmethod
    async def list_torrents(self) -> list: ...

    @abstractmethod
    async def remove_torrent(self, torrent_id: str) -> bool: ...
