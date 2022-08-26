from os import _exit
from zlib import decompress
import asyncio
import websockets
import json

class Transport:

    async def on_message(self, websocket):
        try:
            self.on_connect(websocket)

            print("connected")
            # await websocket.send("hello")
            async for message in websocket:
                 print(message)

        except Exception as er:
            print(er)
        finally:
            self.on_disconnect(websocket)
            print("Disconnected")

    def __init__(self, port, on_connect, on_disconnect ):
        try:
            print("Listening on", port)
            self.port = port
            self.on_connect = on_connect
            self.on_disconnect = on_disconnect

            self.start_server = websockets.serve(
                self.on_message, "0.0.0.0", self.port)
            asyncio.get_event_loop().run_until_complete(self.start_server)
            asyncio.get_event_loop().run_forever()
        finally:
            pass


