from curses import wrapper
import curses


def main(stdscr):
    """Bootstrap game."""
    pad = curses.newpad(100, 100)
    pad.addstr('abc')

    pad.refresh(0, 0, 1, 1, 1, 1)
    pad.getkey()


if __name__ == '__main__':
    wrapper(main)


def start():
    tiler = GamerTiler((newpad, echowin, menuwin))
    tiler.display()
