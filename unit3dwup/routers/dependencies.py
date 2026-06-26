# -*- coding: utf-8 -*-
from fastapi import Request

from unit3dwup.config.settings import Settings
from unit3dwup.external.websocket import WebSocketManager
from unit3dwup.repositories.job_repos import JobRedisRepo


def load_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_job_repo(request: Request) -> JobRedisRepo:
    return request.app.state.job


def get_ws_manager(request: Request) -> WebSocketManager:
    return request.app.state.ws_manager


def get_restart_docker(request: Request) -> bool:
    return request.app.state.restart_docker