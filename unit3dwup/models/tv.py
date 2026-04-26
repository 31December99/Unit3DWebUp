# -*- coding: utf-8 -*-

# Same as the old code unit3dup 0.8.21
from dataclasses import dataclass, field
from unit3dwup.models.interfaces import MediaRepoInterface


@dataclass(slots=True)
class Alternative:
    iso_3166_1: str
    title: str
    type: str


@dataclass(slots=True)
class DataResponse:
    id: int
    results: list[Alternative]


@dataclass(slots=True)
class CreatedBy:
    credit_id: str
    gender: int
    id: int
    name: str
    original_name: str
    profile_path: str | None = None


@dataclass(slots=True)
class Genre:
    id: int
    name: str


@dataclass(slots=True)
class LastEpisodeToAir:
    air_date: str
    episode_number: int
    episode_type: str
    id: int
    name: str
    overview: str
    production_code: str
    runtime: int
    season_number: int
    show_id: int
    vote_average: float
    vote_count: int
    still_path: str | None = None


@dataclass(slots=True)
class Network:
    id: int
    logo_path: str
    name: str
    origin_country: str


@dataclass(slots=True)
class ProductionCompany:
    id: int
    name: str
    origin_country: str
    logo_path: str | None = None


@dataclass(slots=True)
class ProductionCountry:
    iso_3166_1: str
    name: str


@dataclass(slots=True)
class Season:
    episode_count: int
    id: int
    name: str
    overview: str
    season_number: int
    vote_average: float
    air_date: str | None = None
    poster_path: str | None = None


@dataclass(slots=True)
class SpokenLanguage:
    english_name: str
    iso_639_1: str
    name: str


@dataclass(slots=True)
class TVShowDetails(MediaRepoInterface):

    adult: bool
    first_air_date: str
    homepage: str
    id: int
    in_production: bool
    last_air_date: str
    last_episode_to_air: LastEpisodeToAir
    name: str
    number_of_episodes: int
    number_of_seasons: int
    original_language: str
    original_name: str
    overview: str
    popularity: float
    poster_path: str
    status: str
    tagline: str
    type: str
    vote_average: float
    vote_count: int
    languages: list[str] = field(default_factory=list)
    genres: list[Genre] = field(default_factory=list)
    backdrop_path: str | None = None
    created_by: list[CreatedBy] = field(default_factory=list)
    episode_run_time: list[int] = field(default_factory=list)
    networks: list[Network] = field(default_factory=list)
    next_episode_to_air: LastEpisodeToAir | None = None
    production_companies: list[ProductionCompany] = field(default_factory=list)
    production_countries: list[ProductionCountry] = field(default_factory=list)
    seasons: list[Season] = field(default_factory=list)
    spoken_languages: list[SpokenLanguage] = field(default_factory=list)
    origin_country: list[str] = field(default_factory=list)


    def get_title(self) -> str:
        return self.name

    def get_original(self) -> str:
        return self.original_name

    def get_date(self) -> str:
        return self.first_air_date

    def get_id(self) -> int:
        return self.id

    def get_translations(self) -> dict[str, str] | None:
        pass

    def get_imdb(self) -> str | None:
        pass

    def get_poster_path(self) -> str:
        pass


@dataclass(slots=True)
class OnTheAir:
    adult: bool | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] | None = None
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
    origin_country: list[str] | None = None
    original_name: str | None = None
    first_air_date: str | None = None
    name: str | None = None


@dataclass(slots=True)
class Translation:
    """
    Represents a TV show translation
    """
    iso_639_1: str
    """
    Language code of the translation
    """
    english_name: str
    """
    English name of the language
    """
    name: str
    """
    Name of the translation
    """
    url: str | None
    """
    Optional URL associated with the translation
    """
    tagline: str | None
    """
    Optional tagline for the translation
    """
    description: str | None
    """
    Optional description for the translation
    """
    country: str | None
    """
    Optional country code related to the translation
    """


@dataclass(slots=True)
class TranslationsResponse:
    """
    Contains a list of TV show translations
    """
    translations: list[Translation]
    """
    List of Translation objects
    """


@dataclass(slots=True)
class TvShow(MediaRepoInterface):
    """
     Dataclass for manage result from a TMDB search
    """

    id: int
    name: str
    first_air_date: str
    overview: str
    popularity: float
    vote_average: float
    vote_count: int
    genre_ids: list[int] = field(default_factory=list)
    origin_country: list[str] = field(default_factory=list)
    original_language: str = ''
    original_name: str = ''
    backdrop_path: str | None = None
    poster_path: str | None = None
    adult: bool = False
    softcore: str | None = None


    def get_title(self) -> str:
        return self.name

    def get_original(self) -> str:
        return self.original_name

    def get_date(self) -> str:
        return self.first_air_date

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
