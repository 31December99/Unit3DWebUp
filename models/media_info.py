# -*- coding: utf-8 -*-
from __future__ import annotations

# Based on the old code unit3dup 0.8.21
import re, os
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass(slots=True)
class MediaFile:
    """
        Try to create a dataclass for the MediaInfo result
        Many of these data need to be sent to the tracker
    """
    file_path: str
    media_to_string: str | None = None
    video_tracks: List[Dict] = field(default_factory=list)
    audio_tracks: List[Dict] = field(default_factory=list)
    general_track: Dict = field(default_factory=dict)

    @property
    def media_description(self) -> str:
        return self.media_to_string

    # --------- VIDEO ---------
    @property
    def codec_id(self) -> str:
        return self.video_tracks[0].get("codec_id", "Unknown") if self.video_tracks else "Unknown"

    @property
    def video_width(self) -> str:
        return self.video_tracks[0].get("width", "Unknown") if self.video_tracks else "Unknown"

    @property
    def video_height(self) -> Optional[str]:
        return self.video_tracks[0].get("height") if self.video_tracks else None

    @property
    def video_scan_type(self) -> Optional[str]:
        return self.video_tracks[0].get("scan_type") if self.video_tracks else None

    @property
    def video_aspect_ratio(self) -> str:
        return self.video_tracks[0].get("display_aspect_ratio", "Unknown") if self.video_tracks else "Unknown"

    @property
    def video_frame_rate(self) -> str:
        return self.video_tracks[0].get("frame_rate", "Unknown") if self.video_tracks else "Unknown"

    @property
    def video_bit_depth(self) -> str:
        return self.video_tracks[0].get("bit_depth", "Unknown") if self.video_tracks else "Unknown"

    @property
    def video_format(self) -> str:
        return self.video_tracks[0].get("format", "Unknown") if self.video_tracks else "Unknown"

    # --------- AUDIO ---------
    @property
    def audio_codec_id(self) -> str:
        return self.audio_tracks[0].get("codec_id", "Unknown") if self.audio_tracks else "Unknown"

    @property
    def audio_bit_rate(self) -> str:
        return self.audio_tracks[0].get("bit_rate", "Unknown") if self.audio_tracks else "Unknown"

    @property
    def audio_channels(self) -> str:
        return self.audio_tracks[0].get("channels", "Unknown") if self.audio_tracks else "Unknown"

    @property
    def audio_sampling_rate(self) -> str:
        return self.audio_tracks[0].get("sampling_rate", "Unknown") if self.audio_tracks else "Unknown"

    @property
    def audio_format(self) -> str:
        return self.audio_tracks[0].get("format", "Unknown") if self.audio_tracks else "Unknown"

    @property
    def audio_language(self) -> str:
        return self.audio_tracks[0].get("language", "Unknown") if self.audio_tracks else "Unknown"

    @property
    def subtitle_tracks(self) -> List[Dict]:
        return [t for t in self.video_tracks if t.get("track_type") == "Text"]

    @property
    def available_languages(self) -> List[str]:
        langs = {
            t.get("language")
            for t in (self.audio_tracks + self.subtitle_tracks)
            if t.get("language")
        }
        return list(langs) or ["not found"]

    @property
    def file_size(self) -> str:
        return self.general_track.get("file_size", "Unknown")

    @property
    def is_interlaced(self) -> Optional[int]:
        encoding = self.video_tracks[0].get("encoding_settings") if self.video_tracks else None
        if not encoding:
            return None
        match = re.search(r"interlaced=(\d)", encoding)
        return int(match.group(1)) if match else None

    def generate_release_name(self, guess_title: str, resolution: str) -> Optional[str]:
        if not self.video_tracks:
            return None

        video_format = self.video_tracks[0].get("format", "")
        audio_format = self.audio_tracks[0].get("format", "")
        _, ext = os.path.splitext(self.file_path)

        return f"{guess_title}.web-dl.{video_format}.{resolution}.{audio_format}{ext}".lower()

    def to_dict(self) -> Dict:
        return {
            "file_path": self.file_path,
            "media_to_string": self.media_to_string,
            "video_tracks": self.video_tracks,
            "audio_tracks": self.audio_tracks,
            "general_track": self.general_track,
        }

    @classmethod
    # non son più necessarie le virgolette per le classi non ancora completamente costruite ad esempio in "MediaFile"
    # basta importare annotations
    def dict_to_mediafile(cls, data: Dict) -> MediaFile:
        """
        From dict to Mediafile
        """
        return cls(
            file_path=data.get("file_path", ""),
            media_to_string=data.get("media_to_string"),
            video_tracks=data.get("video_tracks", []),
            audio_tracks=data.get("audio_tracks", []),
            general_track=data.get("general_track", {}),
        )
