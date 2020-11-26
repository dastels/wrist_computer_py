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


class Event(object):
    def __init__(self):
        pass

    @property
    def description(self):
        return "unknown"

    def dispatch(self, target):
        return None


class ButtonEvent(Event):
    def __init__(self, label, action):
        super().__init__()
        self._label = label
        self._action = action

    def _action_to_string(self):
        return

    @property
    def description(self):
        return "Button {0} {1}".format(
            self._label, "pressed" if self._action else "released"
        )


class Button0Event(ButtonEvent):
    def __init__(self, action):
        super().__init__("0", action)

    def dispatch(self, target):
        return target.handle_button_0(self._action)


class Button1Event(ButtonEvent):
    def __init__(self, action):
        super().__init__("1", action)

    def dispatch(self, target):
        return target.handle_button_1(self._action)


class Button2Event(ButtonEvent):
    def __init__(self, action):
        super().__init__("2", action)

    def dispatch(self, target):
        return target.handle_button_2(self._action)


class Button3Event(ButtonEvent):
    def __init__(self, action):
        super().__init__("3", action)

    def dispatch(self, target):
        return target.handle_button_3(self._action)


class ButtonUpEvent(ButtonEvent):
    def __init__(self, action):
        super().__init__("Up", action)

    def dispatch(self, target):
        return target.handle_button_up(self._action)


class ButtonRightEvent(ButtonEvent):
    def __init__(self, action):
        super().__init__("Right", action)

    def dispatch(self, target):
        return target.handle_button_right(self._action)


class ButtonDownEvent(ButtonEvent):
    def __init__(self, action):
        super().__init__("Down", action)

    def dispatch(self, target):
        return target.handle_button_down(self._action)


class ButtonLeftEvent(ButtonEvent):
    def __init__(self, action):
        super().__init__("Left", action)

    def dispatch(self, target):
        return target.handle_button_left(self._action)


class ButtonAEvent(ButtonEvent):
    def __init__(self, action):
        super().__init__("A", action)

    def dispatch(self, target):
        return target.handle_button_a(self._action)


class ButtonBEvent(ButtonEvent):
    def __init__(self, action):
        super().__init__("B", action)

    def dispatch(self, target):
        return target.handle_button_b(self._action)


class TouchEvent(Event):
    def __init__(self, touch):
        """touch can be a touch point or None if touch has ended"""
        super().__init__()
        self._touch = touch

    @property
    def description(self):
        return "Touch {0}".format(
            "ended" if self._touch is None else "at {0}".format(self._touch)
        )

    def dispatch(self, target):
        return target.handle_touch(self._touch)


class TickEvent(Event):
    def __init__(self):
        super().__init__()

    @property
    def description(self):
        return "Tick"

    def dispatch(self, target):
        return target.handle_tick(time.monotonic())
