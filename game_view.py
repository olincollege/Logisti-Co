import pygame
from abc import ABC, abstractmethod
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
        pass


class PyGameView(View):
    """
    A PyGame viewer for Logisti Co.

    Attributes:
        _screen: the PyGame Display instance.
    """
    
    def __init__(self, gameboard):
        super(PyGameView, self).__init__(gameboard)
        self._screen = pygame.display.set_mode([800, 600])
        
    def draw(self):
        """
        Updates the view to include background image, packages, and towers.
        """
        background = pygame.image.load("./game_assets/factory_path/Map1.png")
        self._screen.blit(background, (0, 0))
        for package in self._gameboard._packages:
            self._screen.blit(package._surf, package._rect)
        pygame.display.flip() 