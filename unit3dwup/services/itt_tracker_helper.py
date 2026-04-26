# -*- coding: utf-8 -*-
# Based on the old code 0.8.21
import io
import asyncio
import aiohttp

from pathlib import Path
from urllib.parse import urljoin
from unit3dwup.config.api_data import trackers_api_data


class Myhttp:
    def __init__(
            self,
            tracker_name: str,
            pass_key: str = "",
            session: aiohttp.ClientSession | None = None,
    ):
        """
        :param tracker_name: short name of the tracker
        :param pass_key: not used
        :param session: aiohttp.ClientSession | None
        """

        api_data = trackers_api_data.get(tracker_name.upper())
        if not api_data:
            raise ValueError(f"Tracker '{tracker_name}' not found")

        self.session = session or aiohttp.ClientSession()
        self.pass_key = pass_key

        self.base_url = api_data["url"]
        self.api_token = api_data["api_key"]

        # Endpoints
        self.upload_url = urljoin(str(self.base_url), "api/torrents/upload")
        self.filter_url = urljoin(str(self.base_url), "api/torrents/filter")
        self.fetch_url = urljoin(str(self.base_url), "api/torrents/")

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        self.base_params = {}

        # default Payload
        self.data = {
            "name": "TEST.torrent",
            "description": "",  # mandatory
            "mediainfo": "",
            "bdinfo": "",
            "type_id": 1,
            "resolution_id": 10,  # mandatory
            "tmdb": 0,  # mandatory
            "imdb": 0,
            "tvdb": 0,
            "mal": 0,  # no ancora implementato
            "igdb": 0,
            "anonymous": 0,
            "sd": 0,
            "keywords": "",
            "personal_release": 0,
            "internal": 0,
            "featured": 0,
            "free": 0,
            "doubleup": 0,
            "sticky": 0,
        }

    async def close(self):
        await self.session.close()


