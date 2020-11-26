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
import displayio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_debouncer import Debouncer
from adafruit_bno055 import BNO055_I2C
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from menu import MenuItem, Menu
from state_machine import StateMachine
from state import State
from menu_state import MenuState
from events import *
from adafruit_pyportal import PyPortal


UNKNOWN = 0
HELD_LEVEL = 1
ARM_HANGING = 2
UP_VIEWING = 3

ORIENTATION_NAMES = ["Unknown", "Level", "Hanging", "Viewing"]

current_orientation = UNKNOWN

pyportal = PyPortal()

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

# --------------- Fonts ----------------- #
font = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")
font.load_glyphs(b"abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()")

# ---------- Sound Effects ------------- #
error_sound = "/sounds/sound.wav"
beep_sound = "/sounds/beep.wav"
tab_sound = "/sounds/tab.wav"


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
def make_debounced_button(button_pin):
    pin = mcp.get_pin(button_pin)
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP
    return Debouncer(pin)


pins = []
for pin in range(0, 16):
    pins.append(make_debounced_button(pin))

button_0 = pins[0]
button_1 = pins[1]
button_2 = pins[2]
button_3 = pins[3]
button_up = pins[8]
button_right = pins[9]
button_down = pins[10]
button_left = pins[11]
button_a = pins[12]
button_b = pins[13]


def make_menu_group():
    item_height = 20
    item_count = 5
    view = displayio.Group(max_size=item_count * 2, x=0, y=40)
    for row in range(0, item_count):
        select_label = Label(font, text="", color=0x880000, max_glyphs=1)
        select_label.x = 0
        select_label.y = row * item_height
        view.append(select_label)
        item_label = Label(font, text="", color=0x000088, max_glyphs=20)
        item_label.x = 20
        item_label.y = row * item_height
        view.append(item_label)
    return view


splash = displayio.Group(max_size=10)  # The Main Display Group
menu_group = make_menu_group()
splash.append(menu_group)

top_menu = Menu(pyportal, menu_group)
sub_menu = Menu(pyportal, menu_group, top_menu)

top_menu.items = [
    MenuItem("Item 1"),
    MenuItem("Item 2"),
    MenuItem("Item 3", nested_menu=sub_menu),
    MenuItem("Item 4"),
]
sub_menu.items = [
    MenuItem("Item 3-1", function=lambda: print("boom")),
    MenuItem("Item 3-2"),
    MenuItem("Item 3-3"),
]

top_menu.reset()
sub_menu.reset()

machine = StateMachine("main")
MenuState("menu", machine, top_menu)
machine.start()


def event_loop(menu):
    while True:
        [button.update() for button in pins]

        if button_down.fell:
            machine.handle_event(ButtonDownEvent(True))
        elif button_down.rose:
            machine.handle_event(ButtonDownEvent(False))
        elif button_up.fell:
            machine.handle_event(ButtonUpEvent(True))
        elif button_up.rose:
            machine.handle_event(ButtonUpEvent(False))
        elif button_right.fell:
            machine.handle_event(ButtonRightEvent(True))
        elif button_right.rose:
            machine.handle_event(ButtonRightEvent(False))
        elif button_left.fell:
            machine.handle_event(ButtonLeftEvent(True))
        elif button_left.rose:
            machine.handle_event(ButtonLeftEvent(False))


board.DISPLAY.show(splash)
top_menu.redraw()
event_loop(top_menu)
