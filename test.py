import time

import penny.dashboard


dashboard = penny.dashboard.Dashboard()

while True:
    time.sleep(1)
    print(dashboard.gamepad)
