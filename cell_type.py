from enum import Enum


class InvalidCellCombination(Exception):
    """Exception for combining 2 uncombinable cell types."""

    pass


class InvalidCellDetaching(Exception):
    """Exception for detaching an undetachable cell type."""

    pass



class CellType(Enum):
    """Cell Types that are used in grid."""

    UNKNOWN = 0
    BLOCK = 1
    EMPTY = 2
    BOX = 3
    TARGET = 4
    SATISFIED = 5
    FIGURE = 6
    TARGET_N_FIGURE = 7
    PATH = 8

    def moveable(self):
        """Can self move?"""
        return self in [CellType.BOX, CellType.FIGURE, CellType.SATISFIED]

    def step_on_p(self):
        """Can self get stepped on?"""
        return self in [CellType.EMPTY, CellType.TARGET, CellType.PATH]

    def combine(self, other):
        """Combine 2 CellType types."""
        mov, fixed = (self, other) if self.moveable() else (other, self)
        for comb, _mov, _fixed in _combination_rules:
            if mov == _mov and fixed == _fixed:
                return comb

        if other in [CellType.EMPTY, CellType.PATH]: return self

        raise InvalidCellCombination(f"{self} cannot be combined with {other}.")


    def detach(self, moveable=True):
        """
        Detach CellType from another.
        if movealbe is True, detach the moveable part,
        otherwise detach the other.
        """
        for comb, mov, fixed in _combination_rules:
            if self == comb:
                return mov if moveable else fixed

        if self in [CellType.EMPTY, CellType.PATH]: return self

        raise InvalidCellDetaching(f"{self} cannot be detached.")


_combination_rules = (
    # COMBINATION            , MOVEABLE       , FIXED
    (CellType.TARGET_N_FIGURE, CellType.FIGURE, CellType.TARGET),
    (CellType.SATISFIED      , CellType.BOX   , CellType.TARGET),
    (CellType.FIGURE         , CellType.FIGURE, CellType.EMPTY) ,
    (CellType.BOX            , CellType.BOX   , CellType.EMPTY) ,
    (CellType.FIGURE         , CellType.FIGURE, CellType.PATH) ,
    (CellType.BOX            , CellType.BOX   , CellType.PATH) ,
)
