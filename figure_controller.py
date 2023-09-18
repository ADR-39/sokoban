from grid import Grid
from cell_type import CellType
from copy import deepcopy
import numpy as np


class InvalidMove(Exception):
    """Invalid movement exception."""

    pass


class FigureController:
    """Figure Controller on grid."""

    def __init__(self, figure_pos, grid: Grid):
        """Initialize a figure controller."""
        self.grid = grid
        self.pos = figure_pos

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            (self is other or \
             self.grid == other.grid and self.pos == other.pos)

    def __hash__(self):
        return hash((self.grid, self.pos))

    @staticmethod
    def _nextmove(idx: tuple, step: tuple, depth=1):
        """Aggregate all next depth indexes."""
        nxtidx = []
        for i in range(1, depth+1):
            newidx = idx[0]+step[0]*i, idx[1]+step[1]*i
            nxtidx.append(newidx)

        return nxtidx

    def _move_to_p(self, nxtidx: tuple, nxtnxtidx: tuple):
        """Predicate if move to nextidx is valid."""
        nxtblock = self.grid[nxtidx] == CellType.BLOCK
        nxtbox = self.grid[nxtidx] in [CellType.BOX, CellType.SATISFIED]
        nxtnxtrigid = self.grid[nxtnxtidx] in [CellType.BLOCK, CellType.BOX]

        return not (nxtblock or nxtbox and nxtnxtrigid)

    @staticmethod
    def add(idx0: tuple, idx1: tuple):
        """Add 2 complex numbers (x, y)."""
        return idx0[0] + idx1[0], idx0[1] + idx1[1]

    @property
    def figure_pos(self):
        """Get the position of the figure."""
        return self.pos

    def required_next_steps(self, step: tuple):
        """Compute the required path depth."""
        f = open('outfile', 'w')
        f.write(repr(self.pos) + '\n')
        f.write(repr(step))
        nxt = self.add(self.pos, step)
        if self.grid[nxt].step_on_p():
            return 1
        if self.grid[nxt].moveable():
            nxtnxt = self.add(nxt, step)
            if (self.grid[nxtnxt].step_on_p()):
                return 2
        return 0

    def __deepcopy__(self, memo):
        """Return a new deep copy instance."""
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def boxes(self):
        return np.asarray(np.where(self.grid.mat == CellType.BOX)).T

    def targets(self):
        return np.asarray(np.where(self.grid.mat == CellType.TARGET)).T

    def move_left(self, spawn=False):
        """Move figure left."""
        return self._move((0, -1), spawn)

    def move_right(self, spawn=False):
        """Move figure right."""
        return self._move((0, 1), spawn)

    def move_up(self, spawn=False):
        """Move figure up."""
        return self._move((-1, 0), spawn)

    def move_down(self, spawn=False):
        """Move figure down."""
        return self._move((1, 0), spawn)


    def _move(self, step, spawn=False):
        inst = self if not spawn else deepcopy(self)

        depth = inst.required_next_steps(step)
        nxtcells = [inst.pos] + inst._nextmove(inst.pos, step, depth)
        nxtcells_pairs = zip(nxtcells[-2::-1], nxtcells[::-1])

        for previdx, idx in nxtcells_pairs:
            if not inst._move_to_p(previdx, idx):
                raise InvalidMove("Cannot go there!")
            inst.grid.move(previdx, idx)

        # update current figure position
        if len(nxtcells) > 1:
            inst.pos = nxtcells[1]

        return inst

    all_moves = (move_up, move_right, move_down, move_left)

    @property
    def valid_moves(self):
        """Get all valid moves around figure."""
        raise "Not implemented yet."
