import os
import curses


class GameTiler:
    def __init__(self, grid_size):
        self.grid_size = grid_size

        self.maxy = os.get_terminal_size()[0]
        self.startx = (self.maxy - self.grid_size[1])//2 - 2

        self.gridpad = curses.newpad(self.maxy, self.maxy)
        self.echowin = curses.newwin(1, self.maxy, grid_size[0]+self.grid_size[0], self.maxy//2-5)
        self.menuwin = curses.newwin(9, self.maxy, grid_size[0]+self.grid_size[0]+2, self.maxy//2-5)


    def refresh(self):
        self.maxy = os.get_terminal_size()[0]
        self.startx = (self.maxy - self.grid_size[1])//2 - 2

        self.gridpad = curses.newpad(self.maxy, self.maxy)
        self.echowin = curses.newwin(3, self.maxy, self.grid_size[0]*2, self.maxy//2-10)
        self.menuwin = curses.newwin(9, self.maxy, self.grid_size[0]*2+2, self.maxy//2-5)


    def display(self):
        # self.refresh()

        self.gridpad.refresh(0, 0,
                             1, self.startx,
                             self.grid_size[0]+1, self.startx+self.grid_size[1])
        self.echowin.refresh()
        self.menuwin.refresh()
