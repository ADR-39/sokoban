from grid import Grid
from cell_repr import ascii_repr


class GridDisplayer:
    """Displayer for grid."""

    def __init__(self, grid: Grid, stdscr, cell_repr=ascii_repr):
        """Initialize GridDisplayer object."""
        self.grid = grid
        self.stdscr = stdscr
        self.cell_repr = cell_repr

    def display(self):
        """Display grid content."""
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                self.stdscr.addstr(r, c, self.cell_repr[col])

        # self.stdscr.refresh(0, 0, 0, 0, 20, 20)
