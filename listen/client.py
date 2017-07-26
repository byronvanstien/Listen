import json
import asyncio

import aiohttp
import websockets

from listen.errors import ListenError
from listen.objects import User, Song
from listen.utils import ensure_token
from listen.constants import (
    AUTH_URL,
    USER,
    USER_FAVOURITES,
    SONG_FAVOURITES,
    SONG_REQUEST,
    SOCKET_ENDPOINT
)


class Client(object):
    """
    Client class to interface with listen.moe's API
    """
    def __init__(self, loop: asyncio.BaseEventLoop = None):

        self._headers = {
            "User-Agent": "Listen (https://github.com/GetRektByMe/Listen)",
            "Content-Type": "application/json"
        }

        self._loop = loop or asyncio.get_event_loop()
        self._ws = None
        self.ws_handler = None

    @property
    def loop(self):
        return self._loop

    @property
    def headers(self):
        return self._headers

    async def get_token(self, username: str, password: str):
        """
        :param str username: The username of the account you're getting the token for
        :param str password: The password of the account you're getting the token for
        :rtype: str
        """
        with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.post(AUTH_URL, data=json.dumps({"username": username, "password": password})) as response:
                resp_data = await response.json()
                if not resp_data["success"]:
                    raise ListenError(resp_data["message"])
                self._headers["authorization"] = resp_data["token"]
                return self._headers["authorization"]

    @ensure_token
    async def get_info(self):
        """
        :rtype: :class:`listen.objects.User`
        """
        with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(USER) as response:
                return User(**(await response.json()))

    @ensure_token
    async def get_favorites(self):
        """
        :rtype :class:`listen.objects.Song`
        """
        with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(USER_FAVOURITES) as response:
                songs = []
                response_data = await response.json()
                for s in response_data["songs"]:
                    songs.append(Song(s.get("id"), s.get("artist"), s.get("title"), s.get("anime"), s.get("enabled")))
                return songs

    @ensure_token
    async def favorite_toggle(self, song_id: int):
        """
        :param int song_id: The id of the song you want to favourite
        :rtype bool:
        """
        with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.post(SONG_FAVOURITES, data=json.dumps({"song": song_id})) as response:
                boolean = await response.json()
                return boolean["favorite"]

    @ensure_token
    async def make_request(self, song_id: int):
        """
        :param int song_id: The id of the song you want to request
        :rtype bool:
        """
        with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.post(SONG_REQUEST, data=json.dumps({"song": song_id})) as response:
                requested = await response.json()
                return requested["success"]

    async def get_websocket(self, authenticate: bool = False):
        self.ws = await websockets.connect(SOCKET_ENDPOINT)
        if authenticate:
            await self.ws.send(json.dumps({"token": self.headers["authorization"]}))

    async def start(self):
        while True:
            if self.ws_handler:
                await self.ws_handler(json.loads(await self.ws.recv()))
            else:
                raise RuntimeError("No function handler specified")

    def register_handler(self, handler):
        self.ws_handler = handler

    def run(self):
        self.loop.run_until_complete(self.start())
