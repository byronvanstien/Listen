class User(object):
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username

    def __repr__(self):
        return "<{0.username}:{0.id}>".format(self)

    def __str__(self):
        return self.username


class Song(object):
    def __init__(self, id: int, artist: str, title: str, anime: str, enabled: bool):
        self.id = id
        self.artist = artist
        self.title = title
        self.anime = anime
        self.enabled = enabled

    def __repr__(self):
        return "<{0.title}:{0.artist}>".format(self)

    def __str__(self):
        return self.title
