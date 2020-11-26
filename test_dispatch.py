import pytest
from events import *


@pytest.fixture
def recording_state():
    """Return an empty recording state that records everything dispatched to it"""
    import recording_state

    return recording_state.RecordingState()


def test_pressed_button_0_dispatch(recording_state):
    recording_state.handle_event(Button0Event(True))
    assert recording_state.handled("Button 0", True)


def test_released_button_0_dispatch(recording_state):
    recording_state.handle_event(Button0Event(False))
    assert recording_state.handled("Button 0", False)


def test_pressed_button_1_dispatch(recording_state):
    recording_state.handle_event(Button1Event(True))
    assert recording_state.handled("Button 1", True)


def test_released_button_1_dispatch(recording_state):
    recording_state.handle_event(Button1Event(False))
    assert recording_state.handled("Button 1", False)


def test_pressed_button_2_dispatch(recording_state):
    recording_state.handle_event(Button2Event(True))
    assert recording_state.handled("Button 2", True)


def test_released_button_2_dispatch(recording_state):
    recording_state.handle_event(Button2Event(False))
    assert recording_state.handled("Button 2", False)


def test_pressed_button_3_dispatch(recording_state):
    recording_state.handle_event(Button3Event(True))
    assert recording_state.handled("Button 3", True)


def test_released_button_3_dispatch(recording_state):
    recording_state.handle_event(Button3Event(False))
    assert recording_state.handled("Button 3", False)


def test_pressed_button_Up_dispatch(recording_state):
    recording_state.handle_event(ButtonUpEvent(True))
    assert recording_state.handled("Button Up", True)


def test_released_button_Up_dispatch(recording_state):
    recording_state.handle_event(ButtonUpEvent(False))
    assert recording_state.handled("Button Up", False)


def test_pressed_button_Right_dispatch(recording_state):
    recording_state.handle_event(ButtonRightEvent(True))
    assert recording_state.handled("Button Right", True)


def test_released_button_Right_dispatch(recording_state):
    recording_state.handle_event(ButtonRightEvent(False))
    assert recording_state.handled("Button Right", False)


def test_pressed_button_Down_dispatch(recording_state):
    recording_state.handle_event(ButtonDownEvent(True))
    assert recording_state.handled("Button Down", True)


def test_released_button_Down_dispatch(recording_state):
    recording_state.handle_event(ButtonDownEvent(False))
    assert recording_state.handled("Button Down", False)


def test_pressed_button_Left_dispatch(recording_state):
    recording_state.handle_event(ButtonLeftEvent(True))
    assert recording_state.handled("Button Left", True)


def test_released_button_Left_dispatch(recording_state):
    recording_state.handle_event(ButtonLeftEvent(False))
    assert recording_state.handled("Button Left", False)


def test_pressed_button_A_dispatch(recording_state):
    recording_state.handle_event(ButtonAEvent(True))
    assert recording_state.handled("Button A", True)


def test_released_button_A_dispatch(recording_state):
    recording_state.handle_event(ButtonAEvent(False))
    assert recording_state.handled("Button A", False)


def test_pressed_button_B_dispatch(recording_state):
    recording_state.handle_event(ButtonBEvent(True))
    assert recording_state.handled("Button B", True)


def test_released_button_B_dispatch(recording_state):
    recording_state.handle_event(ButtonBEvent(False))
    assert recording_state.handled("Button B", False)


def test_touched_dispatch(recording_state):
    recording_state.handle_event(TouchEvent((1, 1)))
    assert recording_state.handled("Touch", (1, 1))


def test_touch_released_dispatch(recording_state):
    recording_state.handle_event(TouchEvent(None))
    assert recording_state.handled("Touch", None)
