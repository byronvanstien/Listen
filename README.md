# Listen
An API wrapper for listen.moe built upon the websockets library and aiohttp.

Targets python >3.5

This project: https://github.com/Yarn/Listen
This is essentially a rewrite of https://github.com/GetRektByMe/Listen

The api provided is unstable and subject to change

---

## Install
```bash
pip install git+https://github.com/Yarn/Listen.git
```

---

## Example

```python
import listen

async def hand(msg):
    if msg.type == listen.message.SONG_INFO:
        print(msg)
        print(msg.title)
        for x in msg.sources + msg.artists + msg.albums:
            print(" ", x)
    else:
        print(msg.raw)

cl = listen.client.Client()
# pass your loop into Client if you aren't using the event loop returned by asyncio.get_event_loop()
# cl = listen.client.Client(loop)
cl.register_handler(hand)
cl.run()
```

if the event loop is already running you will need to
replace `cl.run()` with
```python
cl.loop.create_task(cl.start())
```

you can get updates for kpop by setting `kpop=True`
```python
cl = listen.client.Client(kpop=True)
```

---

# Docs (out of date)

These are the docs for https://github.com/GetRektByMe/Listen

The api has mostly changed so most of the documentation won't be applicable to this repo

You can find our docs [here](http://listen.readthedocs.io/en/latest/)

# Support

Ping Nyar#3343 in the #development channel on the
Listen.moe [discord](https://listen.moe/discord) or
[open an issue](https://github.com/Yarn/Listen/issues)
if you find a bug, need a new feature or want some documentation.
