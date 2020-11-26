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


class StateMachine(object):
    def __init__(self, name):
        self._name = name
        self._states = {}
        self._start_state = None
        self._current_state = None

    @property
    def name(self):
        return self._name

    @property
    def current_state(self):
        return self._current_state

    @property
    def current_state_name(self):
        return "None" if self._current_state is None else self._current_state.name

    # Clean up when exiting a nested machine
    def exit(self):
        if self._current_state:
            self._current_state.exit()
            self._current_state = None

    def handle_event(self, event):
        if self._current_state:
            result = self._current_state.handle_event(event)
            if result:
                self.exit()
            return result
        else:
            return None

    def add_state(self, state, is_start_state=False):
        if state.name in self._states:
            logger.critical("Duplicate state name %s in %s", state.name, self._name)
            exit()
        self._states[state.name] = state
        if len(self._states) == 1 or is_start_state:
            self._start_state = state.name

    def start(self):
        if self._start_state:
            self.go_to_state(self._start_state)

    def go_to_state(self, state_name):
        logger.debug("%s -> %s", self._name, state_name)
        if state_name not in self._states:
            logger.critical("State %s isn't in machine %s", state_name, self._name)
            exit()
        if self._current_state:
            self._current_state.exit()
        self._current_state = self._states[state_name]
        self._current_state.enter()
