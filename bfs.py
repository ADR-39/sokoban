
from figure_controller import InvalidMove
from queue import Queue
from game_solver import GameSolver


class BFS(GameSolver):
    """BFS for finding the path required to solve the game."""

    def __init__(self, ctrl, targets, outfile=None):
        """Initialize a new BFS instance."""
        super().__init__(ctrl.grid, targets, outfile)
        self.solved = False
        self.discovered = set()

        q = Queue()
        q.put(ctrl)
        self.discovered.add(ctrl)

        while not q.empty():
            state = q.get()
            self._statesprocessed += 1

            if self.grid_final_state_p(state.grid, targets):
                self.solved = True
                self.laststate = state
                break

            for mov in state.all_moves:
                try:
                    newstate = mov(state, spawn=True)

                    if newstate not in self.discovered:
                        q.put(newstate)
                        self.discovered.add(newstate)
                        self._parent[newstate] = state

                except InvalidMove:
                    pass

        # run final stuff
        self.finalize()
