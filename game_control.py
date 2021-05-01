import pygame
from abc import ABC, abstractmethod 

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT,
)

class Control(ABC):
    """
    Control Logisti Co. game.

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
    def control(self):
        """
        Control the game.
        """
        pass

class MouseControl(Control):
    """
    A cursor based controller for Logisti Co. game.
    """
    
    def control(self):
        self.tower_placement()

    def detect_click(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                return True
        return False
    
    def tower_placement(self):
        if self.detect_click():
            mouse_position = pygame.mouse.get_pos()
            self._gameboard.generate_tower(mouse_position[0], mouse_position[1], 300, 100)