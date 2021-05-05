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
        click = self.detect_click()
        self.tower_placement(click)
        self.tower_removal(click)
        
    def detect_click(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                print(event.button)
                return event.button
        return 0
    

    def tower_placement(self, click):
        """
        Attempt to place a tower where clicked
        """
        if click == 1:
            mouse_position = pygame.mouse.get_pos()
            # if 0<=mouse_position[0]<=800 and 0<=mouse_position[1]<=600:
            self._gameboard.generate_tower(mouse_position[0], \
            mouse_position[1], 300, 100)
    
    def tower_removal(self, click):
        """
        Attempt to remove a tower where clicked.
        """
        if click == 3:
            print("removing towers")
            mouse_position = pygame.mouse.get_pos()
            clicked_towers = [tower for tower in self._gameboard._robots if tower._rect.collidepoint(mouse_position)]
            for tower in clicked_towers:
                self._gameboard.remove_tower(tower)
