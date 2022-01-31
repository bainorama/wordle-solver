import random

_BEST_STARTS = ["soare","arose"]


class Solver:
    def __init__(self):
        self._rules = []
        with open("/home/alastairb/Downloads/sgb-words.txt", "r") as f:
            self._dictionary = f.read().split("\n")
        self._dictionary = [w for w in self._dictionary if w != ""]

    def not_contains_letter(self, letter: str):
        def n_contains(word):
            return word.count(letter) == 0
        self._rules.append(n_contains)

    def not_contains(self, letters: str):
        for letter in letters:
            self.not_contains_letter(letter)

    def contains_at(self, letter: str, position: int):
        def _contains_at(word):
            return word[position] == letter
        self._rules.append(_contains_at)

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

    def contains_not_at(self, letter: str, position: int):
        def c(word):
            return word.count(letter) > 0 and not word[position] == letter
        self._rules.append(c)

    def available(self):
        res = []
        for word in self._dictionary:
            if all([rule(word) for rule in self._rules]):
                res.append(word)
        return res


if __name__ == '__main__':
    print(f"I suggest you start with: {random.choice(_BEST_STARTS)}")
    s = Solver()
    while True:
        try:
            s.correct_position(input("Correct position: "))
            s.incorrect_position(input("Incorrect position: "))
            s.not_contains_letter(input("Excluded: "))
            print(s.available())
        except Exception as e:
            print(f"Error while processing: {str(e)}")
            continue

