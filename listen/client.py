import json
import aiohttp

from listen.errors import ListenError
from listen.objects import User, Song
from listen.utils import ensure_token
from listen.constants import (
    AUTH_URL,
    USER,
    USER_FAVOURITES,
    SONG_FAVOURITES,
    SONG_REQUEST
)


class Client(object):
    """
    Client class to interface with listen.moe's API
    """
    def __init__(self):
        self._user_agent = "Listen (https://github.com/GetRektByMe/Listen)"
        self._headers = {
            "User-Agent": self._user_agent,
            "Content-Type": "application/json"
        }

    @property
    def user_agent(self):
        return self._user_agent

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
