from abc import ABC, abstractmethod


class Grid(ABC):
    """Abstract Grid."""

    @abstractmethod
    def __getitem__(self, idx):
        """Get cell at idx."""
        pass

    @abstractmethod
    def __setitem__(self, idx):
        """Set cell at idx."""
        pass

    @abstractmethod
    def dump(self):
        """Dump grid content as are."""
        pass

    @property
    @abstractmethod
    def surroundings(self, idx):
        """Get Surrounding cells of idx."""
        pass

    @abstractmethod
    def move(idx0, idx1):
        """Move cell content from idx0 to idx1."""
        pass


def dummy_input():
    """Return a dummy input for grid."""
    return [
        (10, 10),                          # size
        [(2, 2), (1, 1), (6, 7), (6, 2)],  # blocks
        [(1, 4), (4, 3)],                  # boxes
        [(4, 1), (5, 2)],                  # targets
        (5, 5)                             # figure
    ]
