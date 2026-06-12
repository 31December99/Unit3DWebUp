# -*- coding: utf-8 -*-
import inspect
import json

from fastapi import APIRouter, Depends, Request

from unit3dwup.config import get_logger
from unit3dwup.config.limiter import limiter

from unit3dwup.schemas import ClearJobListRequest

from unit3dwup.external.websocket import WebSocketManager
from unit3dwup.routers.dependencies import (
    get_job_repo,
    get_ws_manager,
)

router = APIRouter()


@router.post("/cjoblist")
@limiter.limit("5/minute")
async def clear_job_list_id(payload: ClearJobListRequest, request: Request,
                            job_repo=Depends(get_job_repo),
                            ws_manager: WebSocketManager = Depends(get_ws_manager),
                            ):
    """
        This endpoint deletes a job list and all related posters

        Required:
        - job_list_id: identifier of the job list

        Returns:
        - status: operation result
        """

    # Load the job list
    # Carica la joblist per ottenere il percorso e inviarlo a log. Mi sembra troppo per una stampa
    job_list = await job_repo.job.get_job_list(job_id=payload.job_list_id)
    results = [json.loads(await job_repo.get_job(job_id)) for job_id in job_list]

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Delete the job list
    # TODO: delete all job ids
    await job_repo.delete_job_list(job_id=payload.job_list_id)

    if results:
        await ws_manager.broadcast({
            "type": "log",
            "level": "success",
            "message": f"Clear JobList {payload.job_list_id} {results[0]['folder']}",
        })
        logger.info(f"-> Clear JobList ID° {payload.job_list_id} {results[0]['folder']}\n")
    else:
        await ws_manager.broadcast({
            "type": "log",
            "level": "error",
            "message": f"Clear JobList : JobList id not found",
        })
        logger.info(f"-> Clear JobList : JobList ID non trovato\n")
