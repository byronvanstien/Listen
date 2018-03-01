from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, List, Optional

class Type(Enum):
    SONG_INFO = auto()
    POST_AUTH = auto()
    UNKNOWN = auto()

# re-export varients of Type
for _name, _member in Type.__members__.items():
    locals()[_name] = _member

class BaseMessage(ABC):
    
    @property
    @abstractmethod
    def raw(self) -> Any:
        pass
    
    @property
    @abstractmethod
    def op(self) -> int:
        pass
    
    @property
    @abstractmethod
    def type(self) -> Type:
        pass

class Message(BaseMessage):
    def __init__(self, raw):
        self._raw_data = raw
    
    @property
    def raw(self):
        return self._raw_data
    
    @property
    def op(self):
        return self._raw_data['op']
    
    @property
    def type(self):
        return Type.UNKNOWN

class Album:
    def __init__(self, raw):
        self._raw = raw
        self.id: int = raw['id']
        self.name: Optional[str] = raw['name']
        self.name_romaji: Optional[str] = raw['nameRomaji']
        self.image: Optional[str] = raw['image']
    
    def __repr__(self):
        return "Album({}, {})".format(self.name, self.name_romaji)

class Artist:
    def __init__(self, raw):
        self._raw = raw
        self.id: int = raw['id']
        self.name: Optional[str] = raw['name']
        self.image: Optional[str] = raw['image']
        self.name_romaji: Optional[str] = raw['nameRomaji']
    
    def __repr__(self):
        return "Artist({}, {})".format(self.name, self.name_romaji)

class Source:
    def __init__(self, raw):
        self._raw = raw
        self.id: int = raw['id']
        self.name: Optional[str] = raw['name']
        self.image: Optional[str] = raw['image']
        self.name_romaji: Optional[str] = raw['nameRomaji']
    
    def __repr__(self):
        return "Source({}, {})".format(self.name, self.name_romaji)

class SongUpdate(Message):
    
    def __init__(self, raw):
        super().__init__(raw)
        self.title: str = raw['d']['song']['title']
        self.id: int = raw['d']['song']
        self.artists: List[Artist] = []
        self.albums: List[Album] = []
        self.sources: List[Source] = []
        
        for album in raw['d']['song']['albums']:
            self.albums.append(Album(album))
        for source in raw['d']['song']['sources']:
            self.albums.append(Source(source))
        for artist in raw['d']['song']['artists']:
            self.artists.append(Artist(artist))
    
    @property
    def type(self):
        return Type.SONG_INFO
    
    def __repr__(self):
        return "SongUpdate({})".format(self.title)

def wrap_message(data):
    op = data['op']
    if op == 1 and data['t'] == 'TRACK_UPDATE':
        song_update = SongUpdate(data)
        return song_update
    else:
        return Message(data)
