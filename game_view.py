import pygame
from abc import ABC, abstractmethod

class View(ABC):
    """
    View Logisti Co. game.

    Attrbitues:
        _gameboard: a Factory instance.
    """

    def __init__(self,gameboard):
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
