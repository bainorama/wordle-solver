from typing import Dict, List

BEST_STARTS = ["soare", "arose"]

with open("words.txt", "r") as f:
    DICTIONARY = [w for w in f.read().split("\n") if w != ""]


class SolverBase:
    def __init__(self):
        self._place_not_known: Dict[str, List[int]] = {}  # Dictionary of letter, list of places where it doesn't belong
        self._place_known: Dict[int, str] = {}  # Dictionary of place, letter
        self._non_letters: List[str] = []  # List of letters which are excluded
        self._remaining_words = DICTIONARY[:]

    def available(self):
        return [word for word in DICTIONARY if self.is_valid_guess(word)]

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
        l = []
        if letter in self._place_not_known:
            l = self._place_not_known[letter]
        else:
            self._place_not_known[letter] = l
        l.append(position)
