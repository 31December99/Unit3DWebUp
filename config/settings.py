# -*- coding: utf-8 -*-
from functools import lru_cache
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, field_validator, model_validator, HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    ITT_APIKEY: str | None = None
    ITT_PID: str | None = None
    SIS_URL: HttpUrl
    SIS_APIKEY: str | None = None
    SIS_PID: str | None = None
    MULTI_TRACKER: list[str] | None = None
    TMDB_APIKEY: str | None = None
    TVDB_APIKEY: str | None = None
    IMGBB_KEY: str | None = None
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
    QBIT_USER: str | None = None
    QBIT_PASS: str | None = None
    QBIT_HOST: str = "http://localhost"
    QBIT_PORT: int = 8080
    SHARED_QBIT_PATH: str | None = None

    TRASM_USER: str | None = None
    TRASM_PASS: str | None = None
    TRASM_HOST: str = "http://localhost"
    TRASM_PORT: int = 9091
    SHARED_TRASM_PATH: str | None = None

    RTORR_USER: str | None = None
    RTORR_PASS: str | None = None
    RTORR_HOST: str = "scgi://localhost"
    RTORR_PORT: int = 5000
    SHARED_RTORR_PATH: str | None = None

    TORRENT_CLIENT: TorrentClient | None = None
    TAG: str | None = None

    @field_validator("QBIT_PORT", "TRASM_PORT", "RTORR_PORT")
    @classmethod
    def validate_ports(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("invalid port range")
        return v

    @field_validator(
        "SHARED_QBIT_PATH",
        "SHARED_TRASM_PATH",
        "SHARED_RTORR_PATH",
        mode="before"
    )
    @classmethod
    def validate_paths(cls, v):
        if v is None:
            return v
        p = Path(v)
        if not p.is_absolute():
            raise ValueError("path must be absolute")
        return str(p)

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
    PTSCREENS_PRIORITY: int = 0
    LENSDUMP_PRIORITY: int = 1
    FREE_IMAGE_PRIORITY: int = 2
    IMGBB_PRIORITY: int = 3
    IMGFI_PRIORITY: int = 4
    PASSIMA_PRIORITY: int = 5
    IMARIDE_PRIORITY: int = 6

    NUMBER_OF_SCREENSHOTS: int = 4
    YOUTUBE_FAV_CHANNEL_ID: str | None = None
    YOUTUBE_CHANNEL_ENABLE: bool = False
    DUPLICATE_ON: bool = False
    SKIP_DUPLICATE: bool = False
    SKIP_TMDB: bool = False
    SKIP_YOUTUBE: bool = False
    SIZE_TH: int = 50
    WATCHER_INTERVAL: int = 60
    WATCHER_PATH: str | None = None
    WATCHER_DESTINATION_PATH: str | None = None
    TORRENT_ARCHIVE_PATH: str | None = None
    SCAN_PATH: str | None = None
    CACHE_PATH: str | None = None
    COMPRESS_SCSHOT: int = 4
    RESIZE_SCSHOT: bool = False
    TORRENT_COMMENT: str | None = "no_comment"
    PREFERRED_LANG: str | None = "all"
    ANON: bool = False
    WEBP_ENABLED: bool = False
    CACHE_SCR: bool = False
    CACHE_DBONLINE: bool = False
    PERSONAL_RELEASE: bool = False
    FAST_LOAD: int = 0

    @field_validator(
        "WATCHER_PATH",
        "WATCHER_DESTINATION_PATH",
        "TORRENT_ARCHIVE_PATH",
        "CACHE_PATH",
        "SCAN_PATH",
        mode="before"
    )
    @classmethod
    def validate_paths(cls, v):
        if v is None:
            return v
        p = Path(v)
        if not p.is_absolute():
            # Convert relative paths to absolute paths
            p = Path.cwd() / p
        return str(p)

    @field_validator("WATCHER_INTERVAL")
    @classmethod
    def validate_interval(cls, v):
        if v < 5:
            raise ValueError("WATCHER_INTERVAL too low")
        return v


# /// APP SETTINGS
class Settings(BaseSettings):
    """
    Set default settings
    """
    tracker: TrackerConfig = Field(default_factory=TrackerConfig)
    torrent: TorrentClientConfig = Field(default_factory=TorrentClientConfig)
    prefs: UserPreferences = Field(default_factory=UserPreferences)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    :return: settings cached
    """
    return Settings()
