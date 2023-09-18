from grid_matrix import GridMatrix
from cell_repr import emoji_chick_repr
from grid import dummy_input
from grid_displayer import GridDisplayer
from figure_controller import FigureController, InvalidMove
from game_config_reader import GameConfigReader
from game_solver import GameSolver


class InteractiveSession:
    """Interactive session to play the game."""

    def __init__(self, stdscr, instream):
        """Initialize interactive session."""
        self.stdscr = stdscr

        reader = GameConfigReader(instream)
        reader.normal_read()
        inlist = reader.tolist()

        figure_pos = inlist[-1]
        targets = inlist[3]
        self.boxes = inlist[2]
        grid = GridMatrix.make_from_input(inlist)
        self.displayer = GridDisplayer(grid, self.stdscr, emoji_chick_repr)
        self.displayer.display()

        self.ctrl = FigureController(figure_pos, grid)
        self.gamechecker = GameSolver(grid, targets)


    def listen(self):
        """Listen for input."""

        try:
            key = self.stdscr.getkey()

            if (key == 'w'):
                self.ctrl.move_up()
            elif (key == 'd'):
                self.ctrl.move_right()
            elif (key == 's'):
                self.ctrl.move_down()
            elif (key == 'a'):
                self.ctrl.move_left()

        except InvalidMove:
            pass
        except:
            pass

    def move(self, key):
        """Move figure by user input."""
        try:
            self._mov_keys[key]()
        except InvalidMove:
            pass


    @property
    def _mov_keys(self):
        return {
            'w': self.ctrl.move_up,
            'd': self.ctrl.move_right,
            's': self.ctrl.move_down,
            'a': self.ctrl.move_left
        }

    def main(self):
        self.stdscr.clear()
        self.displayer.display()

    def start(self, inlist=None):
        """Start the interactive session."""
        if not inlist:
            inlist = dummy_input()

        figure_pos = inlist[-1]
        grid = GridMatrix.make_from_input(inlist)
        self.displayer = GridDisplayer(grid, self.stdscr, emoji_chick_repr)
        self.displayer.display()

        self.ctrl = FigureController(figure_pos, grid)
