import math
import time

import penny.joystick_listener
import penny.components.arduino
import penny.components.ardumoto

ARDUINO_PORT = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Uno_75633313233351C09072-if00'
ACTIVE_LIGHT_PIN = 10

def clamp(lower, upper, value):
    return min(upper, max(lower, value))


def main():
    joystick = penny.joystick_listener.JoystickListener()
    joystick.start()
    arduino = penny.components.arduino.Arduino(ARDUINO_PORT)
    arduino.open()
    # TODO: Fix arduino so it sends a "ready" message.
    time.sleep(3)
    
    # Turn on active light.
    arduino.pin_mode(ACTIVE_LIGHT_PIN, arduino.OUTPUT)
    arduino.digital_write(ACTIVE_LIGHT_PIN, 1)

    motors = penny.components.ardumoto.Ardumoto(arduino)

    try:
        while True:
            y_axis = joystick.state.get('axis', {}).get('1', 0.0)
            x_axis = joystick.state.get('axis', {}).get('0', 0.0)
            high_drive = joystick.state.get('buttons', {}).get('0', False)
            
            # Drop any input lower than a certain threshold,
            # essentially giving the joysticks a "deadzone".
            if abs(y_axis) < 0.1:
                y_axis = 0.0
            if abs(x_axis) < 0.1:
                x_axis = 0.0
        
            # Basic arcade drive - when the stick is forward or backwards
            # both wheels go in the same direction. When the stick is
            # left or right, the wheels go in opposite directions to
            # turn.
            left_basis = y_axis + x_axis
            right_basis = y_axis - x_axis
            # Note: squaring the input gives a smoother curve for output,
            # much nicer for controlling motors.
            left_speed = clamp(
                -1.0, 1.0,
                math.copysign(math.pow(left_basis, 2.0), left_basis))
            right_speed = clamp(
                -1.0, 1.0,
                math.copysign(math.pow(right_basis, 2.0), right_basis))
            
            # Allow "high" and "low" drive modes - the little motors have
            # some juice!
            if not high_drive:
                left_speed *= 0.2
                right_speed *= 0.2
            
            motors.drive_normalized(motors.A, left_speed)
            motors.drive_normalized(motors.B, -right_speed)

    finally:
        # Cleanup and stop the motors.
        joystick.stop()
        motors.stop(motors.B)
        motors.stop(motors.A)
        arduino.digital_write(ACTIVE_LIGHT_PIN, False)
        arduino.close()
        

if __name__ == '__main__':
    main()