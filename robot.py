import math

from penny import joystick_listener
from penny.components import arduino
from penny.components import ardumoto

ARDUINO_PORT = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Uno_75633313233351C09072-if00'


def clamp(lower, upper, value):
    return min(upper, max(lower, value))


def main():
    joystick = joystick_listener.JoystickListener()
    joystick.start()
    ard = arduino.Arduino(ARDUINO_PORT)
    ard.open()
    
    ard.pin_mode(13, arduino.OUTPUT)
    ard.digital_write(13, True)

    motors = ardumoto.Ardumoto(ard)

    try:
        while True:
            y_axis = joystick.state.get('axis', {}).get('1', 0.0)
            x_axis = joystick.state.get('axis', {}).get('0', 0.0)
            high_drive = joystick.state.get('buttons', {}).get('0', False)
            if abs(y_axis) < 0.1:
                y_axis = 0.0
            if abs(x_axis) < 0.1:
                x_axis = 0.0
        
            left_basis = y_axis + x_axis
            right_basis = y_axis - x_axis
            left_speed = clamp(-1.0, 1.0, math.copysign(math.pow(left_basis, 2.0), left_basis))
            right_speed = clamp(-1.0, 1.0, math.copysign(math.pow(right_basis, 2.0), right_basis))
            
            if not high_drive:
                left_speed *= 0.2
                right_speed *= 0.2
            
            motors.drive_normalized(ardumoto.A, left_speed)
            motors.drive_normalized(ardumoto.B, -right_speed)

    finally:
        joystick.stop()
        motors.stop(ardumoto.B)
        motors.stop(ardumoto.A)
        ard.digital_write(13, False)
        ard.close()
        

if __name__ == '__main__':
    main()