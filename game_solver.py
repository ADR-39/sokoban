from cell_type import CellType
from grid_writer import GridWriter
from time import time


class GameSolver:
    """Superclass for solving the game."""

    def __init__(self, grid, targets, outfile=None):
        """Initialize a new GameSolver instance."""
        self.grid = grid
        self.targets = targets
        self.solved = False     # TODO: property not an attribute!
        self.laststate = None
        self.outfile = outfile
        self.tic = time()
        self.tac = None

        self._parent = {}
        self._p = []
        self._path = []
        self._count = 0
        self._statesprocessed = 0

    def final_state_p(self):
        """Predicate if grid state is final."""
        return self.grid_final_state_p(self.grid, self.targets)

    @staticmethod
    def grid_final_state_p(grid, targets):
        """Predicate if grid state is final."""
        for idx in targets:
            if grid[idx] != CellType.SATISFIED:
                return False

        return True

    @property
    def steps(self):
        return len(self._path)

    @property
    def path(self):
        if not self._path:
            self._path = tuple(map(lambda state: state.figure_pos, self.parent))

        return self._path

    @property
    def states_processed(self):
        return self._count

    @property
    def parent(self):
        if not self._p:
            self._p = []
            state = self.laststate
            while state:
                self._p.append(state)
                state = self._parent.get(state)

            self._p.reverse()

        return self._p

    @property
    def duration(self):
        return self.tac - self.tic

    def finalize(self):
        """Final steps to be made after running the solve algorithm."""

        self.tac = time()

        if self.outfile:
            self.outfile.write("Search result:\n")
            self.outfile.write('-' * 9 + '\n')
            for p in self.parent:
                GridWriter(p.grid.dump(), self.outfile).write()

        self.grid.pathize(self.path)
