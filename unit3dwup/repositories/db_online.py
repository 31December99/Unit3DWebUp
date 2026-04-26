# -*- coding: utf-8 -*-
from typing import TypeVar
import aiohttp

from unit3dwup.models.interfaces import MediaRepoInterface
from unit3dwup.models.movie import AltTitle, NowPlaying
from unit3dwup.models.tv import OnTheAir, DataResponse
from unit3dwup.models.keywords import Keyword
from unit3dwup.models.videos import Data

from unit3dwup.repositories.interfaces import MovieRepositoryInterface

from unit3dwup.services.tmdb import TmdbAsyncAPI
from unit3dwup.services.tvdb import TvdbAsyncAPI

T = TypeVar('T')


class Tmdb(TmdbAsyncAPI, MovieRepositoryInterface):
    """
    the purpose is providing a common interface for calling service classes
    while keeping the service implementations separate
    It is an update of the old code unit3dup 0.8.21
    """

    def __init__(self, session: aiohttp.ClientSession | None = None):
        super().__init__(session)

    async def search(self, query: str, category: str) -> list[T] | None:
        result = await super().search(query=query, category=category)
        return result

    async def alternative(self, movie_id: int, category: str) -> AltTitle | DataResponse | None:
        return await super().alternative(movie_id=movie_id, category=category)

    async def videos(self, movie_id: int, category: str) -> Data | None:
        return await super().videos(movie_id=movie_id, category=category)

    async def details(self, video_id: int, category: str) -> Data | None:
        return await super().details(video_id=video_id, category=category)

    async def keywords(self, movie_id: int, category: str) -> Keyword | None:
        return await super().keywords(movie_id=movie_id, category=category)

    async def playing(self, category: str) -> list[NowPlaying] | list[OnTheAir] | None:
        return await super().playing(category=category)

    async def close(self):
        await self.session.close()


class Tvdb(TvdbAsyncAPI, MovieRepositoryInterface):
    """
    the purpose is providing a common interface for calling service classes
    while keeping the service implementations separate
    It is an update of the old code unit3dup 0.8.21
    """

    def __init__(self, session: aiohttp.ClientSession | None = None):
        super().__init__(session)

    async def search(self, query: str, category: str = None) -> list[MediaRepoInterface]:
        await super().tvdb_login()
        return await super().search(query=query, category=category)

    async def alternative(self, movie_id: int, category: str) -> AltTitle | DataResponse | None:
        pass

    async def videos(self, movie_id: int, category: str) -> Data | None:
        pass

    async def details(self, video_id: int, category: str) -> Data | None:
        pass

    async def keywords(self, movie_id: int, category: str) -> Keyword | None:
        pass

    async def playing(self, category: str) -> list[NowPlaying] | list[OnTheAir] | None:
        pass

    async def close(self):
        await self.session.close()
