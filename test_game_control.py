"""
Test functions
"""
import copy
import pytest
import pygame
import game_control as gc
import game_model as gm

# pylint: disable=no-name-in-module
from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
)

# pylint: disable=no-member
pygame.init()
_ = pygame.display.set_mode([1, 1])

LEFT_CLICK = pygame.event.Event(MOUSEBUTTONDOWN,button=1)
RIGHT_CLICK = pygame.event.Event(MOUSEBUTTONDOWN,button=3)

class TestMouseControl(gc.MouseControl):
    """
    Create test class inheriting from MouseControl class.

    Attributes:
    """
    def __init__(self,gameboard,events,mouse_pos):
        """
        """
        super().__init__(gameboard)
        self._events = events
        self._mouse_pos = mouse_pos

    def get_events(self):
        """
        Return inputted events.
        """
        return self._events
    
    def get_mouse_pos(self):
        """
        Return inputted mouse position.
        """
        return self._mouse_pos

test_place_tower_cases = [
    # Form: (events, mouse_pos,tower_count)
    # Base case that no queued inputs places no towers.
    ([],(0,0),0),
    # Test that a queued click places a tower.
    ([LEFT_CLICK],(1,1),1),
    # Test that two queued clicks places two towers.
    ([LEFT_CLICK,LEFT_CLICK],(1,1),2),
    # Test that RIGHT_CLICK input doesn't place a tower.
    ([RIGHT_CLICK],(0,0),0),
    # Test that clicks outside of display range places no towers.
    ([LEFT_CLICK],(1000,1000),0),
]

@pytest.mark.parametrize("events,mouse_pos,tower_count",test_place_tower_cases)
def test_place_tower(events,mouse_pos,tower_count):
    """
    Test tower placement is correct.

    Args:
        events: a list of pygame events.
        mouse_pos: a tuple of ints representing the cartesian coordinate
                   location of the mouse in pixels.
        tower_count: an int representing the number of tower instances
                     expected after test is run.
    """
    # Generate factory with a small loan of $999,999,999
    factory = gm.Factory(999999999)
    click_update = TestMouseControl(factory, events, mouse_pos)
    click_update.control()
    assert len(factory.robots) == tower_count

test_remove_tower_cases = [
    # Form: (events,mouse_pos,tower_removed_count)
    # Test that removal of previously placed tower goes through.
    ([RIGHT_CLICK],(1,1),1),
    # Test that removal of previously placed tower goes through.
    ([RIGHT_CLICK],(400,400),1),
    # Test that removal of previously placed tower goes through
    # without removing extraneous towers.
    ([RIGHT_CLICK,RIGHT_CLICK],(400,400),1),
    # Test click not on a tower doesn't remove a tower.
    ([RIGHT_CLICK],(200,200),0),
    # Test click outside of bounds doesn't do anything.
    ([RIGHT_CLICK],(1000,1000),0),
    # Test other inputs don't do anything.
    ([KEYDOWN],(1,1),0),
]

# Locations of preset towers.
TOWER_LOCATIONS = [(0,0),(400,400)]

@pytest.mark.parametrize("events,mouse_pos,tower_removed_count", \
                         test_remove_tower_cases)
def test_remove_tower(events,mouse_pos,tower_removed_count):
    """
    Test tower removal is correct.

    Args:
        events: a list of pygame events.
        mouse_pos: a tuple of ints representing the cartesian coordinate
                   location of the mouse in pixels.
        tower_removed_count: an int representing how many tower instances
                             were expected to be removed based off of event
                             type and mouse position.
    """
    # Generate factory with a small loan of $999,999,999
    factory = gm.Factory(999999999)
    # Preset towers
    for tower in TOWER_LOCATIONS:
        factory.generate_tower(tower[0],tower[1],1,1)

    click_update = TestMouseControl(factory, events, mouse_pos)
    click_update.control()

    assert len(factory.robots) == 2-tower_removed_count
