# -*- coding: utf-8 -*-
import json

from use_case.make_torrent_usecase import MakeTorrentUseCase
from use_case.upload_usecase import UploadUseCase
from use_case.seed_usecase import SeedUseCase

from fastapi import FastAPI
from models.media import Media


class ProcessAllUseCase:
    def __init__(self, app: FastAPI, job_list_id: str, torrent_client_name: str):
        """
        :param app: the FastAPI app
        :param job_list_id: the job list id
        :param torrent_client_name: the torrent client (qbittorrent etc)
        """

        self.app = app
        self.job_list_id = job_list_id

        self.media_list = None
        self.seed_use_case = SeedUseCase(app=app, client=torrent_client_name)
        self.torrent_use_case = MakeTorrentUseCase(app=app)
        self.upload_use_case = UploadUseCase(app=app)

    async def execute(self):
        # LOAD a list of jobs from the cache based on the job_list_id received from the frontend
        job_list = await self.app.state.job.get_job_list(job_id=self.job_list_id)
        results = [json.loads(await self.app.state.job.get_job(job_id)) for job_id in job_list]

        # MEDIA: create a media_list
        self.media_list = [Media.from_dict(item) for item in results]

        # TORRENT: create one or more torrent files
        await self.torrent_use_case.execute(media_list=self.media_list)

        # UPLOAD: upload to the tracker one or more torrent file
        await self.upload_use_case.execute(media_list=self.media_list)

        # SEED: seed one or more torrent file
        await self.seed_use_case.execute(media_list=self.media_list)
