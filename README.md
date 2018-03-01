# Listen
An API wrapper for listen.moe built upon the websockets library and aiohttp.

Currently only recieving song updates via websocket is tested/maintained.

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
        for x in msg.sources + msg.artists + msg.albums:
            print(" ", x)
    else:
        print(msg.raw)

cl = listen.client.Client()
cl.register_handler(hand)
cl.run()
```

---

## Docs (out of date)
You can find our docs [here](http://listen.readthedocs.io/en/latest/)
