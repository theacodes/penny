import json

from penny import _websockets
import websockets


GAMEPAD_LISTENER_PORT = 5678


class Gamepad:
    def __init__(self):
        self._state: dict = {}

    def update(self, state: dict):
        self._state.update(state)

    @property
    def num_axes(self):
        return len(self._state.get('axes', []))

    @property
    def num_buttons(self):
        return len(self._state.get('buttons', {}))

    def __getattr__(self, key: str):
        if key.startswith('axis_'):
            axis = int(key[len('axis_'):])
            axes = self._state.get('axes', [])
            try:
                return axes[axis]
            except IndexError:
                return 0.0
        elif key.startswith('button_'):
            button = key[len('button_'):]
            return self._state.get('buttons', {}).get(button, False)
        else:
            raise AttributeError

    def __unicode__(self):
        axes = [getattr(self, f'axis_{n}') for n in range(0, self.num_axes)]
        buttons = [
            getattr(self, f'button_{n}') for n in range(0, self.num_buttons)]
        return f'<Gamepad axes={axes} buttons={buttons}>'

    __str__ = __unicode__


class Dashboard:
    def __init__(self, open=True):
        self.gamepad_0 = Gamepad()
        self.gamepad_1 = Gamepad()
        self.gamepad_2 = Gamepad()
        self.gamepad_3 = Gamepad()
        self._gamepad_server = _websockets.BackgroundServer(
            self._gamepad_server_handler, '0.0.0.0', GAMEPAD_LISTENER_PORT)
        if open:
            self.open()

    def open(self):
        self._gamepad_server.start()

    def close(self):
        self._gamepad_server.stop()

    @property
    def gamepad(self) -> Gamepad:
        """Alias for gamepad_0."""
        return self.gamepad_0

    async def _gamepad_server_handler(self, websocket, path):
        while True:
            try:
                data = json.loads(await websocket.recv())
                for key, value in data.items():
                    attr = f'gamepad_{key}'
                    if hasattr(self, attr):
                        getattr(self, attr).update(value)
                    else:
                        # TODO
                        print(f'weird, tried to update {attr}')
            except websockets.ConnectionClosed:
                break
