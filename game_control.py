"""
Logisti-Co game controller.
"""

from abc import ABC, abstractmethod
import pygame

# pylint: disable=no-name-in-module
from pygame.locals import (
    MOUSEBUTTONDOWN,
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

class MouseControl(Control):
    """
    A cursor based controller for Logisti Co. game.

    Attributes:
        events: a list of all of the user inputs taken by Pygame.
        mouse_pos: a tuple which contains the current x and y coordinates of
                   user's cursor.
    """

    def __init__(self, gameboard):
        """
        Initialize events and mouse position.

        Args:
            gameboard: a Factory instance.
        """
        super().__init__(gameboard)
        self.events = []
        self.mouse_pos = ()

    def control(self):
        """
        Get user input and update game model.
        """
        self.get_events()
        self.get_mouse_pos()
        click = self.detect_click()
        self.tower_placement(click)
        self.tower_removal(click)

    def detect_click(self):
        """
        Return click if MOUSEBUTTONDOWN event is detected, else 0.
        """
        for event in self.events:
            if event.type == MOUSEBUTTONDOWN:
                return event.button
        return 0

    def get_events(self):
        """
        Append pygame events into a separate list to preserve queue history.
        """
        self.events = pygame.event.get()

    def get_mouse_pos(self):
        """
        Save mouse position to tuple.
        """
        self.mouse_pos = pygame.mouse.get_pos()

    def tower_placement(self, click):
        """
        Attempt to place a tower where clicked.
        """
        if click == 1:
            if 0<=self.mouse_pos[0]<=800 and 0<=self.mouse_pos[1]<=600:
                self._gameboard.generate_tower(self.mouse_pos[0], \
                self.mouse_pos[1], 300, 100)

    def tower_removal(self, click):
        """
        Attempt to remove a tower where clicked.
        """
        if click == 3:
            clicked_towers = [tower for tower in self._gameboard.robots if \
                              tower.rect.collidepoint(self.mouse_pos)]
            for tower in clicked_towers:
                self._gameboard.remove_tower(tower)
