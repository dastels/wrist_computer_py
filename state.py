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

try:
    import adafruit_logging as logging
except ModuleNotFoundError:
    import logging

logger = logging.getLogger("state")


class State(object):
    def __init__(self, name, machine):
        self._name = name
        self._machine = machine
        if machine is not None:
            machine.add_state(self)

    @property
    def name(self):
        return self._name

    def is_named(self, name):
        return self._name == name

    @property
    def nested(self):
        return False

    @property
    def fullname(self):
        if self._machine is None:
            return self._name
        else:
            return "{0} - {1}".format(self._machine.name, self._name)

    def _go_to(self, state_name):
        self._machine.go_to_state(state_name)

    def enter(self):
        logger.debug("Entering %s", self.fullname)

    def exit(self):
        logger.debug("Exiting %s", self.fullname)

    def handle_event(self, event):
        logger.debug("%s handling %s", self.fullname, event.description)
        return event.dispatch(self)

    def handle_button_0(self, action):
        return None

    def handle_button_1(self, action):
        return None

    def handle_button_2(self, action):
        return None

    def handle_button_3(self, action):
        return None

    def handle_button_up(self, action):
        return None

    def handle_button_right(self, action):
        return None

    def handle_button_down(self, action):
        return None

    def handle_button_left(self, action):
        return None

    def handle_button_a(self, action):
        return None

    def handle_button_b(self, action):
        return None

    def handle_touch(self, touch):
        return None

    def handle_tick(self, now):
        return None
