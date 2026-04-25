# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


# Tempus fugit
# Based on the old code unit3dup 0.8.21
class MediaRepoInterface(ABC):
    """
        interface to get an attribute independently of the repository type (TMDB, TVDB)
    """

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_original(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_poster_path(self) -> str:
        pass

    @abstractmethod
    def get_imdb(self) -> str | None:
        pass

    @abstractmethod
    def get_translations(self) -> dict[str, str] | None:
        pass
