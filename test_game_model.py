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
    tower = gm.Tower(0, 0, rate, 10, gm.TOWER_FRAMES_Y)
    for _ in range(update_count):
        tower.update_ready()
    assert tower.ready == output



# Location cases for factory_update_robots_cases
locations_1 = {"Robot": [(0,0)], "Package": [(0,0)]}
locations_2 = {"Robot": [(0,0)], "Package": [(0,0),(0,1)]}
locations_3 = {"Robot": [(0,0)], "Package": [(0,0),(0,5)]}
locations_4 = {"Robot": [(0,0)], "Package": [(10,0),(0,10)]}
locations_5 = {"Robot": [(0,0), (0,0)], "Package": [(0,0),(0,0)]}
locations_6 = {"Robot": [(0,0), (0,1)], "Package": [(0.1,0.1),(-0.1,0.9)]}
locations_7 = {"Robot": [(0,0), (0,10)], "Package": [(0.1,0.1),(-100,-100)]}
locations_8 = {"Robot": [(0,0)], "Package": []}
# Test the robots' ability to remove packages.
factory_update_robots_cases = [
    # form([(x,y)],[(a,b)],robot_rate,cycle_count,radius,
    # packages_after) Where (x,y) are the locations of robots and (a,b) are the
    # locations of packages.
    # Test base case, removing a single package with a single robot.
    (locations_1["Robot"],locations_1["Package"], 2, 3, 1, 0),
    # Test that if not enough time is given, the tower will not remove a
    # package.
    (locations_1["Robot"],locations_1["Package"], 9, 8, 1, 1),
    # Test that if there are two packages in radius, the robot only removes
    # one package.
    (locations_2["Robot"],locations_2["Package"], 2, 3, 2, 1),
    # Test that if there is one package in radius, and one package outside,
    # that only one gets removed within a long period.
    (locations_3["Robot"],locations_3["Package"], 2, 5, 1, 1),
    # Test that if all packages are outside of the radius, that the tower
    # removes none.
    (locations_4["Robot"],locations_4["Package"], 2, 5, 1, 2),
    # Test that the tower can remove multiple packages within radius, given
    # enough time.
    (locations_2["Robot"],locations_2["Package"], 2, 6, 2, 0),
    # Test that two towers in the same place will remove both packages within a
    # single robot rate time
    (locations_5["Robot"],locations_5["Package"], 2, 3, 1, 0),
    # Test that two towers in different locations and packages nearby will
    # successfully remove all packages.
    (locations_6["Robot"],locations_6["Package"], 2, 3, 1, 0),
    # Test that multiple towers with one package in range and one out of range
    # will only remove one package.
    (locations_7["Robot"],locations_7["Package"], 2, 3, 1, 1),
    # Test base case that no packages returns None.
    (locations_8["Robot"],locations_8["Package"], 2, 3, 1, 0),
]

@pytest.mark.parametrize( \
    "rob_locations,package_locations,rate,cycle_count,radius,packages_after", \
    factory_update_robots_cases)
# pylint: disable=too-many-arguments
def test_factory_update_robots( \
    rob_locations,package_locations,rate,cycle_count,radius,packages_after):
    """
    Test the robots' ability to remove packages.
    Args:
        rob_locations: a list of tuples of floats describing the cartesian
                       coordinates for all Tower instances to be created.
        package_locations: a list of tuples of floats describing the cartesian
                           coordinates for all Package instances to be created.
        rate: an int representing the rate at which the tower can process
              Package classes.
        cycle_count: the number of game ticks which the game is simulated.
        radius: a float representing the distance from the tower which the
                robot can process packages.
        packages_after: an int representing the number of expected Package
                        instances at the end of simualation.
    """
    # Generate a factory with near infinite funds
    factory = gm.Factory(999999999)
    # Generate robots and packages per instructions
    for location in rob_locations:
        factory.generate_tower(location[0], location[1], rate, radius)
    for location in package_locations:
        factory.generate_package([location]*2)
    for _ in range(cycle_count):
        factory.update_robots()
    # Determine if the number of packages is equal to the expected amount
    assert len(factory.packages) == packages_after


locations_1 = {"Robot": (0,0), "Package": [(0,0)]}
locations_2 = {"Robot": (0,0), "Package": [(100,0)]}
locations_3 = {"Robot": (0,0), "Package": [(9,0),(0,5)]}
locations_4 = {"Robot": (0,0), "Package": [(11,0),(0,5)]}
locations_5 = {"Robot": (0,0), "Package": [(11,0),(0,11)]}
locations_6 = {"Robot": (0,0), "Package": []}

