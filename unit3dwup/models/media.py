# -*- coding: utf-8 -*-
# based on the old code unit3dup 08.21
from pathlib import Path
import hashlib
import os
import re

from unit3dwup.config.tags import crew_patterns, platform_patterns
from unit3dwup.config.tags import SIGNS_LIST, TAGS_LIST, BAN_LIST
from unit3dwup.config.constants import MediaStatus
from unit3dwup.config.settings import get_settings
from unit3dwup.config.logger import get_logger

from unit3dwup.services.utility import ManageTitles, System
from unit3dwup.services import utility

from unit3dwup.models.media_info import MediaFile

settings = get_settings()


class Media:
    """
    AsyncMediaManager service uses this class to build for each file an object of type Media
    Each Media has a job_id based on its path and filename. Many job_ids make up a job_list
    As the Media object is processed by multiple classes,
    it is gradually built until it is used to create the payload for the tracker
    """

    def __init__(self, folder: str, subfolder: str, torrent_archive_path: str) -> None:
        """
        :param folder: the main path
        :param subfolder: file path or subfolder path
        """
        self.folder: Path = Path(folder)
        self.subfolder: str = subfolder
        self.title: str = (Path(self.folder) / self.subfolder).name
        self._torrent_file_path = Path(torrent_archive_path) / "ITT" / f"{self.title}.torrent"
        self.logger = get_logger(self.__class__.__name__)

        # // Assign a job id
        path = Path(self.folder) / self.subfolder
        self.job_id: str = hashlib.sha256(str(path).encode()).hexdigest()
        # // Media
        self.cached: bool = False  # non utilizzato
        self._crew_list: list[str] | None = None
        self._game_title: str | None = None
        self._platform_list: list[str] | None = None
        self._title_sanitized: str | None = None
        self._guess_title: str | None = None
        self._guess_filename: utility.Guessit | None = None
        self._guess_season: int | None = None
        self._guess_episode: int | None = None
        self._source: str | None = None
        self._screen_size: str | None = None
        self._audio_codec: str | None = None
        self._subtitle: str | None = None
        self._torrent_path: Path | None = None
        self._media_to_string: str | None = None
        self.signs_list: dict[str, str] = SIGNS_LIST
        self.tags_list: dict[str, str] = TAGS_LIST
        self.ban_list: dict[str, str] = BAN_LIST
        self.releaser_sign: str = settings.prefs.RELEASER_SIGN
        self._tag_position: list[str] = []

        # // Contents
        self._file_name: str | None = None
        self._display_name: str | None = None
        self._category: str | None = None
        self._audio_languages: list[str] = []
        self._media_file: MediaFile | None = None
        self._languages: list[str] | None = None
        self._resolution: str | None = None
        self._tracker_name: str | None = None

        # // Contents dall'esterno
        self._torrent_name: str | None = None
        self._size: int = 0
        self._metainfo: str | None = None
        self._torrent_pack: bool = False
        self._doc_description: str | None = None
        self._game_nfo: str | None = None
        self._tmdb_id: int | None = None
        self._imdb_id: int | None = None
        self._tvdb_id: int | None = None
        self._igdb_id: int | None = None
        self._generate_title: str | None = None
        self._keyword: str | None = None
        self._trailer: str | None = None
        self._description: str | None = None
        self._is_hd: int = 0
        self._is_folder: bool = False
        self._extracted_frames: list[bytes] | None = None
        self._backdrop_path: str | None = None
        self._status: int | None = MediaStatus.INDEXED
        self._error: str | None = None
        self._screen_shots: list | None = None
        self._job_id_list: str | None = None
        self._imdb_from_tvdb: str | None = None

    @property
    def title_sanitized(self) -> str:
        if not self._title_sanitized:
            self._title_sanitized = ManageTitles.clean_text(self.title)
        return self._title_sanitized

    @title_sanitized.setter
    def title_sanitized(self, value: str):
        self._title_sanitized = value

    @property
    def crew_list(self) -> list[str]:
        if not self._crew_list:
            self._crew_list = self._crew(filename=self.title_sanitized)
        return self._crew_list

    @property
    def platform_list(self) -> list[str]:
        if not self._platform_list:
            self._platform_list = self._platform(filename=self.title_sanitized)
        return self._platform_list

    @property
    def game_nfo(self) -> str | None:
        return self._game_nfo

    @game_nfo.setter
    def game_nfo(self, value: str | None):
        self._game_nfo = value

    @property
    def game_title(self) -> str | None:
        if not self._game_title:
            _game_tmp = self.guess_filename.guessit_title
            for crew in self.crew_list:
                _game_tmp = _game_tmp.replace(crew, " ")
            self._game_title = _game_tmp.strip()
        return self._game_title

    @property
    def torrent_name(self) -> str | None:
        return self._torrent_name

    @torrent_name.setter
    def torrent_name(self, value: str | None):
        self._torrent_name = value

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int):
        self._size = value

    @property
    def metainfo(self) -> str | None:
        return self._metainfo

    @metainfo.setter
    def metainfo(self, value: str | None):
        self._metainfo = value

    @property
    def doc_description(self) -> str | None:
        return self._doc_description

    @doc_description.setter
    def doc_description(self, value: str | None):
        self._doc_description = value

    @property
    def tracker_name(self) -> str | None:
        return self._tracker_name

    @tracker_name.setter
    def tracker_name(self, value: str | None):
        self._tracker_name = value

    @property
    def torrent_pack(self) -> bool:
        return self._torrent_pack

    @torrent_pack.setter
    def torrent_pack(self, value: bool):
        self._torrent_pack = value

    @property
    def tmdb_id(self) -> int | None:
        return self._tmdb_id

    @tmdb_id.setter
    def tmdb_id(self, value: int | None):
        self._tmdb_id = value

    @property
    def imdb_id(self) -> int | None:
        return self._imdb_id

    @imdb_id.setter
    def imdb_id(self, value: int | None):
        self._imdb_id = value

    @property
    def tvdb_id(self) -> int | None:
        return self._tvdb_id

    @tvdb_id.setter
    def tvdb_id(self, value: int | None):
        self._tvdb_id = value

    @property
    def igdb_id(self) -> int | None:
        return self._igdb_id

    @igdb_id.setter
    def igdb_id(self, value: int | None):
        self._igdb_id = value

    @property
    def generate_title(self) -> str | None:
        if not self._generate_title and self.mediafile:
            video_f = self.mediafile.video_format
            audio_f = self.mediafile.audio_format
            audio_lang = self.mediafile.audio_language
            available_lang = ' '.join(
                lang for lang in self.mediafile.available_languages if lang is not None
            )

            if System.category_list.get(System.TV_SHOW) in self.category:
                serie = f"S{str(self.guess_season).zfill(2)}" if self.guess_season else ''
                if not self.torrent_pack:
                    serie += f"E{str(self.guess_episode).zfill(2)}"
            else:
                serie = ''

            self._generate_title = f"{self.guess_title} {serie} {self.resolution} {video_f} " \
                                   f"{available_lang} {audio_f} {audio_lang.upper()}"
        return self._generate_title

    @generate_title.setter
    def generate_title(self, value: str | None):
        self._generate_title = value

    @property
    def guess_filename(self) -> utility.Guessit:
        if not self._guess_filename:
            self._guess_filename = utility.Guessit(self.title_sanitized)
        return self._guess_filename

    @property
    def file_name(self) -> str | None:
        return self._file_name

    @file_name.setter
    def file_name(self, value: str | None):
        self._file_name = value

    @property
    def display_name(self) -> str | None:
        return self._display_name

    @display_name.setter
    def display_name(self, value: str | None):
        self._display_name = value
        if self._display_name:
            episode_title = self.guess_filename.guessit_episode_title
            if episode_title:
                self._display_name = " ".join(
                    self._display_name.replace(episode_title, "").split()
                )

    @property
    def guess_title(self) -> str:
        if not self._guess_title:
            self._guess_title = self.guess_filename.guessit_title.strip()
        return self._guess_title

    @guess_title.setter
    def guess_title(self, value: str):
        self._guess_title = value

    @property
    def guess_season(self) -> int | None:
        if not self._guess_season and System.category_list.get(System.TV_SHOW) in self.category:
            self._guess_season = int(str(self.guess_filename.guessit_season))
        return self._guess_season

    @property
    def guess_episode(self) -> int | None:
        if not self._guess_episode and System.category_list.get(System.TV_SHOW) in self.category:
            if isinstance(self.guess_filename.guessit_episode, list):
                self._guess_episode = 0
            else:
                if self.guess_filename.guessit_episode:
                    self._guess_episode = int(str(self.guess_filename.guessit_episode))
                else:
                    self._guess_episode = 0
        return self._guess_episode

    @guess_episode.setter
    def guess_episode(self, value):
        self._guess_episode = value

    @guess_season.setter
    def guess_season(self, value):
        self._guess_season = value

    @property
    def source(self) -> str | None:
        if not self._source:
            self._source = self.guess_filename.source
        return self._source

    @property
    def screen_size(self) -> str | None:
        if not self._screen_size:
            for screen in self.title_sanitized.split():
                if screen in System.RESOLUTION_labels:
                    self._screen_size = screen
        return self._screen_size

    @property
    def audio_codec(self) -> str | None:
        if not self._audio_codec:
            self._audio_codec = self.guess_filename.audio_codec
        return self._audio_codec

    @property
    def audio_languages(self):
        if not self._audio_languages:
            # Get languages from the title
            filename_split = self.display_name.upper().split(" ")

            for code in filename_split:
                converted_code = ManageTitles.convert_iso(code)
                if converted_code:
                    self._audio_languages.append(converted_code[0])

            if not self._audio_languages:
                # get from the audio track
                self._audio_languages = self.languages
        return self._audio_languages

    @property
    def subtitle(self) -> str | None:
        if not self._subtitle:
            self._subtitle = self.guess_filename.subtitle
        return self._subtitle

    @property
    def torrent_file_path(self) -> Path:
        return self._torrent_file_path

    @property
    def torrent_path(self) -> Path:
        if not self._torrent_path:
            if os.path.isfile(self.folder):
                self._torrent_path = self.folder
            if os.path.isdir(self.folder):
                self._torrent_path = Path(self.folder) / self.subfolder
        return self._torrent_path

    @property
    def category(self) -> str | None:
        if self._category:
            return self._category

        if ManageTitles.media_docu_type(self.title):
            self._category = System.category_list.get(System.DOCUMENTARY)
        elif self.guess_filename.guessit_season:
            self._category = System.category_list.get(System.TV_SHOW)
        else:
            self._category = System.category_list.get(System.MOVIE)

        if self.crew_list or self.platform_list:
            self._category = System.category_list.get(System.GAME)

        return self._category

    @category.setter
    def category(self, value: str | None):
        self._category = value

    @property
    def tag_position(self) -> list[str]:
        self._tag_position = settings.prefs.TAG_POSITION_SERIE if self.category == 'series' \
            else settings.prefs.TAG_POSITION_MOVIE
        return self._tag_position

    @property
    def keyword(self) -> str | None:
        return self._keyword

    @keyword.setter
    def keyword(self, value: str | None):
        self._keyword = value

    @property
    def trailer(self) -> str | None:
        return self._trailer

    @trailer.setter
    def trailer(self, value: str | None):
        self._trailer = value

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None):
        self._description = value

    @property
    def extracted_frames(self) -> list[bytes] | None:
        return self._extracted_frames

    @extracted_frames.setter
    def extracted_frames(self, value: list[bytes] | None):
        self._extracted_frames = value

    @property
    def is_hd(self) -> int:
        return self._is_hd

    @is_hd.setter
    def is_hd(self, value: int):
        self._is_hd = value

    @property
    def mediafile(self) -> MediaFile | None:
        return self._media_file

    @mediafile.setter
    def mediafile(self, value: MediaFile | None):
        self._media_file = value

    @property
    def media_to_string(self) -> str | None:
        return self._media_to_string

    @media_to_string.setter
    def media_to_string(self, value: str | None):
        self._media_to_string = value

    @property
    def backdrop_path(self) -> str | None:
        return self._backdrop_path

    @backdrop_path.setter
    def backdrop_path(self, value: str | None):
        self._backdrop_path = value

    @property
    def status(self) -> int | None:
        return self._status

    @status.setter
    def status(self, value: int | None):
        self._status = value

    @property
    def error(self) -> str | None:
        return self._error

    @error.setter
    def error(self, value: str | None):
        self._error = value

    @property
    def is_folder(self) -> bool:
        return self._is_folder

    @is_folder.setter
    def is_folder(self, value: bool):
        self._is_folder = value

    @property
    def screen_shots(self) -> list[str]:
        return self._screen_shots

    @screen_shots.setter
    def screen_shots(self, value: list[str]):
        self._screen_shots = value or []

    def add_screen_shot(self, value: str):
        self._screen_shots.append(value)

    @property
    def job_id_list(self) -> str | None:
        return self._job_id_list

    @job_id_list.setter
    def job_id_list(self, value: str):
        self._job_id_list = value

    @property
    def imdb_id_from_tvdb(self) -> str:
        return self._imdb_from_tvdb

    @imdb_id_from_tvdb.setter
    def imdb_id_from_tvdb(self, value: str):
        self._imdb_from_tvdb = value

    @property
    def languages(self) -> list[str]:
        if not self._languages and self.mediafile:
            self._languages = self.mediafile.available_languages
        return self._languages

    @property
    def detected_resolution(self):
        if not self.mediafile or not self.mediafile.video_width:
            return None

        width = int(self.mediafile.video_width)

        for limit, label in (
                (3200, "2160p"),
                (1600, "1080p"),
                (1100, "720p"),
                (960, "576p"),
        ):
            if width >= limit:
                return label

        return f"{self.mediafile.video_height}p"

    @property
    def resolution(self):
        if self._resolution:
            return self._resolution

        if not self.mediafile:
            self._resolution = System.NO_RESOLUTION
            return self._resolution

        detected = self.detected_resolution

        if detected:
            self._resolution = detected
        else:
            self.logger.warning(f"{self.__class__.__name__}: video resolution not found in {self.file_name}")
            self._resolution = System.NO_RESOLUTION
        return self._resolution

    @staticmethod
    def _crew(filename: str) -> list[str]:
        regex = r"\b(" + "|".join(re.escape(p) for p in crew_patterns) + r")\b$"
        return re.findall(regex, filename, re.IGNORECASE)

    @staticmethod
    def _platform(filename: str) -> list[str]:
        regex = r"\b(" + "|".join(re.escape(p) for p in platform_patterns) + r")\b"
        return re.findall(regex, filename, re.IGNORECASE)

    # Serialize
    def to_dict(self) -> dict:

        # /// PosixPath objects must be converted to strings to be serializable
        return {
            "folder": str(self.folder),
            "subfolder": self.subfolder,
            "title": self.title,
            "job_id": self.job_id,
            "status": self.status,
            "error": self.error,
            "title_sanitized": self.title_sanitized,
            "guess_title": self.guess_title,
            "generate_title": self.generate_title,
            "category": self.category,
            "backdrop_path": self.backdrop_path,
            "media_to_string": self.media_to_string,
            "description": self.description,
            "mediafile": self.mediafile.to_dict() if self.mediafile else None,
            "tmdb_id": self.tmdb_id,
            "imdb_id": self.imdb_id,
            "tvdb_id": self.tvdb_id,
            "igdb_id": self.igdb_id,
            "imdb_id_from_tvdb": self.imdb_id_from_tvdb,
            "file_name": str(self.file_name),
            "display_name": self.display_name,
            "torrent_name": self.torrent_name,
            "torrent_path": str(self.torrent_path),
            "torrent_file_path": str(self.torrent_file_path),
            "torrent_pack": self.torrent_pack,
            "size": self.size,
            "resolution": self.resolution,
            "screen_size": self.screen_size,
            "source": self.source,
            "audio_codec": self.audio_codec,
            "audio_languages": self.audio_languages,
            "subtitle": self.subtitle,
            "crew_list": self.crew_list,
            "platform_list": self.platform_list,
            "screen_shots": self.screen_shots,
            "job_id_list": self.job_id_list,

        }

    @classmethod
    # json to Media()
    def from_dict(cls, data: dict) -> "Media":
        torrent_archive_path = (
            Path("/home/app/torrent_archive") if os.getenv("DOCKER") == "true"
            else Path(settings.prefs.TORRENT_ARCHIVE_PATH)
        )

        m = cls(folder=data["folder"], subfolder=data["subfolder"], torrent_archive_path=str(torrent_archive_path))
        m.file_name = data.get("file_name")
        m.display_name = data.get("display_name")
        m.torrent_name = data.get("torrent_name")
        m.size = data.get("size", 0)  # todo fare cast to int
        m.torrent_pack = data.get("torrent_pack", False)
        m.job_id = data.get("job_id")
        m.status = int(data.get("status", 0))
        m.error = data.get("error")
        m.tmdb_id = data.get("tmdb_id")
        m.imdb_id = data.get("imdb_id")
        m.tvdb_id = data.get("tvdb_id")
        m.igdb_id = data.get("igdb_id")
        m.imdb_id_from_tvdb = data.get("imdb_id_from_tvdb")
        m.backdrop_path = data.get("backdrop_path")
        m.media_to_string = data.get("media_to_string")
        m.description = data.get("description")
        if data.get("mediafile"):
            m.mediafile = MediaFile.dict_to_mediafile(data["mediafile"])
        m.generate_title = data.get("generate_title")
        m.category = data.get("category")
        m.screen_shots = data.get("screen_shots")
        m.job_id_list = data.get("job_id_list")
        return m
