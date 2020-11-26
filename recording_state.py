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

"""This state is used to record events dispatched to it"""

from state import State


class RecordingState(State):
    def __init__(self):
        super().__init__("recording", None)
        self._handled_events = []

    def _record(self, event_type, event_data):
        self._handled_events.append((event_type, event_data))

    def handled(self, event_type, event_data):
        return (event_type, event_data) in self._handled_events

    def handle_button_0(self, action):
        self._record("Button 0", action)

    def handle_button_1(self, action):
        self._record("Button 1", action)

    def handle_button_2(self, action):
        self._record("Button 2", action)

    def handle_button_3(self, action):
        self._record("Button 3", action)

    def handle_button_up(self, action):
        self._record("Button Up", action)

    def handle_button_right(self, action):
        self._record("Button Right", action)

    def handle_button_down(self, action):
        self._record("Button Down", action)

    def handle_button_left(self, action):
        self._record("Button Left", action)

    def handle_button_a(self, action):
        self._record("Button A", action)

    def handle_button_b(self, action):
        self._record("Button B", action)

    def handle_touch(self, touch):
        self._record("Touch", touch)
