"""Component for interacting with an Ardumoto board attached to an Arduino."""

import math

from penny.components import arduino


A = 0
B = 1
FORWARD = 0
REVERSE = 1

_PWMA = 3
_PWMB = 4
_DIRA = 2
_DIRB = 4


class Ardumoto:
    def __init__(self, arduino: arduino.Arduino):
        self._arduino = arduino
        self._arduino.pin_mode(PWMA, arduino.PinMode.OUTPUT)
        self._arduino.pin_mode(DIRA, arduino.PinMode.OUTPUT)
        self._arduino.pin_mode(PWMB, arduino.PinMode.OUTPUT)
        self._arduino.pin_mode(DIRB, arduino.PinMode.OUTPUT)

    def drive(self, motor: int, speed: int, direction: int) -> None:
        pwm_pin = _PWMA if motor == A else _PWMB
        dir_pin = _DIRA if motor == A else _DIRB

        self._arduino.digital_write(dir_pin, direction)
        self._arduino.analog_write(pwm_pin, speed)

    def drive_normalized(self, motor: int, speed: float) -> None:
        if speed >= 0:
            direction = FORWARD
        else:
            direction = REVERSE

        pwm_speed = abs(math.floor(speed * 255))

        self.drive(motor, pwm_speed, direction)

    def stop(self, motor: int):
        self.drive(motor, 0, FORWARD)
