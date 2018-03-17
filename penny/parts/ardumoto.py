"""Component for interacting with an Ardumoto board attached to an Arduino."""

import math

import penny.parts.arduino

_PWMA = 3
_PWMB = 11
_DIRA = 2
_DIRB = 4


class Ardumoto:
    A = 0
    B = 1
    FORWARD = 0
    REVERSE = 1

    def __init__(self, arduino: penny.components.arduino.Arduino):
        self._arduino = arduino
        self._arduino.pin_mode(_PWMA, arduino.OUTPUT)
        self._arduino.pin_mode(_DIRA, arduino.OUTPUT)
        self._arduino.pin_mode(_PWMB, arduino.OUTPUT)
        self._arduino.pin_mode(_DIRB, arduino.OUTPUT)

    def drive(self, motor: int, speed: int, direction: int) -> None:
        pwm_pin = _PWMA if motor == self.A else _PWMB
        dir_pin = _DIRA if motor == self.A else _DIRB

        self._arduino.digital_write(dir_pin, direction)
        self._arduino.analog_write(pwm_pin, speed)

    def drive_normalized(self, motor: int, speed: float) -> None:
        if speed >= 0:
            direction = self.FORWARD
        else:
            direction = self.REVERSE

        pwm_speed = abs(math.floor(speed * 255))

        self.drive(motor, pwm_speed, direction)

    def stop(self, motor: int):
        self.drive(motor, 0, self.FORWARD)
