#!/usr/bin/env python

import asyncio
import datetime
import functools
import json
import random
import time
import threading

import websockets

from penny import _websockets


# TODO: Consider composition over inheritance.
class JoystickListener(_websockets.BackgroundServer):
    def __init__(self):
        super(JoystickListener, self).__init__(
            self._callback, '0.0.0.0', 5678)
        self.joysticks = {}

    async def _callback(self, websocket, path):
        while True:
            try:
                data = await websocket.recv()
                self.joysticks = json.loads(data)
            except websockets.ConnectionClosed:
                print('disconnected')
                break
