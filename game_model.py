import pygame
from abc import ABC, abstractmethod
import game_view
pygame.init()


class Package(pygame.sprite.Sprite):
    """
    Package representation

    Attributes:
        _location: a tuple of floats representing the location of the package
        in cartesian coordinates.
        _path: a list of coordinates depicting the pixel waypoints the package
        should reach.
    """
    def __init__(self, x, y, path):
        """
        Initializes package location, path, and sprite object

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
            path: a list of coordinates depicting the pixel waypoints the package
            should reach.
        """
        
        self._location = [x,y]
        self._path = path

        super(Package, self).__init__()
        self._surf = pygame.Surface((25, 25))
        self._surf.fill((128, 128, 128))
        self._rect = self._surf.get_rect()
        self._rect.center = (int(self._location[0]), int(self._location[1]))

    def move(self):
        """
        Move the package for the game tick along the path.
        """
        # Move onto the next waypoint if reached
        if self._rect.center == self._path[0]:
            self._path = self._path[1:]
        # Detect if the list is too short
        if len(self._path) == 0:
            return False
        # Calculate the normalized direction and use it to transform location
        # with a certain speed
        distance = ((self.location[0] - self._path[0][0])**2 + \
                    (self.location[1] - self._path[0][1])**2)**(1/2)
        direction = ((self._path[0][0] - self.location[0])/distance, \
                    (self._path[0][1] - self.location[1])/distance)
        # The speed, in pixels/tic, which the package will move
        speed = 1
        displacement = (direction[0]*speed, direction[1]*speed)
        self._location = (self._location[0]+displacement[0], self._location[1]+displacement[1])
        
        self._rect.center = (int(self._location[0]), int(self._location[1]))

    @property
    def location(self):
        """
        Returns location of the package.
        """
        return self._location

class ColorPackage(Package):
    """
    A representation of a package with color

    Attributes:
        _color: a string describing the color of the package
        package_colors: a dict mapping package colors to RGB codes.
    """

    def __init__(self,x,y, path, color):
        """
        Initializes a colored package

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
            color: a str describing the color of the package
        """
        super(ColorPackage, self).__init__(x,y,path)
        self._color = color
        self.surf.fill(self.get_RGB())


    @property
    def color(self):
        """
        Returns the color of the package
        """
        return self._color
    
    package_colors = {"red": (255,0,0), "green": (0,255,0), "blue": (0,0,255)}

    def get_RGB(self):
        return self.package_colors[self.color]

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
        _packages: a pygame Group of the generated Package instances.
        _robots: a pygame Group of the generated Tower instances.
        _tower_count: an int representing the number of towers available.
        _path: a list of cartesian coordinates containing anchor points
               for a path which packages instances can follow.
        _packed: an integer which represents the number of Package instances
                 that the Tower instances has processed.
    """
    def __init__(self,tower_count):
        """
        Initializes factory floor gameboard.

        Args:
            path_list: a list of cartesian coordinates containing anchor points
                       for a path which packages instances can follow.
            tower_count: an integer which represents the number of towers the
                         player has access to.
        """
        self._packages = pygame.sprite.Group()
        self._robots = pygame.sprite.Group()
        self._tower_count = tower_count
        self._path = [(0,84), (675,84), (675,213), (112,213), (112,366), (675,366), (675,526), (0,526)]
        self._packed = 0
        self._failed = 0
    
    def main(self):
        view = game_view.PyGameView(self)
        clock = pygame.time.Clock()
        gen_rate = 200
        generator = Generator(self, gen_rate, self._path)
        while True:
            generator.update()
            self.update_packages()
            print(self._failed)
            view.draw()
            clock.tick(60)
    
    def update_packages(self):
        """
        Check validity of Package instance, update position of all packages.
        """
        for package in self._packages:
            if package.move() == False:
                package.kill()
                self._failed += 1

    def generate_tower(self,x,y):
        """
        Create a tower given a positional input.

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
        """
        pass

    def generate_package(self):
        """
        Create a tower at the start of the path

        Args:
            x: the x-axis location of the package in pixels
            y: the y-axis location of the package in pixels
        """
        self._packages.add(Package(self._path[0][0],self._path[0][1],self._path))

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
    
class Generator():
    """
    A generator of Package objects for Logisti Co. game.

    Attributes:
        _factory: the Factory instance to generate 
    """
    def __init__(self, factory, gen_rate, path):
        """
        Initialize factory, gen_rate, tick_count, attributes.

        Args:
            factory: a Factory instance.
            gen_rate: an integer representing the number of game ticks needed
                      to generate a package.
            path: a list of tuple coordinates which represent the route a
                  package will take.
        """
        self._factory = factory
        self._gen_rate = gen_rate
        self._path = path
        self._tick_count = 0
    
    def generate_package(self):
        """
        Generates a new package in the Factory instance.
        """
        self._factory.generate_package()
    
    def update(self):
        """
        Track change in _tick_count & generates package at given interval.
        """
        self._tick_count += 1
        if self._tick_count % self._gen_rate == 0:
            self.generate_package()
    
    @property
    def tick_count(self):
        """
        Returns current _tick_count value.
        """
        return self._tick_count

