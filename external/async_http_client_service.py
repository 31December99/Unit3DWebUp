import aiohttp

from config import logger

class AsyncHttpClient:
    """
     basic Async HTTP client
    """
    def __init__(self, session: aiohttp.ClientSession | None = None):
        """
        :param session: aiohttp.ClientSession | None
        """
        self.session = session or aiohttp.ClientSession()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def get(self, url: str, params: dict = None):
        try:
            async with self.session.get(url, params=params, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception as e:
            logger.debug(f"[HTTP ERROR] {e} | URL: {url}")
            return None

    async def post(self, url: str, data: dict = None):
        try:
            async with self.session.post(url, json=data, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception as e:
            logger.debug(f"[HTTP ERROR] {e} | URL: {url}")
            return None
