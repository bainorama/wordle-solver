import random
import string
from typing import Dict, List, Tuple

_BEST_STARTS = ["soare", "arose"]

with open("/home/alastairb/Downloads/sgb-words.txt", "r") as f:
    _DICTIONARY = [w for w in f.read().split("\n") if w != ""]


class SolverBase:
    def __init__(self):
        self._place_not_known: Dict[str, List[int]] = {}  # Dictionary of letter, list of places where it doesn't belong
        self._place_known: Dict[int, str] = {}  # Dictionary of place, letter
        self._non_letters: List[str] = []  # List of letters which are excluded
        self._remaining_words = _DICTIONARY[:]

    def available(self):
        return [word for word in _DICTIONARY if self.is_valid_guess(word)]

    def is_valid_guess(self, guess: str):
        unused_place_unknown_letters = list(self._place_not_known.keys())
        for index, letter in enumerate(guess):
            if letter in self._non_letters:
                return False
            if index in self._place_known and self._place_known[index] != letter:
                return False
            if letter in self._place_not_known:
                try:
                    indices = self._place_not_known[letter]
                    if index in indices:
                        return False
                    try:
                        unused_place_unknown_letters.remove(letter)
                    except ValueError:
                        pass
                except KeyError:
                    pass
        return len(unused_place_unknown_letters) == 0

    def not_contains(self, letters: str):
        for letter in letters:
            self.not_contains_letter(letter)

    def incorrect_position(self, s: str):
        if len(s) == 0:
            return
        if len(s) > 5:
            raise ValueError()
        for index, letter in enumerate(s):
            if letter.isalpha():
                self.contains_not_at(letter=letter, position=index)

    def correct_position(self, s: str):
        if len(s) == 0:
            return
        if len(s) > 5:
            raise ValueError()
        for index, letter in enumerate(s):
            if letter.isalpha():
                self.contains_at(letter=letter, position=index)

    def guess(self):
        raise NotImplementedError()

    def not_contains_letter(self, letter: str):
        self._non_letters.append(letter)

    def contains_at(self, letter: str, position: int):
        self._place_known[position] = letter

    def contains_not_at(self, letter: str, position: int):
        if letter in self._place_not_known:
            l = self._place_not_known[letter]
        else:
            l = []
            self._place_not_known[letter] = l
        l.append(position)


def try_remove(iterable, value):
    try:
        iterable.remove(value)
    except ValueError:
        pass


class SmarterSolver(SolverBase):
    def __init__(self):
        super().__init__()

    def guess(self):
        num_missing_places = len(self._place_not_known)
        num_known_places = len(self._place_known)
        num_missing_letters = 5 - (num_missing_places + num_known_places)

        self._remaining_words = [w for w in self._remaining_words if self.is_valid_guess(w)]
        # Do we know all the letters

        remaining_letters = list(string.ascii_lowercase)
        for l in self._place_not_known.keys():
            try_remove(remaining_letters, l)
        for l in self._place_known.values():
            try_remove(remaining_letters, l)
        for l in self._non_letters:
            try_remove(remaining_letters, l)

        word_scores = []

        for word in self._remaining_words:
            rl_this_word = remaining_letters[:]
            score = 0
            if num_missing_letters > 0:
                for letter in word:
                    if letter in rl_this_word:
                        rl_this_word.remove(letter)
                        score += 5
            for letter in word:
                if letter in self._place_not_known:
                    score += 5
            word_scores.append((word, score))
        w = max(word_scores, key=lambda p: p[1])
        return w[0]



class DumbSolver(SolverBase):
    def __init__(self):
        super().__init__()

    def guess(self):
        available = self.available()
        return random.choice(available)


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


def interactive_runner(s: SolverBase):
    print(f"I suggest you start with: {random.choice(_BEST_STARTS)}")
    while True:
        try:
            s.correct_position(input("Correct position: "))
            s.incorrect_position(input("Incorrect position: "))
            s.not_contains(input("Excluded: "))
            print(s.available())
        except Exception as e:
            print(f"Error while processing: {str(e)}")
            continue


def run_once(solver_class):
    solver = solver_class()
    word = random.choice(_DICTIONARY)
    attempts = run_game(solver, word)
    print(f"Solved in {attempts}")


if __name__ == '__main__':
    interactive_runner(SmarterSolver())
    # # run_once(SmarterSolver)
    # solver_classes = (SmarterSolver, DumbSolver)
    # # run_once(solver_class)
    # #
    # all_attempts = []
    # for i in range(100):
    #     word = random.choice(_DICTIONARY)
    #     solvers = [solver_class() for solver_class in solver_classes]
    #     attempts = [run_game(solver, word) for solver in solvers]
    #     all_attempts.append(attempts)
    # print(all_attempts)
    # for index in range(len(solver_classes)):
    #     avg = sum((v[index] for v in all_attempts)) / len(all_attempts)
    #     print(f"{solver_classes[index].__name__}:{avg}")
