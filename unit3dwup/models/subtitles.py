# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class SubtitleTrack:
    track_id: int
    language: str
    title: str
    default: bool
    forced: bool


@dataclass
class SubtitleInfo:
    total: int
    tracks: list[SubtitleTrack]