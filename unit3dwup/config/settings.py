# -*- coding: utf-8 -*-
import os
from functools import lru_cache
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, field_validator, model_validator, HttpUrl, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from unit3dwup.config.logger import get_logger


# /// Class to help avoid typos...
class TorrentClient(str, Enum):
    qbittorrent = "qbittorrent"
    transmission = "transmission"
    rtorrent = "rtorrent"


# /// Check for missing value
class BaseConfigModel(BaseModel):

    @field_validator("*", mode="before")
    @classmethod
    def empty_to_none(cls, v):
        if v == "":
            return None
        return v


# /// TRACKER CONFIG
class TrackerConfig(BaseConfigModel):
    ITT_URL: HttpUrl
    ITT_APIKEY: str = None
    ITT_PID: str | None = None
    SIS_URL: HttpUrl
    SIS_APIKEY: str | None = None
    SIS_PID: str | None = None
    MULTI_TRACKER: list[str]
    TMDB_APIKEY: str = None
    TVDB_APIKEY: str = None
    IMGBB_KEY: str = None
    FREE_IMAGE_KEY: str | None = None
    LENSDUMP_KEY: str | None = None
    PTSCREENS_KEY: str | None = None
    IMGFI_KEY: str | None = None
    PASSIMA_KEY: str | None = None
    IMARIDE_KEY: str | None = None
    YOUTUBE_KEY: str | None = None
    IGDB_CLIENT_ID: str | None = None
    IGDB_ID_SECRET: str | None = None

    @field_validator("MULTI_TRACKER", mode="before")
    @classmethod
    def parse_multi_tracker(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v

    @field_validator("*")
    @classmethod
    def validate_api_keys(cls, v, info):
        if info.field_name.endswith("_KEY") or "APIKEY" in info.field_name:
            if v is not None and len(v) < 5:
                raise ValueError(f"{info.field_name} too short")
        return v


# /// TORRENT CLIENT CONFIG
class TorrentClientConfig(BaseConfigModel):
    # Default value when the variable is commented out
    QBIT_USER: str = "admin"
    QBIT_PASS: str = "admin"
    QBIT_HOST: str = "http://127.0.0.1"
    QBIT_PORT: int = 8080
    SHARED_QBIT_PATH: str = "/tmp"

    TRASM_USER: str = "admin"
    TRASM_PASS: str = "admin"
    TRASM_HOST: str = "http://127.0.0.1"
    TRASM_PORT: int = 9091
    SHARED_TRASM_PATH: str = "/tmp"

    RTORR_USER: str = "admin"
    RTORR_PASS: str = "admin"
    RTORR_HOST: str = "http://127.0.0.1"
    RTORR_PORT: int = 5000
    SHARED_RTORR_PATH: str = "/tmp"

    TORRENT_CLIENT: TorrentClient = "qbittorrent"
    TAG: str = "TAG1"

    @field_validator("QBIT_PORT", "TRASM_PORT", "RTORR_PORT")
    @classmethod
    def validate_ports(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("invalid port range")
        return v

    @model_validator(mode="after")
    def validate_selected_client(self):
        if self.TORRENT_CLIENT == TorrentClient.qbittorrent:
            if not self.QBIT_HOST:
                raise ValueError("qbittorrent selected but no host has been configured")
        if self.TORRENT_CLIENT == TorrentClient.transmission:
            if not self.TRASM_HOST:
                raise ValueError("transmission selected but no host has been configured")
        if self.TORRENT_CLIENT == TorrentClient.rtorrent:
            if not self.RTORR_HOST:
                raise ValueError("rtorrent selected but no host has been configured")
        return self


# /// USER PREFERENCES
class UserPreferences(BaseConfigModel):
    RELEASER_SIGN: str = ""
    TAG_POSITION_MOVIE: list[str]
    TAG_POSITION_SERIE: list[str]
    PTSCREENS_PRIORITY: int = 0
    LENSDUMP_PRIORITY: int = 1
    FREE_IMAGE_PRIORITY: int = 2
    IMGBB_PRIORITY: int = 3
    IMGFI_PRIORITY: int = 4
    PASSIMA_PRIORITY: int = 5
    IMARIDE_PRIORITY: int = 6

    NUMBER_OF_SCREENSHOTS: int = 4
    YOUTUBE_CHANNEL_ENABLE: bool = False
    DUPLICATE_ON: bool = False  # Todo Not yet implemented
    SKIP_DUPLICATE: bool = False  #
    SKIP_YOUTUBE: bool = False
    SIZE_TH: int = 50
    WATCHER_INTERVAL: int = 60
    WATCHER_PATH: str | None = None
    WATCHER_DESTINATION_PATH: str | None = None
    TORRENT_ARCHIVE_PATH: str = None
    SCAN_PATH: str = None
    COMPRESS_SCSHOT: int = 4
    TORRENT_COMMENT: str | None = "no_comment"
    PREFERRED_LANG: str | None = "all"
    ANON: bool = False
    WEBP_ENABLED: bool = False
    PERSONAL_RELEASE: bool = False
    FAST_LOAD: int = 0

    @field_validator("WATCHER_INTERVAL")
    @classmethod
    def validate_interval(cls, v):
        if v < 5:
            raise ValueError("WATCHER_INTERVAL too low")
        return v

    @field_validator("TAG_POSITION_MOVIE", "TAG_POSITION_SERIE", mode="before")
    @classmethod
    def parse_tag_position(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


# /// APP SETTINGS
class Settings(BaseSettings):
    """
    Set default settings
    """
    tracker: TrackerConfig = Field(default_factory=TrackerConfig)
    torrent: TorrentClientConfig = Field(default_factory=TorrentClientConfig)
    prefs: UserPreferences = Field(default_factory=UserPreferences)

    # enable storing the .env file outside site_packages or project folder
    env_path: str | None = os.getenv("ENVPATH")
    ENV_FILE: str = str(Path(env_path) / ".env") if env_path else ".env"

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=ENV_FILE if not os.getenv("DOCKER") else None,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    :return: settings cached
    """
    logger = get_logger("settings_logger")

    try:
        settings = Settings()
    except ValidationError as e:
        for err in e.errors():
            field_path = ".".join(str(loc) for loc in err["loc"])
            logger.warning(f"{field_path} value not set or invalid")
            logger.warning("-" * 50)

        raise SystemExit(1)

    # Create a folder for each tracker name in the MULTI_TRACKER environment variable
    torrent_archive_path = Path("/home/app/torrent_archive") if os.getenv("DOCKER") == "true" else Path(
        settings.prefs.TORRENT_ARCHIVE_PATH)
    if not Path.exists(torrent_archive_path):
        logger.warning(f"The path {torrent_archive_path} does not exist")
        raise SystemExit(1)

    for tracker_name in settings.tracker.MULTI_TRACKER:
        torrent_archive_tracker_path = Path(torrent_archive_path) / tracker_name.upper()
        os.makedirs(torrent_archive_tracker_path, exist_ok=True)

    return settings
