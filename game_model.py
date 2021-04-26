import pygame
from abc import ABC, abstractmethod

class Package(ABC):
    """
    Package representation

    Attributes:
        _location: the location of the package in cartesian coordinates
    """
    def __init__(self, x, y):
        """
        Initializes package location

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
        """
        self._location = [x,y]

    def __repr__(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @property
    def location(self):
        """
        Returns location of the package.
        """
        return self._location

class ColorPackage(Package()):
    """
    A representation of a package with color

    Attributes:
        _color = a str describing the color of the package
    """

    def __init__(self,x,y,color):
        """
        Initializes a colored package

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
            color: a str describing the color of the package
        """
        super().__init__(x,y)
        self._color = color

    @property
    def color(self):
        """
        Returns the color of the package
        """
        return self._color

class Tower(ABC):
    """
    Representation of the robot tower.

    Attributes:
        _location: the location of the package in cartesian coordinates
        _rate: the rate at which the tower can process ColorPackage classes.
        _radius: the distance from the tower which the robot can process
                    packages.
    """
    def __init__(self,x,y,rate,radius):
        """
        Initialize robot tower.

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
            rate: the rate at which the tower can process ColorPackage classes.
            radius: the distance from the tower which the robot can process
                    packages.
        """
        self._location = [x,y]
        self._rate = rate
        self._radius = radius

    @property
    def location(self):
        """
        Returns location of the package.
        """
        return self._location
    
    @property
    def rate(self):
        """
        Returns rate of the tower's package processing.
        """
        return self._rate
    
    @property
    def _radius(self):
        """
        Returns active radius of the tower.
        """
        return self._radius
    
    @abstractmethod
    def remove_package(self):
        """
        Process a package instance within a certain radius & time.
        """
        pass

class Factory():
    """
    Representation of the factory floor gameboard

    Attributes:
        _packages: a list of the generated Package instances.
        _robots: a list of the generated Tower instances.
        _tower_count: an int representing the number of towers available.
        _path: a list of cartesian coordinates containing anchor points
               for a path which packages instances can follow.
        _packed: an integer which represents the number of Package instances
                 that the Tower instances has processed.
    """
    def __init__(self,path_list,tower_count):
        """
        Initializes factory floor gameboard.

        Args:
            path_list: a list of cartesian coordinates containing anchor points
                       for a path which packages instances can follow.
            tower_count: an integer which represents the number of towers the
                         player has access to.
        """
        self._packages = []
        self._robots = []
        self._tower_count = tower_count
        self._path = path_list
        self._packed = 0
    
    def generate_tower(self,x,y):
        """
        Create a tower given a positional input.

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
        """
        pass

    def close_to(self,robot):
        """
        Returns Package instances within radius of given Tower instance.

        Args:
            robot: a Tower instance placed onto the gameboard
        
        Returns:
            close_packages: a list of all of the Package instances within range
                            of the given Tower instance.
        """
        close_packages = []
        for package in self._packages:
            distance = ((package.location()[0] - robot.location()[0])**2 + \
                       (package.location()[1] - robot.location()[1])**2)**(1/2)
            if distance <= robot.radius():
                close_packages.append(package)
        return close_packages

    @property
    def packages(self):
        """
        Returns the list of Package instances.
        """
        return self._packages

    @property
    def robots(self):
        """
        Returns the list of Tower instances.
        """
        return self._robots
    
    @property
    def tower_count(self):
        """
        Returns number of Tower instances that the player can place.
        """
        return self._tower_count

    @property
    def packed(self):
        """
        Returns number of Package instances processed.
        """
        return self._packed
    
