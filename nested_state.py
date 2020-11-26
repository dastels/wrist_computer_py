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

from state import State
from state_machine import StateMachine


class NestedState(State):
    def __init__(self, name, machine):
        super().__init__(name, machine)
        self._nested_machine = StateMachine("{0}-nested-machine".format(name))

    @property
    def nested(self):
        return True

    @property
    def current_state(self):
        return self._nested_machine.current_state

    def enter(self):
        super().enter()
        self._nested_machine.start()

    def handle_event(self, event):
        new_state = self._nested_machine.handle_event(event)
        if new_state is not None:
            self._go_to(new_state)
