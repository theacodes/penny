#!/usr/bin/env python

import asyncio
import datetime
import functools
import json
import random
import time
import threading

import websockets


class BackgroundServer:
    def __init__(self, callback, host, port):
        self._callback = callback
        self._host = host
        self._port = port
        self._thread_loop = asyncio.new_event_loop()
        self._stop_event = asyncio.Event(loop=self._thread_loop)
        self._thread = None

    def start(self):
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._thread_main)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._thread_loop.call_soon_threadsafe(self._stop_event.set)
        self._thread.join()
        self._thread = None

    async def _serve(self):
        serve = websockets.serve(
            self._callback, self._host, self._port)
        async with serve:
            await self._stop_event.wait()

    def _thread_main(self):
        asyncio.set_event_loop(self._thread_loop)
        self._thread_loop.run_until_complete(self._serve())
