
from figure_controller import InvalidMove
from queue import PriorityQueue
from game_solver import GameSolver
from itertools import count
from grid_writer import GridWriter

class UniformSearch(GameSolver):
    """Uniform search algorithm to solve the game."""

    def __init__(self, ctrl, targets, outfile=None):
        """Initialize a new UniformSearch instance."""
        super().__init__(ctrl.grid, targets, outfile)
        self.solved = False
        self.visited = set()

        # Priority Queue won't let us store tuple peacfully without this dummy counter
        # or we have to define __lt__ on the state type class
        dummycntr = count()

        states = PriorityQueue()
        states.put((1, next(dummycntr), ctrl))

        while not states.empty():
            cost, _, state = states.get()

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

                    if newstate not in self.visited:
                        newcost = state.grid.cost(newstate.figure_pos)
                        states.put((cost+newcost, next(dummycntr), newstate))

                        # parent goes for the higher cost
                        #self._parent[newstate] = state if newcost < oldcost else oldstate

                        # update parent[newstate]
                        if newstate in self._parent:
                            oldcost = state.grid.cost(self._parent[newstate].figure_pos)
                            if newcost < oldcost:
                                self._parent[newstate] = state
                        else:
                            self._parent[newstate] = state

                except InvalidMove:
                    pass

        # run final stuff
        self.finalize()
