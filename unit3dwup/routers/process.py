# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from unit3dwup.use_case.process_all_usecase import ProcessAllUseCase
from unit3dwup.use_case.upload_usecase import UploadUseCase
from unit3dwup.use_case.seed_usecase import SeedUseCase
from unit3dwup.use_case.make_torrent_usecase import MakeTorrentUseCase

from unit3dwup.schemas import ProcessAllRequest, JobRequest

router = APIRouter()


@router.post("/processall")
async def process_all(payload: ProcessAllRequest, request: Request):
    """
    Start a chain load the joblist filter for existing torrent create torrent upload the complete joblist

    Required
    - job_list_id identifies the list created by the scan endpoint

    Prerequisite
    - valid description status media class attribute

    Return
    - none
    """

    app = request.app

    use_case = ProcessAllUseCase(app=app, job_list_id=payload.job_list_id,
                                 torrent_client_name=app.state.settings.torrent.TORRENT_CLIENT)
    await use_case.execute()


@router.post("/maketorrent")
async def make(payload: JobRequest, request: Request):
    """
    Create one or more torrent files

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """
    app = request.app

    torrent_service = MakeTorrentUseCase(app=app, job_id=payload.job_id)
    await torrent_service.execute()


@router.post("/upload")
async def upload(payload: JobRequest, request: Request):
    """
    Upload a single torrent file

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none

    WebSocket events emitted
    - posterLogMessage: sent for each uploaded torrent
    - job_id: media identifier
    - message: upload result message
    """

    app = request.app

    upload_service = UploadUseCase(app=app, job_id=payload.job_id)
    await upload_service.execute()


@router.post("/seed")
async def seed(payload: JobRequest, request: Request) -> JSONResponse:
    """
    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    app = request.app

    use_case = SeedUseCase(app=app, client=app.state.settings.torrent.TORRENT_CLIENT, job_id=payload.job_id)
    return await use_case.execute()
