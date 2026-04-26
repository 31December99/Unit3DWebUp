# -*- coding: utf-8 -*-
from typing import TypeVar

from unit3dwup.external.async_http_client_service import AsyncHttpClient
from unit3dwup.models.interfaces import MediaRepoInterface
from unit3dwup.models.tvdb_search import TvdbSearchResult
from unit3dwup.config.settings import get_settings

import aiohttp

settings = get_settings()
T = TypeVar('T')


class TvdbAsyncAPI:
    def __init__(self, session: aiohttp.ClientSession | None = None):
        """
        :param session: an active aiohttp session
        """
        # Use the apikey received from the website (apikey for project)
        self.api_key = settings.tracker.TVDB_APIKEY
        # get a new session
        self.session = session or aiohttp.ClientSession()
        # an http async client instance
        self.http = AsyncHttpClient(self.session)
        # the classe state for tvdb token
        self.token = None

    async def tvdb_login(self) -> str:
        """
        Pass the api_key to Tvdb wait for a new jwt token
        :return: None
        """
        if self.token:
            return self.token
        url = "https://api4.thetvdb.com/v4/login"
        payload = {"apikey": self.api_key}

        resp = await self.session.post(url, json=payload)
        data = await resp.json()
        self.token = data["data"]["token"]
        return self.token

    async def search(self, query: str, category: str = "series") -> list[MediaRepoInterface]:
        """
        :param query: the searched title
        :param category: restrict search to 'movies' or 'series'
        :return: a TVDB repository implementing the MediaRepoInterface
        """
        if not self.token:
            self.token = await self.tvdb_login()

        url = f"https://api4.thetvdb.com/v4/search?query={query}&type={category}"
        headers = {"Authorization": f"Bearer {self.token}"}

        resp = await self.session.get(url, headers=headers)
        resp.raise_for_status()
        payload = await resp.json()

        # Build TvdbSearchResult objects
        return [
            TvdbSearchResult.from_dict(item)
            for item in payload.get("data", [])
        ]
