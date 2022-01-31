import random

_BEST_STARTS = ["soare","arose"]


with open("/home/alastairb/Downloads/sgb-words.txt", "r") as f:
    _DICTIONARY = [w for w in f.read().split("\n") if w != ""]


class SolverBase:
    def __init__(self):
        pass

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

    def correct_position(self, s:str):
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
        raise NotImplementedError()

    def contains_at(self, letter: str, position: int):
        raise NotImplementedError()

    def contains_not_at(self, letter: str, position: int):
        raise NotImplementedError()


class DumbSolver(SolverBase):
    def __init__(self):
        self._rules = []

    def not_contains_letter(self, letter: str):
        def n_contains(word):
            return word.count(letter) == 0
        self._rules.append(n_contains)

    def contains_at(self, letter: str, position: int):
        def _contains_at(word):
            return word[position] == letter
        self._rules.append(_contains_at)

    def contains_not_at(self, letter: str, position: int):
        def c(word):
            return word.count(letter) > 0 and not word[position] == letter
        self._rules.append(c)

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

    def correct_position(self, s:str):
        if len(s) == 0:
            return
        if len(s) > 5:
            raise ValueError()
        for index, letter in enumerate(s):
            if letter.isalpha():
                self.contains_at(letter=letter, position=index)

    def available(self):
        res = []
        for word in _DICTIONARY:
            if all([rule(word) for rule in self._rules]):
                res.append(word)
        return res

    def guess(self):
        available = self.available()
        return random.choice(available)


def run_game(solver: SolverBase):
    word = random.choice(_DICTIONARY)
    print(f"word is {word}")
    tries = 0
    while True:
        guess = solver.guess()
        tries += 1
        if guess is None:
            raise Exception("Could not solve")
        print(f"Guess is {guess}")
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
            s.not_contains_letter(input("Excluded: "))
            print(s.available())
        except Exception as e:
            print(f"Error while processing: {str(e)}")
            continue


if __name__ == '__main__':
    solver_class = DumbSolver
    all_attempts = []
    for i in range(1000):
        solver = solver_class()
        attempts = run_game(solver)
        print(f"Solved in {attempts}")
        all_attempts.append(attempts)
    print(all_attempts)
    print(f"Average was {sum(all_attempts)/len(all_attempts)}")



