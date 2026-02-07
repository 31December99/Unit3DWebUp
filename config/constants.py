# -*- coding: utf-8 -*-
from enum import IntEnum

class MediaStatus(IntEnum):
    """
    It tracks the status during the creation of a media file
    """
    INDEXED = 0

    # Searching tmdb,tvdb,imdb
    DB_IDENTIFIED = 1
    DB_NOT_IDENTIFIED = 10
    DB_ERROR = 11

    # When extracting the screenshots from the video file
    VIDEO_READY = 2
    VIDEO_ERROR = 20

    # When uploading raw data to the image host
    DESCRIPTION_READY = 3
    DESCRIPTION_ERROR = 30

    # When generating the torrent file *.torrent
    TORRENT_GENERATED = 4
    TORRENT_ERROR = 40

    # When uploading torrent files to the tracker
    TRACKER_UPLOADED = 5
    TRACKER_NOT_UPLOADED = 50

    # When seeding one or more torrent files
    TORRENT_SEED = 7
    TORRENT_SEED_ERROR = 70
