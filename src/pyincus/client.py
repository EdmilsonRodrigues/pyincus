"""Incus API Client definition."""

import asyncio
import atexit
import functools
from os import PathLike

import aiohttp

from .config import UNIX_SOCKET_PATH
from .exceptions import PyIncusException


class Client:
    """
    Client for connecting with the Incus API.

    All methods are asynchronous.
    """

    def __init__(self, socket_path: PathLike = UNIX_SOCKET_PATH):
        """Init client class."""
        connector = aiohttp.UnixConnector(path=str(socket_path))
        self._session = aiohttp.ClientSession(connector=connector)
        self._BASE_URL = 'https://localhost:8443/1.0'

        atexit.register(self._close)

    @staticmethod
    def _request(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            await self._pre_flight_request()
            return await func(self, *args, **kwargs)

        return wrapper

    async def close(self):
        """Close the client session."""
        await self._session.close()

    @_request
    async def _get_instances(self):
        """Get all instances."""
        url = self._BASE_URL + '/instances'
        async with self._session.get(url) as response:
            self._raise_for_status(response, 'Could not get instances')
            return await response.json()

    async def _pre_flight_request(self):
        async with self._session.get(self._BASE_URL) as response:
            self._raise_for_status(
                response,
                'Could not launch pre-flight request. '
                'Please verify connection with Unix Socket',
            )

    @staticmethod
    async def _raise_for_status(response, message: str):
        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as exc:
            raise PyIncusException(message) from exc

    def _close(self, loop=None):
        """Close the client session synchronously."""
        if self._session.closed:
            return

        try:
            loop = loop or asyncio.get_event_loop()
        except Exception:
            loop = asyncio.new_event_loop()
        finally:
            loop.run_until_complete(self._session.close())


async def _main():
    client = Client()
    await client.get_instances()


if __name__ == '__main__':
    asyncio.run(_main())
