#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets

async def controller(websocket, path):
    while True:
        state = await websocket.recv()
        print(state)

start_server = websockets.serve(controller, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
