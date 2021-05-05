"""
Test functions
"""

import pytest

from game_model import (
    Package,
    ColorPackage,
    Tower,
    ColorTower,
    Factory,
    Generator,
)

# Define sets of test cases.
package_move_cases = [
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
]
@pytest.mark.parametrize("x, y, path, output",package_move_cases)
def test_package_move(x, y, path, output):
    """
    Test movement of Package class.

    Args:
        x: the x-axis location of the package in pixels
        y: the y-axis location of the package in pixels
        path: a list of tuple coordinates depicting the pixel waypoints the
              package should reach.
    """
    package = Package(x, y, path)
    package.move()
    assert package.location == output


# Define sets of test cases.
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
]
@pytest.mark.parametrize("x, y, path, output",package_no_move_cases)
def test_package_no_move(x, y, path, output):
    """
    Test movement of Package class.

    Args:
        x: the x-axis location of the package in pixels
        y: the y-axis location of the package in pixels
        path: a list of tuple coordinates depicting the pixel waypoints the
              package should reach.
    """
    package = Package(x, y, path)
    assert package.move() == output