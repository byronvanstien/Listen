import json
import asyncio
from typing import Optional, List, Dict
import logging

import aiohttp

from listen.errors import ListenError, AuthError, KanaError
from listen.objects import User, Song, Favorite
from listen.utils import ensure_token
from listen.message import wrap_message

logger = logging.getLogger(__name__)

class Client(object):
    """
    Client class to interface with listen.moe's API
    """
    def __init__(self, *, kpop: bool = False, loop: Optional[asyncio.AbstractEventLoop] = None, reconnect: bool = True) -> None:

        self._headers: Dict[str, str] = {
            "User-Agent": "Listen (https://github.com/Yarn/Listen)",
            "Content-Type": "application/json",
            "Accept": "application/vnd.listen.v4+json",
            "library": "kpop" if kpop else "jpop",
        }

        self._loop = loop or asyncio.get_event_loop()
        self._ws = None
        self.ws_handler = None
        self._kpop = kpop
        
        self._websocket_url = 'wss://listen.moe/kpop/gateway_v2' if kpop else 'wss://listen.moe/gateway_v2'
        self._base_url = 'https://listen.moe'
        
        self.reconnect = reconnect

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    # @property
    # def headers(self) -> Dict[str, str]:
    #     return self._headers

    async def login(self, username: str, password: str) -> None:
        """|coro|\n
        Get user token for the account you're using to sign in

        :param str username: The username of the account you're getting the token for
        :param str password: The password of the account you're getting the token for
        :rtype: str
        """
        url = '{}/api/login'.format(self._base_url)
        
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.post(url, json={"username": username, "password": password}) as response:
                
                # print(await response.text())
                resp_data = await response.json()
                if response.status != 200:
                    raise AuthError(resp_data["message"])
                
                # from pprint import pprint
                # pprint(resp_data)
                # if not resp_data["success"]:
                #     raise ListenError(resp_data["message"])
                
                self._headers["authorization"] = "Bearer {}".format(resp_data["token"])
                # return self._headers["authorization"]
    
    async def get_info(self, user_name: Optional[str] = None) -> User:
        """|coro|\n
        Get a user object that is associated with the logged in user

        :rtype: :class:`listen.objects.User`
        """
        if user_name is None:
            if not self._headers.get("authorization"):
                raise KanaError("user_name is required when not logged in")
            user_name = '@me'
        url = "{}/api/users/{}".format(self._base_url, user_name)
        
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(url) as response:
                # return User(**(await response.json()))
                data = await response.json()
                user_obj = User(id=0, username=data['user']['username'], raw=data['user'])
                return user_obj

    @ensure_token
    async def get_favorites(self) -> List[Favorite]:
        """|coro|\n
        Get all favourites from the current logged in user

        :rtype: :class:`listen.objects.Song`
        """
        url = "{}/api/favorites/@me".format(self._base_url)
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(url) as response:
                # songs = []
                response_data = await response.json()
                
                favorites = [Favorite(f) for f in response_data['favorites']]
                return favorites
                
                # from pprint import pprint
                # pprint(response_data)
                # for s in response_data["favorites"]:
                #     songs.append(Favorite(s))
                #     # songs.append(Song(s.get("id"), s.get("artist-"), s.get("title"), s.get("anime-"), s.get("enabled")))
                # return songs

    @ensure_token
    async def favorite_toggle(self, song_id: int):
        """|coro|\n
        Either favourites or unfavourites a song based on if it's favourited already

        :param int song_id: The id of the song you want to favourite
        :rtype: bool
        """
        raise NotImplementedError()
        # https://listen.moe/api/favorites/4726
        # with aiohttp.ClientSession(headers=self._headers) as session:
        #     async with session.post(SONG_FAVOURITES, data=json.dumps({"song": song_id})) as response:
        #         boolean = await response.json()
        #         return boolean["favorite"]
    
    @ensure_token
    async def favorite(self, song_id: int, *, remove=False) -> None:
        pass
        async with aiohttp.ClientSession(headers=self._headers) as session:
            method = session.post if not remove else session.delete
            async with method("{}/api/favorites/{}".format(self._base_url, song_id)) as response:
                # print(response.status)
                # print(await response.json())
                if response.status != 204:
                    raise ListenError()
    
    @ensure_token
    async def remove_favorite(self, song_id: int) -> None:
        return await self.favorite(song_id, remove=True)
    
    @ensure_token
    async def make_request(self, song_id: int):
        """|coro|\n
        Requests a song for queueing

        :param int song_id: The id of the song you want to request
        :rtype: bool
        """
        raise NotImplementedError()
        # with aiohttp.ClientSession(headers=self._headers) as session:
        #     async with session.post(SONG_REQUEST, data=json.dumps({"song": song_id})) as response:
        #         requested = await response.json()
        #         return requested["success"]

    async def create_websocket_connection(self, authenticate: bool = False):
        """|coro|\n
        Creates a websocket connection to Listen.moe's socket API

        :param bool authenticate: Boolean that decides if the authentication to the API is done
        :rtype: None
        """
        url = self._websocket_url
        
        session = aiohttp.ClientSession(headers=self._headers)
        self._ws = await session.ws_connect(url)
        
        # if authenticate:
        #     msg = {"op": 0, "d": {"auth": self._headers["authorization"]}}
        # else:
        #     msg = {"op": 0, "d": {"auth": ""}}
        # await self.send_ws(msg)

    async def start(self):
        while True:
            if self._ws is None:
                await self.create_websocket_connection()
            await self._recv_loop()
            
            if self.reconnect:
                await asyncio.sleep(60)
            else:
                break
    
    async def _recv_loop(self):
        while True:
            if self.ws_handler:
                msg = await self._ws.receive()
                
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self._ws = None
                    logger.warn("websocket error {}".format(msg.data))
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    self._ws = None
                    break
                else:
                    continue
                
                if data['op'] == 0:
                    heartbeat = data['d']['heartbeat'] / 1000
                    self.loop.create_task(self._send_pings(heartbeat))
                
                if data['op'] == 10:
                    # don't send pings to handler
                    continue
                
                wrapped_message = wrap_message(data)
                await self.ws_handler(wrapped_message)
            else:
                raise RuntimeError("No function handler specified")
    
    async def send_ws(self, data):
        json_data = json.dumps(data)
        await self._ws.send_str(json_data)
    
    async def _send_pings(self, interval=45):
        while True:
            await asyncio.sleep(interval)
            msg = {
                'op': 9
            }
            await self.send_ws(msg)

    def register_handler(self, handler):
        """
        Registers a function handler to allow you to do something with the socket API data

        :param function handler: A function that takes a dictionary that contains Listen.moe's API data
        """
        self.ws_handler = handler

    def run(self):
        """
        Start the connection to the socket API
        """
        # self.loop.run_until_complete(self.create_websocket_connection())
        self.loop.run_until_complete(self.start())
        # self.loop.close()
