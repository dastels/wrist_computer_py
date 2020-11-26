import pytest
from events import Button0Event
from state import State
from state_machine import StateMachine


class State1(State):
    def handle_button_0(self, action):
        self._go_to("S2")


class State2(State):
    def handle_button_0(self, action):
        self._go_to("S1" if action else "S3")


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


def test_starting(machine):
    machine.start()
    assert machine.current_state.is_named("S1")


def test_1_transition(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    assert machine.current_state.is_named("S2")


def test_looping_transitions(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    machine.handle_event(Button0Event(True))
    assert machine.current_state.is_named("S1")


def test_branching_transitions(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    machine.handle_event(Button0Event(False))
    assert machine.current_state.is_named("S3")


def test_branching_return_transitions(machine):
    machine.start()
    machine.handle_event(Button0Event(True))
    machine.handle_event(Button0Event(False))
    machine.handle_event(Button0Event(True))
    assert machine.current_state.is_named("S1")
