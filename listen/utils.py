from functools import wraps

from listen.errors import KanaError


def ensure_token(func):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        if not self._headers["authorization"]:
            raise KanaError("Token doesn't exist!")
        return await func(self, *args, **kwargs)
    return wrapped
