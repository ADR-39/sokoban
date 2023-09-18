from cell_type import CellType


ascii_repr = {
    CellType.UNKNOWN: '?',
    CellType.BLOCK: 'X',
    CellType.EMPTY: '.',
    CellType.PATH: '*',
    CellType.BOX: 'O',
    CellType.TARGET: '+',
    CellType.SATISFIED: '!',
    CellType.FIGURE: '|',
    CellType.TARGET_N_FIGURE: '|'
}

emoji_chick_repr = {
    CellType.UNKNOWN: '?',
    CellType.BLOCK: '🪨',
    CellType.EMPTY: '🟫',
    CellType.PATH: '⭐',
    CellType.BOX: '🥚',
    CellType.TARGET: '🪹',
    CellType.SATISFIED: '🪺',
    CellType.FIGURE: '🐥',
    CellType.TARGET_N_FIGURE: '🐥'
}
