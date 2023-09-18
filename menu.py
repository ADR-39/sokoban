import curses
from interactive_session import InteractiveSession
import os
from enum import Enum


class MenuOptions(Enum):
    """Enumeration Type for represnting valid menu options."""

    REFRESH = 1
    BFS = 2
    DFS = 3
    UCS = 4
    HILL_CLIMBING = 5
    A_STAR = 6
    EXIT = 0


class Menu:
    """Game Menu."""

    def __init__(self, win, centery):
        """Initialize game menu."""
        self.win = win
        self.centery = centery
        self._crntselection = 0

    _opts = [opt.name for opt in MenuOptions]

    def display(self):
        """Display menu content."""
        self.win.clear()

        for idx, opt in enumerate(self._opts):
            self.win.addstr(idx, 0, opt, curses.A_DIM)

        self.win.addstr(self._crntselection, 0, self._opts[self._crntselection],
                        curses.A_REVERSE)

        self.win.refresh()

    def select_next(self):
        """Select next item in the menu."""
        self._crntselection += 1
        if self._crntselection >= len(MenuOptions):
            self._crntselection = 0

    def select_previous(self):
        """Select previous item in the menu."""
        self._crntselection -= 1
        if self._crntselection < 0:
            self._crntselection = 6

    @property
    def current_option(self):
        return MenuOptions((self._crntselection+1)%7)
