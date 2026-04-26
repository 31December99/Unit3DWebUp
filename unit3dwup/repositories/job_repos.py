# -*- coding: utf-8 -*-

import json
import os
import signal
from fastapi import FastAPI

from unit3dwup.config.logger import get_logger
from unit3dwup.repositories.interfaces import JobRepositoryInterface

import redis.asyncio as redis
from redis import exceptions as redis_exceptions, Redis


class JobRedisRepo(JobRepositoryInterface):
    """
    Manage Redis connections

    Save Media data to Redis

    Redis instance is stored in FastAPi app.state

    The purpose is to avoid waste calls to scanner and share data across endpoints and other..(later)

    """

    def __init__(self, url: str):
        """
        :param url: Redis server url
        """
        self.redis = redis.from_url(url, decode_responses=True)
        self.logger = get_logger(self.__class__.__name__)

    async def connect(self, app: FastAPI) -> Redis | None:
        """
        :param app: FastAPi app instance
        :return: the redis instance stored in the fastapi app
        """
        app.state.redis = self.redis

        try:
            if await self.redis.ping(): print("INfO:     DB connected to redis://localhost:6379")
            return self.redis
        except redis_exceptions.ConnectionError as e:
            self.logger.error("Database connection error")
            os.kill(os.getpid(), signal.SIGTERM)
            return None

    async def create_job(self, job_id: str, data: dict):
        """
        :param job_id: Job id is the file or folder path hashed stored in the Media class object
        :param data: a dict che store the data of Media object ( media to dict())
        :return:

        Create a new job
        Each job represents a Media file or folder

        Every Media object contains a job_id (hash)
        """
        try:
            await self.redis.hset(job_id, mapping={
                "data": json.dumps(data),
            })
        except Exception as e:
           self.logger.error(e)
        return job_id

    async def create_job_list(self, job_id: str, job_list: list):
        """
        :param job_id: Job id is the scan path hashed
        :param job_list: a list of job id
        :return:

        It represents a page on the frontend that is a list of Poster

        We use joblist to manage group of posters

        Each poster is a job id
        """
        await self._save_list(job_id, job_list)

    async def get_job_list(self, job_id: str) -> list:
        """
        :param job_id: the job id list
        :return: a list of job id

        Get a list of Jobs ID

        it represents a page on the frontend

        For example we load the page on start to avoid running a new scan on the ssd and requests to TMDB,TVDB
        """
        ids = await self.redis.smembers(f"{job_id}:ids")
        return list(set(ids))

    async def create_profile(self, data: dict):
        """
        :param data: a dict che store the configuration file read from the server
        :return:

        Create a new job that includes the user preferences read from the configuration file

        You can see the preferences on the preferences page
        """
        await self.create_job(job_id='0', data=data)

    async def get_job(self, job_id: str):
        """
        :param job_id: Job id is the file or folder path hashed stored in the Media class object
        :return: a dict that stores data about Media object
        """
        return await self.redis.hget(job_id, 'data')

    async def update_job(self, job_id: str, new_data: dict):
        """
        :param job_id: Job id is the file or folder path hashed stored in the Media class object
        :param new_data: a dict that stores new data
        :return:

        Update a specific field of a job
        """

        current = await self.redis.hget(job_id, "data")
        if current:
            data = json.loads(current)
        else:
            data = {}

        data.update(new_data)

        await self.redis.hset(job_id, mapping={
            "data": json.dumps(data),
        })

        return job_id

    async def _save_list(self, job_id: str, job_list_id: list):
        """
        :param job_id: the job id list
        :param job_list_id: a list of job id
        :return:

        Replace an old job list with a new one

        for example if the user moves or deletes or adds new file in the scan folder

        """
        await self.redis.delete(f"{job_id}:ids")
        await self.redis.sadd(f"{job_id}:ids", *job_list_id)

    async def delete_job_list(self, job_id: str):
        """
        :param job_id: the job id list
        :return:

        Delete an old job list

        For example if the user wipes the scan folder
        """

        await self.redis.delete(f"{job_id}:ids")

    async def close(self):
        """
        Close connection to Redis server
        """
        await self.redis.close()
