# -*- coding: utf-8 -*-
import inspect
import json

from fastapi import APIRouter, Request

from unit3dwup.config import get_logger

from unit3dwup.schemas import ClearJobListRequest

router = APIRouter()


@router.post("/cjoblist")
async def clear_job_list_id(payload: ClearJobListRequest, request: Request):
    """
        This endpoint deletes a job list and all related posters

        Required:
        - job_list_id: identifier of the job list

        Returns:
        - status: operation result
        """

    app = request.app

    # Load the job list
    # Carica la joblist per ottenere il percorso e inviarlo a log. Mi sembra troppo per una stampa
    job_list = await app.state.job.get_job_list(job_id=payload.job_list_id)
    results = [json.loads(await app.state.job.get_job(job_id)) for job_id in job_list]

    # Logger
    frame = inspect.currentframe()
    logger = get_logger(frame.f_code.co_name)

    # Delete the job list
    # TODO: delete all job ids
    await app.state.job.delete_job_list(job_id=payload.job_list_id)

    if results:
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "success",
            "message": f"Clear JobList {payload.job_list_id} {results[0]['folder']}",
        })
        logger.info(f"-> Clear JobList ID° {payload.job_list_id} {results[0]['folder']}\n")
    else:
        await app.state.ws_manager.broadcast({
            "type": "log",
            "level": "error",
            "message": f"Clear JobList : JobList id not found",
        })
        logger.info(f"-> Clear JobList : JobList ID non trovato\n")
