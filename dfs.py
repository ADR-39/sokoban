from figure_controller import InvalidMove
from queue import Queue
from game_solver import GameSolver


class DFS(GameSolver):

    def __init__(self, ctrl, targets, outfile=None):
        super().__init__(ctrl.grid, targets, outfile)
        self.solved = False
        self.visited = set([ctrl])
        s = [ctrl]

        while s:
            state = s.pop()
            self._statesprocessed += 1

            if self.grid_final_state_p(state.grid, targets):
                self.solved = True
                self.laststate = state
                break

            for mov in state.all_moves:
                try:
                    newstate = mov(state, spawn=True)

                    if newstate not in self.visited:
                        s.append(newstate)
                        self.visited.add(newstate)
                        self._parent[newstate] = state

                except InvalidMove:
                    pass

        # run final stuff
        self.finalize()
