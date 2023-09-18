
from figure_controller import InvalidMove
from queue import PriorityQueue
from game_solver import GameSolver
from itertools import count
from math import sqrt


class HillClimbing(GameSolver):
    """Hill climbing algorithm to solve the game."""

    def __init__(self, ctrl, targets, boxes, outfile=None):
        """Initialize a new HillClimbing instance."""
        super().__init__(ctrl.grid, targets, outfile)
        self.solved = False
        self.visited = set()

        # Priority Queue won't let us store tuple peacfully without this dummy counter
        # or we have to define __lt__ on the state type class
        dummycntr = count()

        states = PriorityQueue()
        states.put((0, next(dummycntr), ctrl))

        while not states.empty():
            _h, _, state = states.get()

            if state in self.visited: continue
            self.visited.add(state)
            self._statesprocessed += 1

            if self.grid_final_state_p(state.grid, targets):
                self.solved = True
                self.laststate = state
                break

            for mov in state.all_moves:
                try:
                    newstate = mov(state, spawn=True)
                    _h = self.h(newstate, newstate.targets(), newstate.boxes())

                    if newstate not in self.visited:
                        states.put((_h, next(dummycntr), newstate))
                        self._parent[newstate] = state

                except InvalidMove:
                    pass

        # run final stuff
        self.finalize()

    @staticmethod
    def h(grid, targets, boxes):
        """Compute the heuristic of the grid using normal distance equation."""
        d = 0
        for box in boxes:
            for target in targets:
                d += sqrt((box[0]-target[0])**2 + (box[1]-target[1])**2)

        return d
