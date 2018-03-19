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

if you already having something running on the event loop Client.run won't work

replace `cl.run()` with
```python
await cl.create_websocket_connection()
cl.loop.create_task(cl.start())
```

---

## Docs (out of date)
You can find our docs [here](http://listen.readthedocs.io/en/latest/)
