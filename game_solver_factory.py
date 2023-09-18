from game_solver import GameSolver
from bfs import BFS
from dfs import DFS
from uniform import UniformSearch
from hill_climbing import HillClimbing
from a_star import AStar
from menu import MenuOptions

class GameSolverFactory:
    SOLUTION_FILENAME = 'current_solution'

    def __init__(self, ctrl, targets, boxes):
        self.ctrl = ctrl
        self.targets = targets
        self.boxes = boxes

    def make(self, instance_type):
        inst = self._select_proper(instance_type)

        return inst

    def _select_proper(self, instance_type):
        cls = self._opts[instance_type]
        f = open(self.SOLUTION_FILENAME, 'w')
        if cls in [BFS, DFS, UniformSearch]:
            return cls(self.ctrl, self.targets, f)
        else:
            return cls(self.ctrl, self.targets, self.boxes, f)

    _opts = {
        MenuOptions.BFS: BFS,
        MenuOptions.DFS: DFS,
        MenuOptions.UCS: UniformSearch,
        MenuOptions.HILL_CLIMBING: HillClimbing,
        MenuOptions.A_STAR: AStar
    }
