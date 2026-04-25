# -*- coding: utf-8 -*-

from fastapi import WebSocket
from typing import Set
import asyncio


class WebSocketManager:
    def __init__(self):
        self._connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        async with self._lock:
            if ws in self._connections:
                self._connections.remove(ws)
            self._connections.add(ws)

    async def disconnect(self, ws: WebSocket):
        async with self._lock:
            self._connections.discard(ws)

    async def broadcast(self, message: dict):
        """
        :param message: message to frontend
        :return:
        """
        async with self._lock:
            dead = []
            for ws in self._connections:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.append(ws)

            for ws in dead:
                self._connections.discard(ws)

        for ws in dead:
            self._connections.discard(ws)
