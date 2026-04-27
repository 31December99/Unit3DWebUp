# -*- coding: utf-8 -*-
from dataclasses import fields
from typing import TypeVar
import aiohttp

from models.movie import (Movie, AltTitle, Title, NowPlaying, MovieDetails, Genre,
                          ProductionCompany, SpokenLanguage, ProductionCountry)
from models.tv import (TVShowDetails, CreatedBy, Network, LastEpisodeToAir, Season,
                       OnTheAir, TvShow, DataResponse, Alternative)
from models.videos import Videos, Data
from models.keywords import Keyword

from external.async_http_client_service import AsyncHttpClient

from config.settings import get_settings

settings = get_settings()
BASE_URL = "https://api.themoviedb.org/3"
TMDB_APIKEY = settings.tracker.TMDB_APIKEY
T = TypeVar('T')


# Endpoints TMDB
class TmdbEndpoints:
    BASE_URL = "https://api.themoviedb.org/3"
    # TMDB occasionally adds new fields to its responses (e.g. `softcore`). The
    # local dataclasses don't declare them, so passing the raw payload via
    # `Movie(**item)` blows up with TypeError. Filter to known fields before
    # instantiation so the upstream payload doesn't break the parser.
    _MOVIE_FIELDS = {f.name for f in fields(Movie)}
    _TV_FIELDS = {f.name for f in fields(TvShow)}

    @staticmethod
    def _only_known(item: dict, allowed: set[str]) -> dict:
        """Return a copy of ``item`` with only the keys present in ``allowed``."""
        return {k: v for k, v in item.items() if k in allowed}

    @staticmethod
    def movie_search(query: str) -> str:
        return f"{TmdbEndpoints.BASE_URL}/search/movie"

    @staticmethod
    def tv_search(query: str) -> str:
        return f"{TmdbEndpoints.BASE_URL}/search/tv"

    @staticmethod
    def alternative_movie(movie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/movie/{movie_id}/alternative_titles"

    @staticmethod
    def alternative_show(serie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/tv/{serie_id}/alternative_titles"

    @staticmethod
    def videos_movie(movie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/movie/{movie_id}/videos"

    @staticmethod
    def videos_show(serie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/tv/{serie_id}/videos"

    @staticmethod
    def movie_details(movie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/movie/{movie_id}"

    @staticmethod
    def tv_details(serie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/tv/{serie_id}"

    @staticmethod
    def movie_keywords(movie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/movie/{movie_id}/keywords"

    @staticmethod
    def tv_keywords(serie_id: int) -> str:
        return f"{TmdbEndpoints.BASE_URL}/tv/{serie_id}/keywords"

    @staticmethod
    def movie_now_playing() -> str:
        return f"{TmdbEndpoints.BASE_URL}/movie/now_playing"

    @staticmethod
    def tv_on_the_air() -> str:
        return f"{TmdbEndpoints.BASE_URL}/tv/on_the_air"


# TMDB async
class TmdbAsyncAPI:
    def __init__(self, session: aiohttp.ClientSession | None = None):
        self.api_key = TMDB_APIKEY
        self.language = "it-IT"
        self.session = session or aiohttp.ClientSession()
        self.http = AsyncHttpClient(self.session)

    async def close(self):
        await self.session.close()

    async def search(self, query: str, category: str) -> list[T]:
        """
        :param query: the title to search for
        :param category: serie or movie
        :return:
        """
        url = TmdbEndpoints.movie_search(query) if category == "movie" else TmdbEndpoints.tv_search(query)
        params = {"api_key": self.api_key, "query": query, "language": self.language}

        data = await self.http.get(url, params=params)

        results: list[T] = []
        if data and "results" in data:
            items = data["results"]
            if category == "movie":
                for item in items:
                    results.append(Movie(**_only_known(item, _MOVIE_FIELDS)))
            else:  # "tv"
                for item in items:
                    results.append(TvShow(**_only_known(item, _TV_FIELDS)))
        return results

    async def alternative(self, movie_id: int, category: str) -> AltTitle | DataResponse | None:
        """
        :param movie_id: the movie id
        :param category: serie or movie
        :return:

        Get alternative title of a movie or serie

        """
        url = TmdbEndpoints.alternative_movie(movie_id) if category == "movie" else TmdbEndpoints.alternative_show(
            movie_id)
        params = {"api_key": self.api_key, "language": self.language}

        data = await self.http.get(url, params=params)

        if not data:
            return None

        if category == "movie":
            titles = [title for t in data.get("titles", []) if (title := Title.from_data(t))]

            return AltTitle(id=data.get("id", 0), titles=titles)
        else:  # series
            results = [Alternative(**r) for r in data.get("results", [])]
            return DataResponse(id=data.get("id", 0), results=results)

    async def videos(self, movie_id: int, category: str) -> Data | None:
        """
        :param movie_id: the movie id
        :param category: serie or movie
        :return:

        Get trailers o associated video
        """
        url = TmdbEndpoints.videos_movie(movie_id) if category == "movie" else TmdbEndpoints.videos_show(movie_id)
        params = {"api_key": self.api_key, "language": self.language}

        data = await self.http.get(url, params=params)

        if not data:
            return None

        results = [Videos(**v) for v in data.get("results", [])]
        return Data(id=data.get("id", 0), results=results)

    async def details(self, video_id: int, category: str) -> MovieDetails | TVShowDetails | None:
        """
        :param video_id: the video id
        :param category: serie or movie
        :return:

        Get details about a movie or serie
        """
        url = TmdbEndpoints.movie_details(video_id) if category == "movie" else TmdbEndpoints.tv_details(video_id)
        params = {"api_key": self.api_key, "language": self.language}

        data = await self.http.get(url, params=params)

        if not data:
            return None

        if category == "movie":
            data["genres"] = [Genre(**g) for g in data.get("genres", [])]
            data["production_companies"] = [ProductionCompany(**c) for c in data.get("production_companies", [])]
            data["production_countries"] = [ProductionCountry(**c) for c in data.get("production_countries", [])]
            data["spoken_languages"] = [SpokenLanguage(**l) for l in data.get("spoken_languages", [])]
            return MovieDetails(**data)

        else:  # tv

            data["genres"] = [Genre(**g) for g in data.get("genres", [])]
            data["created_by"] = [CreatedBy(**c) for c in data.get("created_by", [])]
            data["networks"] = [Network(**n) for n in data.get("networks", [])]
            data["production_companies"] = [ProductionCompany(**p) for p in data.get("production_companies", [])]
            data["production_countries"] = [ProductionCountry(**c) for c in data.get("production_countries", [])]
            data["spoken_languages"] = [SpokenLanguage(**l) for l in data.get("spoken_languages", [])]

            if data.get("last_episode_to_air"):
                data["last_episode_to_air"] = LastEpisodeToAir(**data["last_episode_to_air"])

            if data.get("next_episode_to_air"):
                data["next_episode_to_air"] = LastEpisodeToAir(**data["next_episode_to_air"])

            data["seasons"] = [Season(**s) for s in data.get("seasons", [])]
            return TVShowDetails(**data)

    async def keywords(self, movie_id: int, category: str) -> list[Keyword] | None:
        """
        :param movie_id: the movie id
        :param category: serie or movie
        :return:

        Get the keywords associated with a movie or serie
        """
        url = TmdbEndpoints.movie_keywords(movie_id) if category == "movie" else TmdbEndpoints.tv_keywords(movie_id)
        params = {"api_key": self.api_key, "language": self.language}
        data = await self.http.get(url, params=params)
        if not data:
            return None

        # TMDB restituisce "keywords" per i film, "results" per TV
        if category == "movie":
            items = data.get("keywords", [])
        else:
            items = data.get("results", [])

        return [Keyword(**k) for k in items]

    async def playing(self, category: str) -> list[NowPlaying] | list[OnTheAir] | None:
        """
        :param category: serie or movie
        :return:

         Get the last movie/series
        """
        if category == "movie":
            url = TmdbEndpoints.movie_now_playing()
        elif category == "tv":
            url = TmdbEndpoints.tv_on_the_air()
        else:
            raise ValueError(f"Invalid category: {category}")

        params = {"api_key": self.api_key, "language": self.language}

        data = await self.http.get(url, params=params)

        if not data or "results" not in data:
            return None

        results = []
        if category == "movie":
            for item in data["results"]:
                results.append(NowPlaying(**item))
        else:  # tv
            for item in data["results"]:
                results.append(OnTheAir(**item))

        return results
