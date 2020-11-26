import pytest
from events import *


def test_button_0():
    event = Button0Event(True)
    assert event.description == "Button 0 pressed"
    event = Button0Event(False)
    assert event.description == "Button 0 released"


def test_button_1():
    event = Button1Event(True)
    assert event.description == "Button 1 pressed"
    event = Button1Event(False)
    assert event.description == "Button 1 released"


def test_button_2():
    event = Button2Event(True)
    assert event.description == "Button 2 pressed"
    event = Button2Event(False)
    assert event.description == "Button 2 released"


def test_button_3():
    event = Button3Event(True)
    assert event.description == "Button 3 pressed"
    event = Button3Event(False)
    assert event.description == "Button 3 released"


def test_button_Up():
    event = ButtonUpEvent(True)
    assert event.description == "Button Up pressed"
    event = ButtonUpEvent(False)
    assert event.description == "Button Up released"


def test_button_Right():
    event = ButtonRightEvent(True)
    assert event.description == "Button Right pressed"
    event = ButtonRightEvent(False)
    assert event.description == "Button Right released"


def test_button_Down():
    event = ButtonDownEvent(True)
    assert event.description == "Button Down pressed"
    event = ButtonDownEvent(False)
    assert event.description == "Button Down released"


def test_button_Left():
    event = ButtonLeftEvent(True)
    assert event.description == "Button Left pressed"
    event = ButtonLeftEvent(False)
    assert event.description == "Button Left released"


def test_button_A():
    event = ButtonAEvent(True)
    assert event.description == "Button A pressed"
    event = ButtonAEvent(False)
    assert event.description == "Button A released"


def test_button_B():
    event = ButtonBEvent(True)
    assert event.description == "Button B pressed"
    event = ButtonBEvent(False)
    assert event.description == "Button B released"


def test_touch():
    event = TouchEvent((1, 1))
    assert event.description == "Touch at (1, 1)"
    event = TouchEvent(None)
    assert event.description == "Touch ended"


def test_tick():
    event = TickEvent()
    assert event.description == "Tick"