class Tracker(Myhttp):
    """
        calls "low level"...
    """

    async def _get(self, params: dict):

        # Build the params
        final_params = {k: v for k, v in params.items() if v is not None}

        # Set the _token_
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.api_token}"
        }

        while True:
            try:
                async with self.session.get(self.filter_url, params=final_params, headers=headers,
                                            timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 429:
                        await asyncio.sleep(60)
                        continue

                    resp.raise_for_status()
                    data = await resp.json()
                    return data

            except aiohttp.ClientResponseError as e:
                raise RuntimeError(f"Tracker HTTP error {e.status}") from e

            except asyncio.TimeoutError as e:
                raise TimeoutError("Tracker timeout") from e

    async def _post(self, files: dict, data: dict) -> dict:
        # Prepare the form
        form = aiohttp.FormData()

        # Fill the form
        for k, v in data.items():
            form.add_field(k, str(v))

        # Prepare the field for the file
        for k, (name, fp, ctype) in files.items():
            form.add_field(k, fp, filename=name, content_type=ctype)

        # Set the _token_
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.api_token}"
        }

        # Send to the tracker timeout 30
        async with self.session.post(self.upload_url, headers=headers, data=form,
                                     timeout=aiohttp.ClientTimeout(total=30)) as resp:
            return await resp.json()

    # Main endpoints fetch all
    async def _fetch_all(self, params: dict):
        final_params = {**self.base_params, **params}
        async with self.session.get(
                self.fetch_url,
                params=final_params,
                headers=self.headers,
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    # Main endpoints fetch by id
    async def _fetch_id(self, torrent_id: int):
        async with self.session.get(
                f"{self.fetch_url}{torrent_id}",
                params=self.base_params,
                headers=self.headers,
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    @staticmethod
    def bool_to_str(value: bool) -> str:
        return 'true' if value else 'false'


class filterAPI(Tracker):
    """
     Calls "high level"...
    """

    async def tmdb(self, tmdb_id: int, perPage: int = None):
        return await self._get({"tmdbId": tmdb_id, "perPage": perPage})

    async def imdb(self, imdb_id: int, perPage: int = None):
        return await self._get({"imdbId": imdb_id, "perPage": perPage})

    async def tvdb(self, tvdb_id: int, perPage: int = None):
        return await self._get({"tvdbId": tvdb_id, "perPage": perPage})

    async def mal(self, mal_id: int, perPage: int = None):
        return await self._get({"malId": mal_id, "perPage": perPage})

    async def playlist_id(self, playlistId: int, perPage: int = None):
        return await self._get({"playlistId": playlistId, "perPage": perPage})

    async def collection_id(self, collectionId: int, perPage: int = None):
        return await self._get({"collectionId": collectionId, "perPage": perPage})

    async def freeleech(self, freeleech: int, perPage: int = None):
        return await self._get({"free": freeleech, "perPage": perPage})

    async def name(self, name: str, perPage: int = None):
        return await self._get({"name": name, "perPage": perPage})

    async def description(self, description: str, perPage: int = None):
        return await self._get({"description": description, "perPage": perPage})

    async def mediainfo(self, mediainfo: str, perPage: int = None):
        return await self._get({"mediainfo": mediainfo, "perPage": perPage})

    async def bdinfo(self, bdinfo: str, perPage: int = None):
        return await self._get({"bdinfo": bdinfo, "perPage": perPage})

    async def start_year(self, start_year: str, perPage: int = None):
        return await self._get({"startYear": start_year, "perPage": perPage})

    async def end_year(self, end_year: str, perPage: int = None):
        return await self._get({"endYear": end_year, "perPage": perPage})

    async def uploader(self, uploader: str, perPage: int = None):
        return await self._get({"uploader": uploader, "perPage": perPage})

    async def alive(self, alive: int, perPage: int = None):
        return await self._get({"alive": alive, "perPage": perPage})

    async def dying(self, dying: int, perPage: int = None):
        return await self._get({"dying": dying, "perPage": perPage})

    async def dead(self, dead: int, perPage: int = None):
        return await self._get({"dead": dead, "perPage": perPage})

    async def file_name(self, file_name: str, perPage: int = None):
        return await self._get({"file_name": file_name, "perPage": perPage})

    async def seasonNumber(self, seasonNumber: int, perPage: int = None):
        return await self._get({"seasonNumber": seasonNumber, "perPage": perPage})

    async def episodeNumber(self, episodeNumber: int, perPage: int = None):
        return await self._get({"episodeNumber": episodeNumber, "perPage": perPage})

    async def types(self, type_id: str, perPage: int = None):
        return await self._get({"types[]": type_id, "perPage": perPage})

    async def resolution(self, res_id: str, perPage: int = None):
        return await self._get({"resolutions[]": res_id, "perPage": perPage})

    async def doubleup(self, double_up: int, perPage: int = None):
        return await self._get({"doubleup": double_up, "perPage": perPage})

    async def featured(self, featured: int, perPage: int = None):
        return await self._get({"featured": featured, "perPage": perPage})

    async def refundable(self, refundable: int, perPage: int = None):
        return await self._get({"refundable": refundable, "perPage": perPage})

    async def stream(self, stream: int, perPage: int = None):
        return await self._get({"stream": stream, "perPage": perPage})

    async def sd(self, sd: int, perPage: int = None):
        return await self._get({"sd": sd, "perPage": perPage})

    async def highspeed(self, high_speed: int, perPage: int = None):
        return await self._get({"highspeed": high_speed, "perPage": perPage})

    async def internal(self, internal: int, perPage: int = None):
        return await self._get({"internal": internal, "perPage": perPage})

    async def personal_release(self, personalRelease: int, perPage: int = None):
        return await self._get({"personalRelease": personalRelease, "perPage": perPage})

    async def tmdb_res(self, tmdb_id: int, res_id: str, perPage: int = None):
        return await self._get({
            "tmdbId": tmdb_id,
            "resolutions[]": res_id,
            "perPage": perPage,
        })


class Torrents(Tracker):
    """
      TORRENTS
      High level calls for fetch endpoints
    """

    async def torrents(self, perPage: int = None):
        return await self._fetch_all({"perPage": perPage})

    async def torrent(self, torrent_id: int):
        return await self._fetch_id(torrent_id)


class Uploader(Tracker):
    """
     UPLOADER
     Upload the torrent file *.torrent
     Upload the nfo file
    """

    async def upload_t(self, data: dict, torrent_path: Path, nfo_path=None) -> dict | None:
        files = {}

        if Path(torrent_path).exists():
            with open(torrent_path, "rb") as tf:
                files["torrent"] = (
                    "upload.torrent",
                    tf,
                    "application/x-bittorrent",
                )

                if nfo_path:
                    with open(nfo_path, "rb") as nf:
                        files["nfo"] = ("file.nfo", nf, "text/plain")
                        return await self._post(files, data)

                return await self._post(files, data)
        return None

    @staticmethod
    def encode_utf8(file_path: str) -> bytes | io.BytesIO:
        encodings = ["utf-8", "iso-8859-1", "windows-1252", "latin1"]
        raw = open(file_path, "rb").read()

        for enc in encodings:
            try:
                return raw.decode(enc).encode("utf-8")
            except UnicodeDecodeError:
                pass

        return io.BytesIO(b"Error: Unable to decode NFO file")


class Unit3D(filterAPI, Torrents, Uploader):
    """
    UNIT3D - calls
    """

    async def get_tmdb(self, tmdb_id: int, perPage: int = None):
        return await self.tmdb(tmdb_id=tmdb_id, perPage=perPage)

    async def get_tvdb(self, tvdb_id: int, perPage: int = None):
        return await self.tvdb(tvdb_id=tvdb_id, perPage=perPage)

    async def get_imdb(self, imdb_id: int, perPage: int = None):
        return await self.imdb(imdb_id=imdb_id, perPage=perPage)

    async def get_igdb(self, igdb_id: int, perPage: int = None):
        return await self.igdb(igdb_id=igdb_id, perPage=perPage)

    async def get_mal(self, mal_id: int, perPage: int = None):
        return await self.mal(mal_id=mal_id, perPage=perPage)

    async def get_playlist_id(self, playlist_id: int, perPage: int = None):
        return await self.playlist_id(
            playlistId=playlist_id, perPage=perPage
        )

    async def get_collection_id(self, collection_id: int, perPage: int = None):
        return await self.collection_id(
            collectionId=collection_id, perPage=perPage
        )

    async def get_freeleech(self, freeleech: int, perPage: int = None):
        return await self.freeleech(
            freeleech=freeleech, perPage=perPage
        )

    async def get_name(self, name: str, perPage: int = None):
        return await self.name(name=name, perPage=perPage)

    async def get_description(self, description: str, perPage: int = None):
        return await self.description(
            description=description, perPage=perPage
        )

    async def get_bdinfo(self, bdinfo: str, perPage: int = None):
        return await self.bdinfo(bdinfo=bdinfo, perPage=perPage)

    async def get_mediainfo(self, mediainfo: str, perPage: int = None):
        return await self.mediainfo(
            mediainfo=mediainfo, perPage=perPage
        )

    async def get_uploader(self, uploader: str, perPage: int = None):
        return await self.uploader(
            uploader=uploader, perPage=perPage
        )

    async def after_start_year(self, start_year: str, perPage: int = None):
        return await self.start_year(
            start_year=start_year, perPage=perPage
        )

    async def before_end_year(self, end_year: str, perPage: int = None):
        return await self.end_year(
            end_year=end_year, perPage=perPage
        )

    async def get_alive(self, alive: int, perPage: int = None):
        return await self.alive(alive=alive, perPage=perPage)

    async def get_dying(self, dying: int, perPage: int = None):
        return await self.dying(dying=dying, perPage=perPage)

    async def get_dead(self, dead: int, perPage: int = None):
        return await self.dead(dead=dead, perPage=perPage)

    async def get_filename(self, file_name: str, perPage: int = None):
        return await self.file_name(
            file_name=file_name, perPage=perPage
        )

    async def get_season_number(self, se_number: int, perPage: int = None):
        return await self.seasonNumber(
            seasonNumber=se_number, perPage=perPage
        )

    async def get_episode_number(self, ep_number: int, perPage: int = None):
        return await self.episodeNumber(
            episodeNumber=ep_number, perPage=perPage
        )

    async def get_types(self, type_id: str, perPage: int = None):
        if type_id:
            return await self.types(type_id=type_id, perPage=perPage)
        return None

    async def get_res(self, res_id: str, perPage: int = None):
        if res_id:
            return await self.resolution(res_id=res_id, perPage=perPage)
        return None

    async def fetch_all(self, perPage: int = None):
        return await self.torrents(perPage=perPage)

    async def fetch_id(self, torrent_id: int):
        return await self.torrent(torrent_id=torrent_id)

    async def get_double_up(self, double_up: int, perPage: int = None):
        return await self.doubleup(
            double_up=double_up, perPage=perPage
        )

    async def get_featured(self, featured: int, perPage: int = None):
        return await self.featured(
            featured=featured, perPage=perPage
        )

    async def get_refundable(self, refundable: int, perPage: int = None):
        return await self.refundable(
            refundable=refundable, perPage=perPage
        )

    async def get_stream(self, stream: int, perPage: int = None):
        return await self.stream(
            stream=stream, perPage=perPage
        )

    async def get_sd(self, sd: int, perPage: int = None):
        return await self.sd(sd=sd, perPage=perPage)

    async def get_highspeed(self, highspeed: int, perPage: int = None):
        return await self.highspeed(
            high_speed=highspeed, perPage=perPage
        )

    async def get_internal(self, internal: int, perPage: int = None):
        return await self.internal(
            internal=internal, perPage=perPage
        )

    async def get_personal_release(self, personalRelease: int, perPage: int = None):
        return await self.personal_release(
            personalRelease=personalRelease, perPage=perPage
        )

    async def get_tmdb_res(self, tmdb_id: int, res_id: str, perPage: int = None):
        if tmdb_id and res_id:
            return await self.tmdb_res(
                tmdb_id=tmdb_id, res_id=res_id, perPage=perPage
            )
        return None
