
from typing import List, Any

from .message import Artist, Album, Source

class User(object):
    def __init__(self, id: int, username: str, raw) -> None:
        self.id: int = id
        self.username: str = username
        self.raw: Any = raw

    def __repr__(self):
        return "<{0.username}:{0.id}>".format(self)

    def __str__(self):
        return self.username


class Song(object):
    def __init__(self, id: int, artist: str, title: str, anime: str, enabled: bool) -> None:
        self.id = id
        self.artist = artist
        self.title = title
        self.anime = anime
        self.enabled = enabled

    def __repr__(self):
        return "<{0.title}:{0.artist}>".format(self)

    def __str__(self):
        return self.title

class Favorite:
    def __init__(self, raw):
        self._raw = raw
        
        self.title: str = raw['title']
        self.id: int = raw['id']
        self.artists: List[Artist] = []
        self.albums: List[Album] = []
        self.sources: List[Source] = []
        
        for album in raw['albums']:
            self.albums.append(Album(album))
        for source in raw['sources']:
            self.sources.append(Source(source))
        for artist in raw['artists']:
            self.artists.append(Artist(artist))
    
    def __repr__(self):
        return "<Favorite {0.id}:{0.title}:{0.artists}>".format(self)

    def __str__(self):
        return "{}:{}".format(self.id, self.title)
