"""Component for interacting with an Arduino running Penny firmware over
serial."""

import struct

import serial


INPUT = 0
INPUT_PULLUP = 1
OUTPUT = 2


class Arduino:
    """Controls an Ardiuno daughterboard running Penny firmware via serial."""
    DEFAULT_BAUD_RATE = 9600

    def __init__(self, serial_port: str):
        self._serial = serial.Serial()
        self._serial.baudrate = self.DEFAULT_BAUD_RATE
        self._serial.port = serial_port

    def open(self):
        self._serial.open()
        return self

    def close(self) -> None:
        self._serial.close()

    def __enter__(self):
        self.open()

    def __exit__(self, *exc):
        self.close()

    def _send(self, message: bytes) -> None:
        self._serial.write(message)

    def _recv(self, num: int) -> bytes:
        return self._serial.read(num)

    def digital_read(self, pin: int) -> bool:
        self._serial.write(b'R' + struct.pack('B', pin))
        data = self._recv(1)
        result, = struct.unpack('B', data)
        return result

    def digital_write(self, pin: int, state: bool) -> None:
        self._send(b'W' + struct.pack('BB', pin, state))

    def pin_mode(self, pin: int, mode: int) -> None:
        data = b'M' + struct.pack('BB', pin, mode)
        self._send(data)

    def analog_write(self, pin: int, value: int) -> None:
        self._send(b'A' + struct.pack('BB', pin, value))
