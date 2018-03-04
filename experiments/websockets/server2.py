#!/usr/bin/env python

import asyncio
import datetime
import functools
import json
import random
import time
import threading

import websockets


class JoystickListener:
    def __init__(self):
        self._joystick_state = {}
        self._thread_loop = asyncio.new_event_loop()
        self._stop = asyncio.Future(loop=self._thread_loop)
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._thread_main)
        self._thread.daemon = True
        self._thread.start()
        
    def stop(self):
        self._thread_loop.call_soon_threadsafe(
            functools.partial(self._stop.set_result, None))
        self._thread.join()
        self._thread = None

    async def _websocket_listener(self, websocket, path):
        while True:
            try:
                recv_state = await websocket.recv()
                self._joystick_state = json.loads(recv_state)
            except websockets.ConnectionClosed:
                print('disconnected')

    async def _serve_websockets(self):
        serve = websockets.serve(
            self._websocket_listener, '127.0.0.1', 5678)
        async with serve:
            await self._stop

    def _thread_main(self):
        asyncio.set_event_loop(self._thread_loop)
        self._thread_loop.run_until_complete(self._serve_websockets())




listener = JoystickListener()
listener.start()

try:
    while True:
        time.sleep(1)
        print(listener._joystick_state)
except KeyboardInterrupt:
    listener.stop()

