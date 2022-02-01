from dumb import DumbSolver
from smarter import SmarterSolver
from solver_base import SolverBase, DICTIONARY
import random


def run_game(solver: SolverBase, word: str):
    tries = 0
    while True:
        guess = solver.guess()
        tries += 1
        if guess is None:
            raise Exception("Could not solve")
        if guess == word:
            return tries

        for index, letter in enumerate(guess):
            count = word.count(letter)
            if count == 0:
                solver.not_contains_letter(letter)
            else:
                if word[index] == letter:
                    solver.contains_at(letter=letter, position=index)
                else:
                    solver.contains_not_at(letter=letter, position=index)


if __name__ == "__main__":
    solver_classes = (SmarterSolver, DumbSolver)
    all_attempts = []
    for i in range(100):
        word = random.choice(DICTIONARY)
        solvers = [solver_class() for solver_class in solver_classes]
        attempts = [run_game(solver, word) for solver in solvers]
        all_attempts.append(attempts)
    for index in range(len(solver_classes)):
        avg = sum((v[index] for v in all_attempts)) / len(all_attempts)
        print(f"{solver_classes[index].__name__}:{avg}")
