# -*- coding: utf-8 -*-
import aiohttp
import base64
import os
import io

from pathlib import Path
from PIL import Image

from unit3dwup.services.interfaces import VideoServiceInterface, DescriptionBuilderInterface
from unit3dwup.config.host_data import upload_hosts, master_uploaders
from unit3dwup.external.async_http_client_service import AsyncHttpClient
from unit3dwup.config.constants import MediaStatus
from unit3dwup.config.settings import get_settings
from unit3dwup.config.logger import get_logger
from unit3dwup.config import __version__
from unit3dwup.models.media import Media

from pymediainfo import MediaInfo
from aiohttp import FormData
from fastapi import FastAPI
import numpy as np
import asyncio



# Based on the old code unit3dup 0.8.21
class VideoFrame:
    def __init__(self, video_path: str, num_screenshots: int, webp_filepath=None):
        self.video_path = Path(video_path)
        self.webp_filepath = Path(webp_filepath) if webp_filepath else None
        self.num_screenshots = num_screenshots
        self.logger = get_logger(self.__class__.__name__)

    async def create(self):
        """
        return list of extract screenshots from the video
        """
        frames = await self._extract()
        frames_in_bytes = []
        is_hd = 0

        for frame in frames:
            img_bytes = self.image_to_bytes(frame)
            if frame.height >= 720:
                is_hd = 1
            frames_in_bytes.append(img_bytes)

        webp = []
        if self.webp_filepath:
            webp = await self.create_webp_from_video(video_path=self.video_path, output_path=self.webp_filepath)

        return frames_in_bytes + (webp or []), is_hd

    @staticmethod
    def image_to_bytes(frame: Image.Image) -> bytes:
        """
        Convert frame bytes to Jpeg with no compression
        """
        buffered = io.BytesIO()
        frame.save(buffered, format="JPEG", optimize=False, compress_level=4)
        return buffered.getvalue()

    async def _get_video_duration(self) -> float:
        """
        return the video duration

        -show_entries format: Get video duration

        -of default=noprint_wrappers=1:nokey=1:  output formatted to get only the number ( duration value)
        """
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(self.video_path),
        ]
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        return float(stdout.decode().strip())

    async def _extract(self):
        """
            FFPROBE
            - "-v",                                       show the errore only
            - "-select_streams", "v:0",                   extract only the first stream
            - "-show_entries", "stream=width,height",     return only Height and Width value
            - "-of", "default=nw=1:nk=1",                 print only the numeric value ( WxH value)

            - FFMPEG
            - "-ss", str(t),                              seek at time t(secondi)
            - "-i", str(self.video_path),                 video file path
            - "-vframes", "1",                            extract only one frame
            - "-f", "rawvideo",                           output format rawvideo
            - "-pix_fmt", "rgb24",                        24-bit rgb  - todo: problema con formato png?
            - "-" : output to stdout

        :return:
        """

        duration = await self._get_video_duration()
        # todo: Hardcoded values
        start_time = duration * 0.35
        end_time = duration * 0.85

        times = np.linspace(start_time, end_time, self.num_screenshots, endpoint=True)

        command = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "default=nw=1:nk=1",
            str(self.video_path)

        ]
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        w, h = stdout.decode().strip().splitlines()
        width, height = int(w), int(h)

        frames = []
        for t in times:
            command = [
                "ffmpeg",
                "-ss", str(t),
                "-i", str(self.video_path),
                "-vframes", "1",
                "-f", "rawvideo",
                "-pix_fmt", "rgb24",  # ho avuto un problema con png
                "-"
            ]
            proc = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL
            )
            stdout, _ = await proc.communicate()
            img = Image.fromarray(np.frombuffer(stdout, dtype=np.uint8).reshape((height, width, 3)))
            frames.append(img)

        return frames


    async def create_webp_from_video(self, video_path, output_path):
        """
        - "-y",                                            overwrite output if it exists
        - "-ss", '70',                                     start time at 70 seconds
        - "-t", '10',                                      extracts 10 seconds
        - "-i", video_path,                                video file path
        - "-vf", f"fps=7,scale=650:-1:flags=lanczos",      set fps and scale to 650 ( aspect ratio ok)
        - "-c:v", "libwebp",                               encode video as WebP
        - "-quality", "50",                                quality
        - "-loop", "0",                                    repeat the animation
        - "-speed", "9",                                   encoding speed (1 = slowest, 10 = fastest)
        - "-threads", "8",                                 number of threads
        - "-f", "webp",                                    webp format
        - "output_path"                                    output file path
        """
        command = [
            "ffmpeg",
            "-y",
            "-ss", '70',
            "-t", '10',
            "-i", video_path,
            "-vf", f"fps=7,scale=650:-1:flags=lanczos",
            "-c:v", "libwebp",
            "-quality", "50",
            "-loop", "0",
            "-speed", "9",
            "-threads", "8",
            "-f", "webp",
            output_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()

        if not os.path.isfile(output_path):
            self.logger.error(f"file {output_path} doesn't exist!")
            return None

        # todo: vorrei non dover scrivere su file ma in memoria ram
        with open(output_path, "rb") as webp_file:
            webp_file_content = webp_file.read()
        os.remove(output_path)
        return [webp_file_content]


class VideoService(VideoServiceInterface):
    """ Build a description for the torrent page: screenshots, mediainfo, trailers, metadata """

    def __init__(self, media: Media):
        """
        :param media: The Media object
        """

        self.media = media
        self.file_name: str = media.file_name
        self.display_name: str = media.display_name
        self.webp_filepath: str | None = None
        settings = get_settings()

        if settings.prefs.WEBP_ENABLED:
            self.webp_filepath = f"{media.display_name}.webp"

        # Load the video frames
        # if web_enabled is off set the number of screenshots to an even number
        if not settings.prefs.WEBP_ENABLED:
            if settings.prefs.NUMBER_OF_SCREENSHOTS % 2 != 0:
                settings.prefs.NUMBER_OF_SCREENSHOTS += 1

        samples_n = max(2, min(settings.prefs.NUMBER_OF_SCREENSHOTS, 10))

        self.video_frames: VideoFrame = VideoFrame(video_path=self.file_name,
                                                   num_screenshots=samples_n, webp_filepath=self.webp_filepath)

    async def generate(self):
        """Build the information to send to the tracker"""

        # Extract the frames
        self.media.extracted_frames, self.media.is_hd = await self.video_frames.create()
        # Add Media description
        self.media.media_to_string = await asyncio.to_thread(MediaInfo.parse, self.media.file_name,
                                                             output="STRING", full=False)
        return None


class BuildService(DescriptionBuilderInterface):
    """
        Upload all previously created screenshots to hostimage, get their URLs, build a description for the tracker
    """

    def __init__(self, media_list: list[Media], app: FastAPI, session: aiohttp.ClientSession | None = None):
        """
        :param media_list: a list of Media objects
        :param session: aiohttp.ClientSession | None
        """
        self.session = session or aiohttp.ClientSession()
        self.http = AsyncHttpClient(self.session)
        self.media_list = media_list
        self.app = app
        self.screenshots = []
        self.logger = get_logger(self.__class__.__name__)
        self.sign = (
            f"[url=https://github.com/31December99/Unit3DWebUp][code][color=#00BFFF][size=14]Uploaded with Unit3DwUp"
            f" {__version__}[/size][/color][/code][/url]")

    async def description(self):

        settings = get_settings()
        priority_map = {
            'ImgBB': settings.prefs.IMGBB_PRIORITY,
            'PtScreens': settings.prefs.PTSCREENS_PRIORITY,
            'LensDump': settings.prefs.LENSDUMP_PRIORITY,
            'ImgFi': settings.prefs.IMGFI_PRIORITY,
            'PassIMA': settings.prefs.PASSIMA_PRIORITY,
            'ImaRide': settings.prefs.IMARIDE_PRIORITY,
            'Freeimage': settings.prefs.FREE_IMAGE_PRIORITY,
        }

        user_order = sorted(master_uploaders, key=lambda uploader: priority_map[uploader])

        async def upload_frame(media: Media, index: int, image_bytes: bytes) -> str:
            """
            :param media: the Media object
            :param index: enumeration for the screenshot
            :param image_bytes: the image data
            :return:

            Upload single frame
            """

            image_name = f"{media.display_name}.id_{index}"
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            timeout = 30

            host = upload_hosts[user_order[0]]
            form = FormData()
            form.add_field('key', host['data']['key'])

            # passtheima host
            if host.get('data', {}).get('fieldname', None):
                form.add_field(host['data']['fieldname'], image_name)
            form.add_field('image', image_base64)

            try:
                response = await self.session.post(host['url'], data=form, timeout=timeout)
                response.raise_for_status()
                result = await response.json()
                if result.get('data', None):
                    img_url = result["data"]["image"]["url"]
                else:
                    img_url = result["image"]["url"]
                self.logger.info(f"[OK] Uploaded {img_url}")
                self.screenshots.append(img_url)
                media.status = MediaStatus.DESCRIPTION_READY
                return f"[url={img_url}][img=650]{img_url}[/img][/url]"
            except Exception as e:
                self.logger.error(f"[ERROR] Upload frame {image_name}: {e}")
                media.status = MediaStatus.DESCRIPTION_ERROR
                return ""

        async def upload_media(media: Media) -> str | None:
            """
            :param media: the Media object
            :return:

            upload media screenshot to hostimage
            """
            tasks = [upload_frame(media, idx, img_bytes) for idx, img_bytes in enumerate(media.extracted_frames)]
            uploaded_frames = await asyncio.gather(*tasks)

            media.screen_shots = self.screenshots
            if media.status == MediaStatus.DESCRIPTION_READY:
                description = "[center]\n" + "".join(uploaded_frames)
                if media.trailer:
                    description += (
                        f"\n[/center][b][spoiler=Spoiler:"
                        f" PLAY TRAILER][center][youtube]{media.trailer}[/youtube]"
                        f"[/center][/spoiler][/b]")
                description+=self.sign
                return description
            return None

        # Upload
        all_descriptions = await asyncio.gather(*[upload_media(media) for media in self.media_list])
        # Add description
        for media, desc in zip(self.media_list, all_descriptions):
            if media.status == MediaStatus.DESCRIPTION_READY:
                media.description = desc
            else:
                self.logger.warning("Description error")
                # Send a message to the frontend by ws
                await self.app.state.ws_manager.broadcast({
                    "type": "log",
                    "level": "error",
                    "message": f"Failed to build description for {media.file_name}",
                })

        return None

    async def close(self) -> None:
        await self.session.close()
