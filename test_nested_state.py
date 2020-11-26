import pytest
from events import Button0Event
from state import State
from nested_state import NestedState
from state_machine import StateMachine

try:
    import adafruit_logging as logging
except ModuleNotFoundError:
    import logging

logger = logging.getLogger("state")
logger.setLevel(10)


class State1(State):
    def handle_button_0(self, action):
        self._go_to("S2")


class State4(State):
    def handle_button_0(self, action):
        self._go_to("S5")


class State5(State):
    def handle_button_0(self, action):
        return "S3"


class State2(NestedState):
    def __init__(self, name, machine):
        super().__init__(name, machine)
        State4("S4", self._nested_machine)
        State5("S5", self._nested_machine)


class State3(State):
    def handle_button_0(self, action):
        self._go_to("S1")


@pytest.fixture
def machine():
    m = StateMachine("M")
    State1("S1", m)
    State2("S2", m)
    State3("S3", m)
    return m


def test_entering_nested_state(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    assert machine.current_state.is_named("S2")
    assert machine.current_state.current_state.is_named("S4")


def test_moving_in_nested_machine(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    machine.handle_event(Button0Event(True))
    assert machine.current_state.is_named("S2")
    assert machine.current_state.current_state.is_named("S5")


def test_returning_from_nested_state(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    machine.handle_event(Button0Event(True))
    machine.handle_event(Button0Event(True))
    assert machine.current_state.is_named("S3")
