"""
Logisti-Co game model.
"""
import pygame
import game_view
import game_control
# pylint: disable=no-member
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
    def __init__(self, x_pos, y_pos, path):
        """
        Initializes package location, path, and sprite object

        Args:
            x_pos: the x-axis location of the package in pixels
            y_pos: the y-axis location of the package in pixels
            path: a list of tuple coordinates depicting the pixel waypoints the
                  package should reach.
        """

        self._location = (x_pos,y_pos)
        self._path = path

        super().__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((128, 128, 128))
        self.rect = self.surf.get_rect()
        self.rect.center = (int(self._location[0]), int(self._location[1]))

    def move(self):
        """
        Move the package for the game tick along the path.
        """
        # Move onto the next waypoint if reached
        if self.rect.center == self._path[0]:
            self._path = self._path[1:]
        # Detect if the list is too short
        if len(self._path) == 0:
            return False
        # Calculate the normalized direction and use it to transform location
        # with a certain speed
        distance = ((self.location[0] - self._path[0][0])**2 + \
                    (self.location[1] - self._path[0][1])**2)**(1/2)
        if distance == 0:
            direction = (0,0)
        else:
            direction = ((self._path[0][0] - self.location[0])/distance, \
                        (self._path[0][1] - self.location[1])/distance)
        # The speed, in pixels/tic, which the package will move
        speed = 1
        displacement = (direction[0]*speed, direction[1]*speed)
        self._location = (self._location[0]+displacement[0], self._location[1]+displacement[1])

        self.rect.center = (int(self._location[0]), int(self._location[1]))

        # Report successful behavior
        return True

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

    def __init__(self,x_pos,y_pos, path, color):
        """
        Initializes a colored package

        Args:
            x_pos: the x-axis location of the package in pixels
            y_pos: the y-axis location of the package in pixels
            color: a str describing the color of the package
        """
        super().__init__(x_pos,y_pos,path)
        self._color = color
        self.surf.fill(self.get_rgb())
        self._package_colors = {"red":(255,0,0),"green":(0,255,0),
                                "blue":(0,0,255)}

    def get_rgb(self):
        """
        Return color of package in RGB.
        """
        return self._package_colors[self.color]

    @property
    def color(self):
        """
        Returns the color of the package
        """
        return self._color

TOWER_SPRITES = []
FRAME_COUNT = 40
for i in range(FRAME_COUNT):
    TOWER_SPRITES.append(pygame.image.load(f'./game_assets/Robot Animation Frames/frame{i}.gif'))

# pylint: disable=too-many-instance-attributes
class Tower(pygame.sprite.Sprite):
    """
    Representation of the robot tower.

    Attributes:
        _sprites: a list of GIF images representing the keyframes of the tower.
        _location: the location of the package in cartesian coordinates
        _rate: the rate at which the tower can process ColorPackage classes.
        _radius: the distance from the tower which the robot can process
                    packages.
        _ready: a bool status indicating whether the Tower is ready to receive
                a package or not.
        _tick: an int representing how much time has passed since the _ready
               attribute was changed.
    """
    def __init__(self,x_pos,y_pos,rate,radius):
        """
        Initialize robot tower.

        Args:
            x_pos: the x-axis location of the package in pixels
            y_pos: the y-axis location of the package in pixels
            rate: the rate at which the tower can process Package classes.
            radius: the distance from the tower which the robot can process
                    packages.
        """
        self._sprites = TOWER_SPRITES
        self._current_sprite = 0
        self._animating = False


        self._location = [x_pos,y_pos]
        self._rate = rate - 1
        self._radius = radius
        self._ready = False
        self._tick = 0

        super().__init__()
        self.surf = self._sprites[self._current_sprite].convert()
        size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(size[0]*0.1), int(size[1]*0.1)))
        self.surf = pygame.transform.rotate(self.surf, -90)
        self.rect = self.surf.get_rect(center = self._location)

    def update_sprite(self):
        """
        Update the sprite of the robot to the next animation frame.
        """
        self._current_sprite += 1
        print(f"Current Sprite: {self._current_sprite}")
        self.surf = self._sprites[self._current_sprite].convert()
        if self._current_sprite >= len(self._sprites)-1:
            self._current_sprite = 0
            self.surf = self._sprites[self._current_sprite].convert()
            self._animating = False

    def animate(self):
        """
        Change _animating attribute to True.
        """
        self._animating = True
        print(self._animating)

    def ready_reset(self):
        """
        Reset the ready state of the tower to false and reset tick
        """
        self._ready = False
        self._tick = 0

    def update_ready(self):
        """
        Update ready state based off of Tower rate.
        """
        if self._tick >= self._rate:
            self._ready = True
        self._tick += 1

    @property
    def ready(self):
        """
        Returns True is wait function is running, False otherwise.
        """
        return self._ready

    @property
    def animating(self):
        """
        Returns animating status.
        """
        return self._animating

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
    def radius(self):
        """
        Returns active radius of the tower.
        """
        return self._radius

