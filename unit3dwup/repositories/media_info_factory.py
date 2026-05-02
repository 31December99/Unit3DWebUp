# -*- coding: utf-8 -*-

import asyncio

from pymediainfo import MediaInfo
from unit3dwup.models.media_info import MediaFile


class MediaFileFactory:

    @staticmethod
    async def from_path(path: str) -> MediaFile:
        """
        Try to run pymediainfo without blocking
        """
        info = await asyncio.to_thread(MediaInfo.parse, path)
        data = info.to_data().get("tracks", [])

        video = [track for track in data if track.get("track_type") == "Video"]
        audio = [track for track in data if track.get("track_type") == "Audio"]
        general = next((track for track in data if track.get("track_type") == "General"), {})
        text = [track for track in data if track.get("track_type") == "Text"]

        return MediaFile(
            file_path=path,
            video_tracks=video,
            audio_tracks=audio,
            general_track=general,
            text_tracks=text,
        )
