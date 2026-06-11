# -*- coding: utf-8 -*-
from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """
    :param ws: websocket connection.Currently used to report the progress of the process (%)
    URL:
        ws://host:8000/ws

    Purpose:
        Push notifications from backend to frontend.

    Events sent by server:
        {
            "type": "log",
            "level": "success | error | warn | info",
            "message": "text"
        }

        {
            "type": "progress",
            "job_id": "abc123",
            "value": 45
        }

    """

    manager = ws.app.state.ws_manager
    await manager.connect(ws)

    try:
        while True:
            # TODO for the moment websocket tx only
            await ws.receive_text()  # waiting for new message
    except:
        pass
    finally:
        await manager.disconnect(ws)
