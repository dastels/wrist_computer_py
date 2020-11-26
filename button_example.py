# The MIT License (MIT)
#
# Copyright (c) 2019 Dave Astels
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_debouncer import Debouncer
from adafruit_bno055 import BNO055_I2C

UNKNOWN = 0
HELD_LEVEL = 1
ARM_HANGING = 2
UP_VIEWING = 3

ORIENTATION_NAMES = ["Unknown", "Level", "Hanging", "Viewing"]

current_orientation = UNKNOWN

# Reset the MCP23017

reset_23017 = DigitalInOut(board.D3)
reset_23017.direction = Direction.OUTPUT
reset_23017.value = True
time.sleep(0.050)
reset_23017.value = False
time.sleep(0.050)
reset_23017.value = True

i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)
sensor = BNO055_I2C(i2c)


def make_debounced_button(button_pin):
    pin = mcp.get_pin(button_pin)
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP
    return Debouncer(pin)


def orientation(old_orientation, gravity):
    """Returns the new orientation and whether it just changed"""
    x, y, z = gravity
    # print(gravity)
    if z > 5.0 and abs(x) < 5.0 and abs(y) < 5.0:
        new_orientation = HELD_LEVEL
    elif x > 5.0 and abs(z) < 5.0 and abs(y) < 5.0:
        new_orientation = ARM_HANGING
    elif y < -5.0 and abs(x) < 5.0 and abs(z) < 5.0:
        new_orientation = UP_VIEWING
    else:
        new_orientation = old_orientation

    return new_orientation, new_orientation != old_orientation


# Make a list of all the pins (a.k.a 0-15)
pins = []
for pin in range(0, 16):
    pins.append(make_debounced_button(pin))

bno_time = 0.0
BNO_INTERVAL = 1.0
while True:
    for button in pins:
        button.update()

    now = time.monotonic()
    if now >= bno_time:
        bno_time = now + BNO_INTERVAL
        print(sensor.temperature, "C")
    current_orientation, orientation_changed = orientation(
        current_orientation, sensor.gravity
    )
    if orientation_changed:
        print("New orientation is", ORIENTATION_NAMES[current_orientation])

    for num, button in enumerate(pins):
        if button.fell:
            print("Button #", num, "pressed!")
        elif button.rose:
            print("Button #", num, "released!")
