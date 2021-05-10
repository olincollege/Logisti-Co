"""
Helper functions for test_game_control.py
"""

import game_control as gc

class MouseControlTest(gc.MouseControl):
    """
    Test class inheriting from MouseControl class with assignable events and
    mouse position

    Attributes:
    self._events: a list of pygame Events which can be assigned for simulating
                  input.
    self._mouse_pos: a tuple of integers representing the current simulated
                     mouse position.
    """
    def __init__(self,gameboard,events,mouse_pos):
        """
        Initialize attributes for simulated use.
        """
        super().__init__(gameboard)
        self.events = events
        self.mouse_pos = mouse_pos

    def get_events(self):
        """
        Return inputted events.
        """
        return self.events

    def get_mouse_pos(self):
        """
        Return inputted mouse position.
        """
        return self.mouse_pos

# pylint: disable=too-few-public-methods
class EventTest():
    """
    A simulated pygame Event used for testing input.

    Attributes:
        type: the pygame Event type.
        button: an int correstponding to the mouse button pressed.
    """

    def __init__(self, event_type, button):
        """
        Initialize type and button.

        Args:
            type: a pygame Event type.
            button: an int correstponding to the mouse button pressed.
        """
        self.type = event_type
        self.button = button
