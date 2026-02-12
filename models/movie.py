# -*- coding: utf-8 -*-
from __future__ import annotations

# Same as the old code unit3dup 0.8.21. Add annotations
import json
from dataclasses import dataclass, field
from typing import Any

from config.logger import get_logger
from models.interfaces import MediaRepoInterface


@dataclass(slots=True)
class Title:
    """
         Dataclass for manage result from a TMDB search
    """
    iso_3166_1: str
    title: str
    type: str | None = None

    @staticmethod
    def from_data(data: dict[str, any]) -> Title | None:
        try:
            return Title(
                iso_3166_1=data["iso_3166_1"],
                title=data["title"],
                type=data.get("type"),
            )
        except KeyError as e:
            print(f"Missing key in Title data: {e}")
            return None
        except TypeError as e:
            print(f"Type error in Title data: {e}")
            return None


@dataclass(slots=True)
class AltTitle:
    id: int
    titles: list[Title]

    @classmethod
    def validate(cls, json_str: str) -> AltTitle:
        data = json.loads(json_str)
        id_ = data.get("id", 0)
        titles_data = data.get("titles", [])
        titles = [
            Title.from_data(title_data)
            for title_data in titles_data
            if Title.from_data(title_data) is not None
        ]
        return cls(id=id_, titles=titles)


@dataclass(slots=True)
class Genre:
    id: int
    name: str


@dataclass(slots=True)
class ProductionCompany:
    id: int
    logo_path: str | None
    name: str
    origin_country: str


@dataclass(slots=True)
class ProductionCountry:
    iso_3166_1: str
    name: str


@dataclass(slots=True)
class SpokenLanguage:
    english_name: str
    iso_639_1: str
    name: str


@dataclass(slots=True)
class MovieDetails(MediaRepoInterface):
    adult: bool
    backdrop_path: str | None
    belongs_to_collection: str | None
    budget: int
    genres: list[Genre]
    homepage: str
    id: int
    imdb_id: str
    origin_country: list[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str | None
    production_companies: list[ProductionCompany]
    production_countries: list[ProductionCountry]
    release_date: str
    revenue: int
    runtime: int
    spoken_languages: list[SpokenLanguage]
    status: str
    tagline: str
    title: str
    video: bool
    vote_average: float
    vote_count: int

    def get_title(self) -> str:
        return self.title

    def get_original(self) -> str:
        return self.original_title

    def get_date(self) -> str:
        return self.release_date

    def get_id(self) -> int:
        return self.id

    def get_translations(self) -> dict[str, str] | None:
        pass

    def get_imdb(self) -> str | None:
        pass

    def get_poster_path(self) -> str:
        pass


@dataclass(slots=True)
class NowPlaying:
    """
    Represents Nowplaying attributes
    """
    adult: bool | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] = field(default_factory=list)
    id: int | None = None
    original_language: str | None = None
    original_title: str | None = None
    overview: str | None = None
    popularity: float | None = None
    poster_path: str | None = None
    release_date: str | None = None
    title: str | None = None
    video: bool | None = None
    vote_average: float | None = None
    vote_count: int | None = None

    def __repr__(self):
        """Returns a string """
        return f"<Movie title={self.title} id={self.id}>"


@dataclass(slots=True)
class NowPlayingByCountry(NowPlaying):
    """
    Represents a combined movie object NowPlayIng by Country code
    """
    iso_3166_1: str | None = None
    release_dates: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self):
        """Validate data """
        if self.iso_3166_1 and (len(self.iso_3166_1) != 2 or not self.iso_3166_1.isalpha()):
            self.iso_3166_1 = None

    @staticmethod
    def from_data(now_playing: NowPlaying, release_info: MovieReleaseInfo) -> NowPlayingByCountry:
        """
        Creates a NowPlayingByCountry instance from NowPlaying and MovieReleaseInfo instances
        """
        return NowPlayingByCountry(
            adult=now_playing.adult,
            backdrop_path=now_playing.backdrop_path,
            genre_ids=now_playing.genre_ids,
            id=now_playing.id,
            original_language=now_playing.original_language,
            original_title=now_playing.original_title,
            overview=now_playing.overview,
            popularity=now_playing.popularity,
            poster_path=now_playing.poster_path,
            release_date=now_playing.release_date,
            title=now_playing.title,
            video=now_playing.video,
            vote_average=now_playing.vote_average,
            vote_count=now_playing.vote_count,
            iso_3166_1=release_info.iso_3166_1,
            release_dates=release_info.release_dates,
        )


@dataclass(slots=True)
class Movie(MediaRepoInterface):
    """
    A movie object for the search endpoint
    """
    adult: bool = False
    backdrop_path: str = ''
    genre_ids: list[int] = field(default_factory=list)
    id: int = 0
    original_language: str = ''
    original_title: str = ''
    overview: str = ''
    popularity: float = 0.0
    poster_path: str = ''
    release_date: str = ''
    title: str = ''
    video: bool = False
    vote_average: float = 0.0
    vote_count: int = 0

    def get_title(self) -> str:
        return self.title

    def get_original(self) -> str:
        return self.original_title

    def get_date(self) -> str:
        return self.release_date

    def get_id(self) -> int:
        return self.id

    def get_poster_path(self) -> str:
        return self.poster_path

    def get_imdb(self) -> str | None:
        # Get remote ids (IMDB) only from tvdb
        pass

    def get_translations(self) -> list[str] | None:
        # Get translations list only from tvdb
        pass


@dataclass(slots=True)
class MovieReleaseInfo:
    """
    Represents release information for a movie in a specific country.
    """

    iso_3166_1: str | None = None
    release_dates: list[dict[str, Any]] = field(default_factory=list)

    def __repr__(self) -> str:
        """
        Returns the MovieReleaseInfo string
        """
        return f"<ReleaseInfo iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"

    @classmethod
    def validate(cls, data: dict) -> MovieReleaseInfo | None:
        """
        Validates the data; return None if it's invalid
        """

        iso_3166_1 = data.get("iso_3166_1")
        release_dates = data.get("release_dates", {})
        logger = get_logger(cls.__name__)

        # Validate country code
        if iso_3166_1 is not None:
            if (
                    not isinstance(iso_3166_1, str)
                    or len(iso_3166_1) != 2
                    or not iso_3166_1.isupper()
            ):
                logger.error(f"Invalid ISO 3166-1 code: {iso_3166_1}")
                return None

            # Validate release_dates
        if not isinstance(release_dates, list):
            logger.error("release_dates must be a list.")
            return None

        for item in release_dates:
            if not isinstance(item, dict):
                logger.error(f"Invalid item in release_dates list: {item}")
                return None

        return cls(iso_3166_1=iso_3166_1, release_dates=release_dates)
