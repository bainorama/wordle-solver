import string

from solver_base import SolverBase


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
