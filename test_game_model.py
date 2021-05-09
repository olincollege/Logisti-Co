"""
Test Logisti-Co model functions.
"""

import pytest
import pygame
import game_model as gm

# Test cases for package movement
package_move_cases = [
    # As the packages will only be moving one pixel per call with this
    # function, and the packages only move in cardinal directions, we will test
    # this behavior and non-moving packages.
    # test moving 1 pixel over in positive x direction
    (0, 0, [(0,0),(10,0)],   (1,0)),
    # test moving 1 pixel over in positive y direction
    (0, 0, [(0,0),(0,10)],   (0,1)),
    # test moving 1 pixel over in negative x direction
    (0, 0, [(0,0),(-10,0)],   (-1,0)),
    # test moving 1 pixel over in negative y direction
    (0, 0, [(0,0),(0,-10)],   (0,-1)),
    # test no moving on provided path
    (0, 0, [(0,0),(0,0)],   (0,0)),
    # test moving one pixel from a non (0,0) starting position
    (5, 6, [(5,6),(5,10)],   (5,7)),
    # test no movement from a non (0,0) starting position
    (5, 6, [(5,6),(5,6)],   (5,6)),
]
@pytest.mark.parametrize("x_pos, y_pos, path, output",package_move_cases)
def test_package_move(x_pos, y_pos, path, output):
    """
    Test movement of Package class.

    Args:
        x_pos: the x-axis location of the package in pixels
        y_pos: the y-axis location of the package in pixels
        path: a list of tuple coordinates depicting the pixel waypoints the
              package should reach.
        output: expected output of the function.
    """
    package = gm.Package(x_pos, y_pos, path)
    package.move()
    assert package.location == output


# Test
package_no_move_cases = [
    # test no moving on provided path was unsuccessful on path of length 1
    (0, 0, [(0,0)],   False),
    # test no moving on provided path was successful on path of length 2
    (0, 0, [(0,0),(0,0)],   True),
    # test moving 1 pixel over in positive x direction was successful
    (0, 0, [(0,0),(10,0)],   True),
    # test moving 1 pixel over in positive y direction was successful
    (0, 0, [(0,0),(0,10)],   True),
    # test moving 1 pixel over in negative x direction was successful
    (0, 0, [(0,0),(-10,0)],   True),
    # test moving 1 pixel over in negative y direction was successful
    (0, 0, [(0,0),(0,-10)],   True),
    # test no moving on provided path was unsuccessful on path of length 1 from
    # a non (0,0) starting position
    (5, 6, [(5,6)],   False),
]
@pytest.mark.parametrize("x_pos, y_pos, path, output",package_no_move_cases)
def test_package_no_move(x_pos, y_pos, path, output):
    """
    Test movement of Package class is successful when not at the end of the
    path and unsuccessful when at the end of the path.

    Args:
        x_pos: the x-axis location of the package in pixels
        y_pos: the y-axis location of the package in pixels
        path: a list of tuple coordinates depicting the pixel waypoints the
              package should reach.
        output: expected output of the function.
    """
    package = gm.Package(x_pos, y_pos, path)
    assert package.move() == output


tower_update_ready_cases = [
    # Test the behavior of towers becoming ready after a set amount of ticks.
    # Should yield true if the cycles is greater than the rate.
    # Test rate of 1 is True after 100 cycles.
    # Form: (cycles, ticks, output)
    (100, 1, True),
    # Test rate of 100 is False after one cycle.
    (1, 100, False),
    # Test rate of 0 is always True after 100 cycles.
    (100, 0, True),
    # Test edge case of cycles and ticks being equal.
    (2, 2, True),
    # Test edge case of cycles being one less than ticks
    (3, 4, False),
    # Test edge case of cycles being one more than ticks
    (4, 3, True)
]
# pylint: disable=no-member
pygame.init()
_ = pygame.display.set_mode([1, 1])



@pytest.mark.parametrize("update_count, rate, output", tower_update_ready_cases)
def test_tower_update_ready(update_count, rate, output):
    """
    Test reset timer on Tower class.

    Args:
        update_count: the number of game ticks which the game is simulated.
        rate: the rate at which the tower can process Package classes.
        output: expected output of the function.
    """
    tower = gm.Tower(0, 0, rate, 10, TOWER_FRAMES_Y)
    for _ in range(update_count):
        tower.update_ready()
    assert tower.ready == output



# Location cases for factory_update_robots_cases
robot_locations_1 = [(0,0)]
package_locations_1 = [(0,0)]


# Test the robots' ability to remove packages.
factory_update_robots_cases = [
    # form([(x,y)],[(a,b)],robot_rate,cycle_count,radius,
    # packages_after) Where (x,y) are the locations of robots and (a,b) are the
    # locations of packages.
    # Test base case, removing a single package with a single robot
    (robot_locations_1,package_locations_1, 2, 3, 1, 0),
]

@pytest.mark.parametrize( \
    "rob_locations,package_locations,rate,cycle_count,radius,packages_after", \
    factory_update_robots_cases)
def test_factory_update_robots( \
    rob_locations,package_locations,rate,cycle_count,radius,packages_after):
    """
    Test the robots' ability to remove packages.
    Args:
        output: expected output of the function.
    """
    # Generate a factory with near infinite funds
    factory = gm.Factory(999999999)
    # Generate robots and packages per instructions
    for location in rob_locations:
        factory.generate_tower(location[0], location[1], rate, radius)
    for location in rob_locations:
        factory.generate_package([location])
    for _ in range(cycle_count):
        factory.update_robots()
    # Determine if the number of packages is equal to the expected amount
    assert len(factory.packages) == packages_after

test_update_package_cases = [
    # Test that packages get removed after they reach the end of the path.
    # Form: (path_length, cycles, got_removed)
    # Test base case that 
]



# Test generator behaves as expected.
test_generator_update_cases = [
    # Form: (rate, cycles, expected_packages)
    # Form:
]