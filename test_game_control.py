"""
Test functions
"""

# pylint: disable=no-name-in-module
from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
)

import pytest
import pygame
import game_model as gm

from test_helper_classes import (
    EventTest,
    MouseControlTest,
)

# pylint: disable=no-member
pygame.init()
_ = pygame.display.set_mode([1, 1])


LEFT_CLICK = EventTest(MOUSEBUTTONDOWN, 1)
RIGHT_CLICK = EventTest(MOUSEBUTTONDOWN, 3)
EXTRANEOUS_INPUT = EventTest(KEYDOWN, 0)

test_detect_click_cases = [
    # Form: (event_list, mouse_button)
    # Test that no events returns 0.
    ([], 0),
    # Test that events but no click returns 0.
    ([EXTRANEOUS_INPUT], 0),
    # Test that a left click returns 1.
    ([LEFT_CLICK], 1),
    # Test that a left click returns 1.
    ([RIGHT_CLICK], 3),
    # Test that a left click and other events returns 1.
    ([EXTRANEOUS_INPUT, LEFT_CLICK], 1),
    # Test that a right click and other events returns 1.
    ([EXTRANEOUS_INPUT, RIGHT_CLICK], 3),
]

@pytest.mark.parametrize("event_list, mouse_button",test_detect_click_cases)
def test_detect_click(event_list, mouse_button):
    """
    Test that click detection performs as expected.

    Args:
        event_list: a list of pygame events.
        mouse_button: an int describing which button is pressed
    """
    # Generate factory with a small loan of $999,999,999
    factory = gm.Factory(999999999)
    control = MouseControlTest(factory, event_list, (0,0))
    assert mouse_button == control.detect_click()

test_place_tower_cases = [
    # Form: (events, mouse_pos,tower_count)
    # Base case that no queued inputs places no towers.
    ([],(0,0),0),
    # Test that a queued click places a tower.
    ([LEFT_CLICK],(1,1),1),
    # Test that two queued clicks only places one tower.
    ([LEFT_CLICK,LEFT_CLICK],(1,1),1),
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
    click_update = MouseControlTest(factory, events, mouse_pos)
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
    ([EXTRANEOUS_INPUT],(1,1),0),
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

    click_update = MouseControlTest(factory, events, mouse_pos)
    click_update.control()

    assert len(factory.robots) == 2-tower_removed_count
