# Penny

The goal of Penny is to be an approachable, extensible, and easy to learn robotics platform. It's for me to make various robots and use as an example to help teach digital electronics, but it could eventually be generalized. To that end, it is aimed at students, hobbyists, and robotics club mentors.

## Core tenants

Penny *must*:

* Be completely open-source under permissive license (Apache 2.0).
* Use open hardware.
* Use open protocols for communication.
* Allow the use of custom components out of the box.
* Be controller-hardware agnostic - we will start with Raspberry Pi, but it should be able to work on any Linux minicomputer with a little effort (hopefully just configuration).
* Be programmable from a web browser - it should be possible to program a robot
using just a Chromebook.
* Focus on students and education, not aim to be a professional robotics platform.

## What does robot code look like?

Penny should be *extremely easy* to develop for. There are a few options, and
I should consider supporting a few of them. Regardless of the approach,
the main entrypoint for the robot is `robot.py`.

We could adopt the Arduino style:

```python
import time

start_time = 0


def setup(robot):
    start_time = time.now()


def loop(robot):
    left_motor = robot.motors['left']
    right_motor = robot.motors['right']

    if time.now() < start_time + 60:
        left_motor.speed = 100
        right_motor.speed = 100
    else:
        left_motor.speed = 100
        right_motor.speed = 100
```


Or we can leave it completely open-ended:

```python
import time

import penny

robot = penny.Robot()
start_time = time.now()


while True:
    left_motor = robot.motors['left']
    right_motor = robot.motors['right']

    if time.now() < start_time + 60:
        left_motor.speed = 100
        right_motor.speed = 100
    else:
        left_motor.speed = 100
        right_motor.speed = 100
```

## Configuration

FRC's Java libraries make you add robot components in your robot code, for example:

```java
public class Robot extends IterativeRobot {

//Defines the variables as members of our Robot class
     RobotDrive myRobot;
     Joystick stick;
     Timer timer;

//Initializes the variables in the robotInit method, this method is called when the robot is initializing
     public void robotInit() {
          myRobot = new RobotDrive(0,1);
          stick = new Joystick(1);
          timer = new Timer();
     }
}
```

Student Robotics, on the other hand, is clever enought to discover most connected components and expose them for you automatically:

```python
from sr.robot import *

R = Robot()

# motor board 0, channel 0 to full power forward
R.motors[0].m0.power = 100
```

Penny should work to strike a reasonable balance. By default, Penny will not
automatically configure anything. You will have the option to attach components
to your robot programmically like this:

```python
import penny
import penny.components.motors


robot = penny.Robot()
drive_motors = penny.components.motors.ArduinoMotorBoard(
    'serialno://13456')

drive_motors.one.speed = 100
```

Or via a `robot.yaml` file, which Penny will use to automatically attach components to the `Robot` object when it's constructed:

```yaml
components:
    name: drive_motors
    type: penny.components.motors.ArduinoMotorBoard
    url: serialno://12356
```

In the robot code:

```python
import penny

robot = penny.Robot()
robot.components.drive_motors.one.speed = 100
```

## Uploading code

There's a few ways we could make it possible to upload robot code:

1. Through a usb stick attached to the Raspberry Pi.
2. Via uploading the code to the Raspberry Pi through a web interface.
3. By dropping the code on the Raspberry Pi SD card.

We could support all three with an order on precedence.

The web interface is the most interesting one. We could use JupyterHub to give students a full IDE-like experience for developing and experimenting with their robot.


## Controlling the robot remotely

This gets a bit complex. We need to allow multiple "Driver Station" like pieces of software- mostly because we need to support multiple operating systems *and* a web-browser interface.

We could use something like `pygame`, which is a wrapper on top of SDL, to get joystick/keyboard/mouse input in a cross-platform manner. There is even a web port of pygame so we can use WebAssembly and share most of the code.

On the robot side, we could create an open protocol for communicating driver station signals to the robot itself (such as a simple HTTP API). How we expose that to the robot code is also interesting. We could do something very simple like:

```python
driver_station = penny.DriverStation()

while True:
    if driver_station.joystick[0].y_axis > 0:
        drive_motors.one.speed = 100
    elif driver_station.joystick[0].y_aix < 0:
        drive_motors.one.speed = -100
    else:
        drive_motors.one.speed = 0
```

We could also expose callback-based input:

```python
def activate_pusher():
    robot.components.solenoids['pusher'].toggle()

driver_station.on_button_down(penny.BUTTON_ONE, active_pusher)
```

The driver station should be completely optional. It should be possible to build standalone, autonomous robots.