class ColorTower(Tower):
    """
    A representation of a Tower with color.

    Attributes:
        _color: a string describing the color of the package
        tower_colors: a dict mapping package colors to RGB codes.
    """
    # pylint: disable=too-many-arguments
    def __init__(self,x_pos,y_pos,rate,radius,color):
        """
        Initializes a colored Tower.

        Args:
            x_pos: the x-axis location of the Tower in pixels
            y_pos: the y-axis location of the Tower in pixels
            rate: a float representing the number of packages the Tower can
                  process per second.
            radius: an int representing the active radius which the Tower can
                    process an incoming package.
            color: a str describing the color of the package
        """
        super().__init__(x_pos,y_pos,rate,radius)
        self._color = color
        self.surf.fill(self.get_rgb())
        self._tower_colors = {"red":(255,0,0),"green":(0,255,0),"blue":(0,0,255)}

    def get_rgb(self):
        """
        Return color of Tower in RGB.
        """
        return self._tower_colors[self.color]

    @property
    def color(self):
        """
        Returns the color of the Tower.
        """
        return self._color

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
        self._path = [(0,84), (675,84), (675,213), (112,213), \
                      (112,366), (675,366), (675,526), (0,526)]
        self._packed = 0
        self._failed = 0
        self._view = game_view.PyGameView(self)

    def main(self):
        """
        Run main game loop.
        """
        controller = game_control.MouseControl(self)
        clock = pygame.time.Clock()
        gen_rate = 300
        generator = ExponentialGenerator(self, gen_rate, self._path, 0.95)
        running = True
        while running:
            for event in pygame.event.get():
                # pylint: disable=no-member
                if event.type == pygame.locals.QUIT:
                    running = False
            generator.update()
            self.update_packages()
            self.update_robots()
            self._view.draw()
            controller.control()
            clock.tick(60)

    def update_robots(self):
        """
        Check if Package instances are within range of a given Tower instance.
        """
        for robot in self._robots:
            if robot.ready:
                closest_package = self.closest_to(robot)
                if closest_package is not None:
                    closest_package.kill()
                    robot.animate()
                    self._packed += 1
                    robot.ready_reset()
            robot.update_ready()
            if robot.animating:
                robot.update_sprite()
                size = robot.surf.get_size()
                robot.surf = pygame.transform.scale(robot.surf, \
                                (int(size[0]*0.1), int(size[1]*0.1)))
                robot.surf = pygame.transform.rotate(robot.surf, -90)
                robot.rect = robot.surf.get_rect(center = robot.location)

    def update_packages(self):
        """
        Check validity of Package instance, update position of all packages.
        """
        for package in self._packages:
            if package.move() is False:
                package.kill()
                self._failed += 1

    def generate_tower(self,x_pos,y_pos,rate,radius):
        """
        Create a tower given a positional input.

        Args:
            x_pos: the x-axis location of the package in pixels
            y_pos: the y-axis location of the package in pixels
            rate: an int which represents how many ticks a tower will take to
                  wait after processing a package.
            radius: an int which represents how far a package can be before it
                    is packed & removed by the Tower instance.
        """
        if self._tower_count > 0:
            self._robots.add(Tower(x_pos,y_pos,rate,radius))
            self._tower_count += -1

    def generate_package(self):
        """
        Create a tower at the start of the path
        """
        self._packages.add(Package(self._path[0][0],self._path[0][1],self._path))

    def closest_to(self,robot):
        """
        Returns Package instances within radius of given Tower instance.

        Args:
            robot: a Tower instance placed onto the gameboard

        Returns:
            closest_package: The closest Package instance in range, else None.
        """
        closest_package = None
        closest_distance = float("inf")
        for package in self._packages:
            distance = ((package.location[0] - robot.location[0])**2 + \
                       (package.location[1] - robot.location[1])**2)**(1/2)
            if distance <= robot.radius:
                if distance < closest_distance:
                    closest_package = package
                    closest_distance = distance
        return closest_package

    def remove_tower(self, tower):
        """
        Remove the tower from gameplay, and increase the number of available
        towers.
        """
        tower.kill()
        self._tower_count += 1

    @property
    def packages(self):
        """
        Returns the list of Package instances.
        """
        return self._packages

    @property
    def robots(self):
        """
        Return _robots.
        """
        return self._robots

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

    @property
    def failed(self):
        """
        Returns number of Packages that reached the end.
        """
        return self._failed

class Generator():
    """
    A generator of Package objects for Logisti Co. game.

    Attributes:
        _factory: the Factory instance to generate.
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

class IncreasingGenerator(Generator):
    """
    A generator which linearly increases the rate at which it produces
    packages.

    Attributes:
        _decrease: a float denoting the linear decrease in time to generate
        a package per tick.
    """
    def __init__(self, factory, gen_rate, path, decrease):
        super().__init__(factory, gen_rate, path)
        self._decrease = decrease

    def update(self):
        """
        Increment _tick_count, generate packages if the tick is larger than
        rate, and decrease the time to produce a package.
        """
        self._tick_count += 1
        if self._tick_count >= self._gen_rate:
            self.generate_package()
            if self._gen_rate >= 30:
                self._gen_rate += - self._decrease
            self._tick_count = 0

class ExponentialGenerator(Generator):
    """
    A generator which exponentially increases the rate at which it produces
    packages.

    Attributes:
        _proportion: a float denoting the exponential proportion between the
        time to generate the current package and the next package.
    """
    def __init__(self, factory, gen_rate, path, proportion):
        super().__init__(factory, gen_rate, path)
        self._proportion = proportion

    def update(self):
        """
        Increment _tick_count, generate packages if the tick is larger than
        rate, and decrease the time to produce a package.
        """
        self._tick_count += 1
        if self._tick_count >= self._gen_rate:
            self.generate_package()
            if self._gen_rate >= 30:
                self._gen_rate *= self._proportion
            self._tick_count = 0
