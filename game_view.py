"""
Logisti-Co game view.
"""
from abc import ABC, abstractmethod
import pygame
# pylint: disable=no-member
pygame.init()

class View(ABC):
    """
    View Logisti Co. game.

    Attrbitues:
        _gameboard: the active Factory instance.
        _screen: the PyGame Display instance.
    """

    def __init__(self, gameboard):
        """
        Initialize gameboard.

        Args:
            gameboard: a Factory instance.
        """
        self._gameboard = gameboard

    @property
    def gameboard(self):
        """
        Return the Factory instance being represented by this view.
        """
        return self._gameboard

    @abstractmethod
    def draw(self):
        """
        Draw the gameboard Factory instance.
        """


class PyGameView(View):
    """
    A PyGame viewer for Logisti Co.

    Attributes:
        _screen: the PyGame Display instance.
        _successful_packages: a VisualText which shows the number of packages
                              that Tower instances have handled.
        _lives: a VisualText which shows the number of lives the player has
                left.
        _available_towers: a VisualText which shows the number of Tower
                           instances available to be placed.
    """

    def __init__(self, gameboard):
        """
        Initialize PyGameView

        Args:
            gameboard: a Factory instance.
        """
        super().__init__(gameboard)
        self._screen = pygame.display.set_mode([1100, 600])
        self._successful_packages = VisualText("Successes: ", (850, 20), 30)
        self._lives = VisualText("Lives: ", (850, 70), 30)
        self._available_towers = VisualText("Money: ", (850, 120), 30)

    def draw(self):
        """
        Updates the view to include background image, packages, and towers.
        """
        background = pygame.image.load("./game_assets/factory_path/Map1.png")
        menu = pygame.image.load("./game_assets/factory_path/menu_back.png")
        self._screen.blit(background, (0, 0))
        self._screen.blit(menu, (800, 0))
        for package in self._gameboard.packages:
            self._screen.blit(package.surf, package.rect)

        for tower in self._gameboard.robots:
            self._screen.blit(tower.surf, tower.rect)

        self._successful_packages.update(self._gameboard.packed)
        self._lives.update(10 - self._gameboard.failed)
        self._available_towers.update(self._gameboard.money)
        self._screen.blit(self._successful_packages.text, \
                          self._successful_packages.location)
        self._screen.blit(self._lives.text, \
                          self._lives.location)
        self._screen.blit(self._available_towers.text, \
                          self._available_towers.location)
        pygame.display.flip()

class VisualText():
    """
    A surface container object for displaying pygame text

    Attributes:
        _font: a pygame Font instance used for rendering fonts.
        text_label: a string denoting what to place before text being passed
        in. (eg "Score: ")
        color: a tuple denoting RGB color values for the text.
    """

    def __init__(self, text_label, location, font_size):
        self._font = pygame.font.Font('./game_assets/fonts/Mayor.ttf', font_size)
        self.text_label = text_label
        self.color = (255, 255, 255)
        self._text = self._font.render(text_label, True, self.color)
        self.location = location

    def update(self, text):
        """
        Update the text to display.

        Args:
            text: Any object instance with a repr that will be displayed using
                  text.
        """

        self._text = self._font.render(self.text_label + str(text), \
            True, (255, 255, 255))

    @property
    def text(self):
        """
        Returns a pygame text Surface to be overlayed on the game window.
        """
        return self._text

class HealthBar(pygame.sprite.Sprite):
    """
    Visualization of the user's current health.

    Attributes:
        _current_length: an int representing the current length of the healthbar
        _base_length: an int which represents 
    """
    def __init__(self, base_length, base_width):
        """
        Initialize healthbar characteristics.

        Args:
            base_length: an int representing the initial length of the
                         healthbar.
            base_width: an int representing the initial width of the healthbar.
        """
        self._current_length = length
        self._base_length = length
        self._width = width
        self._full_health = 10
        self._location = []

    def update(self,health):
        """
        Update health value.

        Args:
            health: an int representing the user's health
        """
        self._length = self._base_length*health
        pass