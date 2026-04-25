# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from models.interfaces import MediaRepoInterface


# slots, non avendo la necessità di aggiungere nuovi attributi al volo
@dataclass(slots=True)
class TvdbRemoteID:
    id: str
    sourceName: str
    type: int


@dataclass(slots=True)
class TvdbSearchResult(MediaRepoInterface):
    """
        Dataclass for manage result from a TVDB search
        TMDB e TVDB share the same interface
    """
    id: str
    tvdb_id: str
    name: str
    extended_title: str | None
    slug: str | None
    type: str
    primary_type: str
    status: str | None
    year: str | None
    first_air_time: str | None
    country: str | None
    primary_language: str | None
    director: str | None  # for movies

    studios: list[str] = field(default_factory=list)
    genres: list[str] = field(default_factory=list)

    overview: str | None = None
    overviews: dict[str, str] = field(default_factory=dict)
    translations: dict[str, str] = field(default_factory=dict)

    image_url: str | None = None
    thumbnail: str | None = None

    # for imdb id
    remote_ids: list[TvdbRemoteID] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> TvdbSearchResult:
        remote_ids = [TvdbRemoteID(**r) for r in item.get("remote_ids", [])]

        return cls(
            id=item.get("id", ""),
            tvdb_id=item.get("tvdb_id", "0"),
            name=item.get("name", ""),
            extended_title=item.get("extended_title"),
            slug=item.get("slug"),
            type=item.get("type", ""),
            primary_type=item.get("primary_type", ""),
            status=item.get("status"),
            year=item.get("year"),
            first_air_time=item.get("first_air_time"),
            country=item.get("country"),
            primary_language=item.get("primary_language"),
            director=item.get("director"),
            studios=item.get("studios", []),
            genres=item.get("genres", []),
            overview=item.get("overview"),
            overviews=item.get("overviews", {}),
            translations=item.get("translations", {}),
            image_url=item.get("image_url"),
            thumbnail=item.get("thumbnail"),
            remote_ids=remote_ids,
        )

    def get_title(self) -> str:
        return self.name

    def get_original(self) -> str:
        return self.extended_title or self.name

    def get_date(self) -> str:
        return self.first_air_time or ""

    def get_id(self) -> int:
        try:
            return int(self.tvdb_id)
        except ValueError:
            return 0

    def get_poster_path(self) -> str:
        return self.image_url or ""

    def get_imdb(self) -> str | None:
        for r in self.remote_ids:
            if 'IMDB' in r.sourceName.upper():
                return r.id.lower().replace('tt', '')
        return None

    def get_translations(self) -> dict[str, str] | None:
        return self.translations
