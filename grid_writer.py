from grid import Grid
from cell_repr import emoji_chick_repr


class GridWriter:
    """Writer for grid."""

    def __init__(self, grid: Grid, outfile, cell_repr=emoji_chick_repr):
        """Initialize GridDisplayer object."""
        self.grid = grid
        self.outfile = outfile
        self.cell_repr = cell_repr

    def write(self):
        """Display grid content."""
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                self.outfile.write(self.cell_repr[col])
            self.outfile.write('\n')
        self.outfile.write('\n' + '-' * 10 + '\n')
