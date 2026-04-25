# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(slots=True)
class Videos:
    """
     Dataclass for manage result from a TMDB search : Trailers
    """
    id: str
    iso_3166_1: str
    iso_639_1: str
    key: str
    name: str
    official: bool
    published_at: str
    site: str
    size: int
    type: str


@dataclass(slots=True)
class Data:
    id: int
    results: list[Videos]
