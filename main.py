from curses import wrapper
import curses
from interactive_session import InteractiveSession
from game import Game
from sys import argv, stdin


def main(stdscr):
    """Bootstrap game."""
    configinfile = open(argv[1]) if len(argv) > 1 else stdin

    curses.curs_set(0)      # do not show the cursor
    game = Game(stdscr, configinfile)
    game.start()


if __name__ == '__main__':
    wrapper(main)