test_closest_package_cases = [
    # Test the Factory method closest_package for returning the closest package
    # Form (robot radius, robot location, package locations, expected closest
    # package location)
    # Robot, Package @ (0,0), should return the only package.
    (10, locations_1["Robot"],locations_1["Package"],(0,0)),
    # Test that a package out of range returns None
    (10, locations_2["Robot"],locations_2["Package"],None),
    # Test that function chooses closer package within radius.
    (10, locations_3["Robot"],locations_3["Package"],(0,5)),
    # Test that function ignores package outside of radius.
    (10, locations_4["Robot"],locations_4["Package"],(0,5)),
    # Test that function returns None if no packages within radius.
    (10, locations_5["Robot"],locations_5["Package"],None),
    # Test base case that no packages returns None.
    (10, locations_6["Robot"],locations_6["Package"],None),
]

@pytest.mark.parametrize("radius,rob_location,package_locations,closest_loc", \
    test_closest_package_cases)
def test_closest_package(radius,rob_location,package_locations,closest_loc):
    """
    Test closest package detection works properly.
    Args:
        radius: a float representing the distance from the tower which the
                robot can process packages.
        rob_location: a tuple of floats describing the cartesian
                      coordinates for all Tower instances to be created.
        package_locations: a list of tuples of floats describing the cartesian
                           coordinates for all Package instances to be created.
        closest_loc: a tuple of floats which return the location of the closest
                     package instance.
    """
    # Generate a factory with near infinite funds
    factory = gm.Factory(999999999)
    # Generate robots and packages per instructions
    robot = gm.Tower(rob_location[0],rob_location[1], \
                     4,radius,gm.TOWER_FRAMES_Y)
    for location in package_locations:
        factory.generate_package([location]*2)
    # Determine if the number of packages is equal to the expected amount
    if closest_loc is not None:
        assert factory.closest_to(robot).location == closest_loc
    else:
        assert factory.closest_to(robot) == closest_loc

test_update_package_cases = [
    # Test that packages get removed after they reach the end of the path.
    # Form: (path_length, expected_num_packages)
    # Test base case that package at the end of its path is removed
    ([1],0),
    # Test the case that multiple packages, but that only one is @ the end of
    # it's path.
    ([3,2,1],2),
    # Test base case that package not at the end of its path lives.
    ([3],1),
    # Test case that multiple packages are at the end and are killed.
    ([1,1,1],0),
    # Test case that mutliple packages are not at the end and live.
    ([3,3,3],3),
]

@pytest.mark.parametrize("path_length, expected_num_packages", \
    test_update_package_cases)
def test_update_package(path_length, expected_num_packages):
    """
    Test that updating packages / removal works properly.
    Args:
        path_length: an int representing how many coordinates are left within
                     a path list.
        expected_num_packages: an int representing how many packages should be
                               left after the update_packages call.
    """
    # Generate a factory with near infinite funds
    factory = gm.Factory(999999999)
    # Generate packages per instructions
    for length in path_length:
        factory.generate_package([(0,0)]*length)
    factory.update_packages()
    # Determine if the number of packages is equal to the expected amount
    assert len(factory.packages) == expected_num_packages

# Test generator behaves as expected.
test_generator_cases = [
    # Form: (rate, cycles, expected_packages)
    # Test that the generator creates one package given expected time.
    (5,6,1),
    # Test that the generator creates one package given expected time.
    (10,22,2),
    # Test base case that no packages generate with insufficient time.
    (10,1,0),
]

@pytest.mark.parametrize("rate,cycles,expected_packages", test_generator_cases)
def test_generator(rate, cycles, expected_packages):
    """
    Test that package generation function works correctly.
    Args:
        rate: an int that represents the number of ticks it takes to generate a
              package instance.
        cycles: an int that represents how many generation ticks that are
                simulated.
        expected_packages: an int that represents how many packages that should
                           be generated given the rate and cycle amount.
    """
    # Generate a factory & generator
    factory = gm.Factory(999999999)
    generator = gm.Generator(factory, rate, factory.path)
    for _ in range(cycles):
        generator.update()
    # Determine if the number of packages is equal to the expected amount
    assert len(factory.packages) == expected_packages
