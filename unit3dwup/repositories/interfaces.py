# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from unit3dwup.models.interfaces import MediaRepoInterface
from unit3dwup.models.movie import Movie, NowPlaying
from unit3dwup.models.keywords import Keyword
from unit3dwup.models.videos import Data

from fastapi import FastAPI


class MovieRepositoryInterface(ABC):
    """
    an Interface class for TMDB and TVDB to share the same methods
    """

    @abstractmethod
    async def search(self, query: str, category: str = None) -> list[MediaRepoInterface]: ...

    @abstractmethod
    async def alternative(self, movie_id: int, category: str) -> list: ...

    @abstractmethod
    async def videos(self, movie_id: int, category: str) -> Data: ...

    @abstractmethod
    async def details(self, movie_id: int, category: str) -> Movie: ...

    @abstractmethod
    async def keywords(self, movie_id: int, category: str) -> list[Keyword]: ...

    @abstractmethod
    async def playing(self, category: str) -> list[NowPlaying]: ...

    @abstractmethod
    async def close(self) -> None: ...


class JobRepositoryInterface(ABC):
    """
    an Interface class for Redis to share the same methods with other repositories that are not yet implemented
    """
    @abstractmethod
    async def connect(self, app: FastAPI): ...

    @abstractmethod
    async def create_job(self, job_id: str, data: dict): ...

    @abstractmethod
    async def create_profile(self, data: dict): ...

    @abstractmethod
    async def update_job(self, job_id: str, new_job: dict): ...

    @abstractmethod
    async def delete_job_list(self, job_id: str): ...

    @abstractmethod
    async def close(self): ...
