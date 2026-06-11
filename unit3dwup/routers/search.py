# -*- coding: utf-8 -*-
import aiohttp

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from unit3dwup.services.itt_tracker_service import ITTtrackerService
from unit3dwup.services.interfaces import TrackerServiceInterface

from unit3dwup.schemas import FilterRequest

router = APIRouter()


@router.post("/filter")
async def filter_search(payload: FilterRequest, request: Request):
    """
    Search words or title in the tracker

    Required
    - title: title or part of it

    Return
    - none
    """

    app = request.app

    # Search for a title in the tracker
    async with aiohttp.ClientSession() as session:
        # A new ITT tracker instance with interface
        tracker_service: TrackerServiceInterface = ITTtrackerService(session, app=app)

        # Search
        data = await tracker_service.search(payload.title)

        # Return the source as remote ( change the bottom line color on the poster)
        # job_id not applicable
        # Extract attributes field for each data found
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "source": "remote",
                "job_id": '-1',
                "results": [c['attributes'] for c in data['data']],
            }
        )
