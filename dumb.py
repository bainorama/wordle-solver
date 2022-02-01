from solver_base import SolverBase
import random


class DumbSolver(SolverBase):
    def __init__(self):
        super().__init__()

    def guess(self):
        available = self.available()
        return random.choice(available)
