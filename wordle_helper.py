#!/usr/bin/env python3
from solver_base import *
from smarter import SmarterSolver
import random


def interactive_runner(s: SolverBase):
    print(f"I suggest you start with: {random.choice(BEST_STARTS)}")
    while True:
        try:
            s.correct_position(input("Letters in correct position (e.g. 'ar s ' : "))
            s.incorrect_position(input("Letter in incorrect position: "))
            s.not_contains(input("Excluded letters: "))
            print(f"Suggested guesses: {s.available()}")
        except Exception as e:
            print(f"Error while processing: {str(e)}")
            continue


if __name__ == '__main__':
    interactive_runner(SmarterSolver())
