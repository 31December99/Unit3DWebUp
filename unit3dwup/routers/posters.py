# -*- coding: utf-8 -*-
import inspect

from fastapi import APIRouter, Request

from unit3dwup.config import MediaStatus
from unit3dwup.config import get_logger
from unit3dwup.config.limiter import limiter

from unit3dwup.schemas import UpdatePosterRequest

router = APIRouter()


async def update_poster(app, msg: str, job_id: str, field_id: str, new_id: str):
    # Fix the DB ID with the received one
    await app.state.job.update_job(job_id=job_id, new_data={field_id: new_id})

    # Update the Media status
    await app.state.job.update_job(job_id=job_id, new_data={'status': str(MediaStatus.DB_IDENTIFIED)})

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Console message
    logger.info(f"-> Update {msg} JOB_ID: {job_id}\n")

    # Send log to the client
    await app.state.ws_manager.broadcast({
        "type": "log",
        "level": "success",
        "message": f"Update {msg} JOB_ID {job_id}",
    })


@router.post("/settmdbid")
@limiter.limit("5/minute")
async def set_poster_id(payload: UpdatePosterRequest, request: Request):
    """
    Set a Tmdb id for example when tmdb returns an empty result

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(request.app, msg="TMDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@router.post("/settvdbid")
@limiter.limit("5/minute")
async def set_tvdb_id(payload: UpdatePosterRequest, request: Request):
    """
    Set a TVdb id for example when tvdb returns an empty result

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(request.app, msg="TVDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@router.post("/setimdbid")
@limiter.limit("5/minute")
async def set_imdb_id(payload: UpdatePosterRequest, request: Request):
    """
    Set an Imdb id for example when the remote list of tvdb is empty

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(request.app, msg="IMDB", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@router.post("/setposterurl")
@limiter.limit("5/minute")
async def set_poster_url(payload: UpdatePosterRequest, request: Request):
    """
    Set a poster url for example when tmdb returns an empty result only for frontend

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(request.app, msg="TMDB Poster Url", job_id=payload.job_id, field_id=payload.field_id, new_id=payload.new_id)


@router.post("/setposterdname")
@limiter.limit("5/minute")
async def set_poster_dname(payload: UpdatePosterRequest, request: Request):
    """
    Set a poster display name for example if you dont like it
    Display name is the name shown on the dedicated torrent page

    Required
    - job_id identifies each poster corresponds to Media.job_id

    Return
    - none
    """

    await update_poster(request.app, msg="Update DisplayName", job_id=payload.job_id, field_id=payload.field_id,
                        new_id=payload.new_id)
