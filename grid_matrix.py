import grid
import numpy as np
from cell_type import CellType
from copy import deepcopy


class GridMatrix(grid.Grid):
    """Grid Implementation using Numpy's 2D array."""
    DEFAULT_COST = 1

    def __init__(self, size=(8, 8), default_value=CellType.UNKNOWN):
        """Initialize grid matrix."""
        self.mat = np.full(size, default_value)
        self.costs = {}

    def __getitem__(self, idx: tuple):
        """Get cell at idx."""
        return self.mat[idx]

    def __setitem__(self, idx: tuple, value: CellType):
        """Set cell at idx."""
        self.mat[idx] = value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            (self is other or \
                np.array_equal(self.mat, other.mat))

    def __hash__(self):
        return hash(str(self.mat))

    def dump(self):
        """Dump grid content as are."""
        return self.mat

    def refresh(self):
        """Replace Path cells with Empty ones."""
        self.mat[self.mat == CellType.PATH] = CellType.EMPTY
        return self

    def pathize(self, path: list):
        """Path'ize the grid with path."""
        for p in path:
            if self.mat[p] == CellType.EMPTY:
                self.mat[p] = CellType.PATH
        return self

    def __deepcopy__(self, memo):
        """Return a new deep copy instance."""
        cls = self.__class__
        newinst = cls.__new__(cls)
        memo[id(self)] = newinst
        newinst.mat = deepcopy(self.mat)
        newinst.costs = deepcopy(self.costs)

        return newinst

    def cost(self, idx):
        return self.costs.get(idx) or self.DEFAULT_COST

    @property
    def surroundings(self, idx: tuple, depth=1):
        """Get Surrounding cells of idx."""
        col, row = idx
        up, right, down, left = col+1, row+1, col-1, row-1
        surr = ([], [], [], [])

        while True:
            if depth == 0:
                break

            upcell = (up, row)
            rightcell = (col, right)
            downcell = (down, row)
            leftcell = (col, left)

            surr[0].append(upcell)
            surr[1].append(rightcell)
            surr[2].append(downcell)
            surr[3].append(leftcell)

            up += 1
            right += 1
            down -= 1
            left -= 1

            depth -= 1

        return surr

    @staticmethod
    def _block_borders(mat, block_value=CellType.BLOCK):
        """Convert all border cells in the grid to BLOCK type."""
        for r in mat:
            r[0] = r[-1] = block_value

        mat[0] = block_value
        mat[-1] = block_value

    @classmethod
    def make_from_input(cls, in_list):
        """Make GridMatrix object from in_list input."""
        size, blocks, boxes, targets, weights, figure = in_list
        newinst = cls(size=size, default_value=CellType.EMPTY)

        GridMatrix._block_borders(newinst)

        for b in blocks:
            newinst.mat[b] = CellType.BLOCK
        for b in boxes:
            newinst.mat[b] = CellType.BOX
        for t in targets:
            newinst.mat[t] = CellType.TARGET

        for weight in weights:
            c, w = weight
            newinst.costs[c] = w

        newinst.mat[figure] = CellType.FIGURE
        return newinst

    def cells(self, start: tuple, step: tuple, key):
        res = []
        idx = start

        while True:
            if key(start):
                break
            res.append(idx)

            idx[0], idx[1] = idx[0]+step[0], idx[1]+step[1]

        return res

    def move(self, idx0: tuple, idx1: tuple,):
        """Move cell content from idx0 to idx1."""

        fixed_idx0 = self[idx0].detach(moveable=False)
        mov_idx0 = self[idx0].detach()

        self[idx0] = fixed_idx0
        self[idx1] = self[idx1].combine(mov_idx0)
