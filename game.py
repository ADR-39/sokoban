import curses
from interactive_session import InteractiveSession
import os
from menu import Menu, MenuOptions
from game_solver import GameSolver
from bfs import BFS
from dfs import DFS
from uniform import UniformSearch
from hill_climbing import HillClimbing
from a_star import AStar
from game_solver_factory import GameSolverFactory
from game_tiler import GameTiler


class EchoArea:

    def __init__(self, win):
        self.win = win

    def display(self, msg: str):
        self.win.clear()
        #self.win.addstr(0, 0, f'"{msg}"', curses.A_ITALIC)
        self.win.addstr(0, 0, f'"{msg}"')
        # self.win.refresh()


class Game:

    def __init__(self, stdscr, instream):
        self.stdscr = stdscr
        self.instream = instream

    def listen(self):
        key = self.stdscr.getkey()

        if key == 'KEY_DOWN':
            self.gamemenu.select_next()

        elif key == 'KEY_UP':
            self.gamemenu.select_previous()

        elif key == 'q':
            exit(0)

        elif key == '\n':
            if self.gamemenu.current_option == MenuOptions.REFRESH:
                self.session.ctrl.grid.refresh()
                self.echoarea.display('Refreshing..')
            elif self.gamemenu.current_option == MenuOptions.EXIT:
                exit(0)
            else:
                searchinst = self.gamesolverfact.make(self.gamemenu.current_option)
                self.echoarea.display(f"Launching {self.gamemenu.current_option}..")
                _cond = searchinst.solved
                self.echoarea.display(f"{self.gamemenu.current_option}: " \
                                      f"states: {searchinst._statesprocessed}, " \
                                      "time: %.2f, " % searchinst.duration + \
                                      f"steps: {len(searchinst._path)}.")

        elif key == 'w':
            self.session.move('w')
            self.echoarea.display("Going up..")
        elif key == 'd':
            self.session.move('d')
            self.echoarea.display("Going right..")
        elif key == 's':
            self.session.move('s')
            self.echoarea.display("Going down..")
        elif key == 'a':
            self.session.move('a')
            self.echoarea.display("Going left..")

    def start(self):
        maxy = os.get_terminal_size()[0]

        self.instream.seek(0)
        size = self.instream.readline().split()
        self.instream.seek(0)

        size = int(size[0]), int(size[1])
        self.tiler = GameTiler(grid_size=size)

        self.stdscr.refresh()

        self.gamemenu = Menu(self.tiler.menuwin, maxy//2)
        self.gamemenu.display()

        # TODO should add these
        # reader = GameConfigReader(instream)
        # reader.normal_read()
        # inlist = reader.tolist()

        self.session = InteractiveSession(self.tiler.gridpad, self.instream)
        self.echoarea = EchoArea(self.tiler.echowin)
        self.echoarea.display('Go!')
        self.gamechecker = self.session.gamechecker
        self.gamesolverfact = GameSolverFactory(self.session.ctrl,
                                                self.gamechecker.targets,
                                                self.session.boxes)

        while True:
            if self.gamechecker.final_state_p():
                self.echoarea.display('You won!')

            self.gamemenu.display()
            self.session.main()
            self.tiler.display()

            self.listen()
