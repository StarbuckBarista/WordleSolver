from ast import literal_eval
from json import load
from progressbar import PercentageLabelBar, ProgressBar
from requests import get

from guesses.first_guesses import FirstGuesses
from guesses.last_guesses import LastGuesses

class Guess:
    def __init__(self, incorrect_words, known_minimums, known_maximums, incorrect_placements, correct_placements,
                 scrape_web, callback):
        self.incorrect_words = incorrect_words
        self.known_minimums = known_minimums
        self.known_maximums = known_maximums
        self.incorrect_placements = incorrect_placements
        self.correct_placements = correct_placements
        self.scrape_web = scrape_web

        self.possible_guesses = []
        self.get_possible_guesses()

        self.possible_answers = []
        self.get_possible_answers()

        progressbar_widgets = ["Progress: ", PercentageLabelBar(format=" %(percentage)2d%% ")]
        progress_stages = len(self.possible_guesses) if len(self.possible_answers) > 500 else len(self.possible_answers)

        with ProgressBar(widgets=progressbar_widgets, max_value=progress_stages) as bar:
            if len(self.possible_answers) > 500:
                callback(FirstGuesses(self.possible_guesses, self.possible_answers, bar.update).guess())
            else:
                callback(LastGuesses(self.possible_answers, bar.update).guess())

    def get_all_possible_guesses(self):
        if self.scrape_web:
            javascript = get("https://www.nytimes.com/games/wordle/main.18740dce.js").text
            list_start = javascript[javascript.index("Ma=") + 3:]
            list_end = list_start[:list_start.index("]") + 1]
            all_possible_guesses = literal_eval(list_end)

            javascript = get("https://www.nytimes.com/games/wordle/main.18740dce.js").text
            list_start = javascript[javascript.index("Oa=") + 3:]
            list_end = list_start[:list_start.index("]") + 1]
            all_possible_guesses += literal_eval(list_end)

            return all_possible_guesses
        else:
            with open("../words.json", "r") as words:
                data = load(words)
                return data["possible_guesses"]

    def get_all_possible_answers(self):
        if self.scrape_web:
            javascript = get("https://www.nytimes.com/games/wordle/main.18740dce.js").text
            list_start = javascript[javascript.index("Ma=") + 3:]
            list_end = list_start[:list_start.index("]") + 1]

            return literal_eval(list_end)
        else:
            with open("../words.json", "r") as words:
                data = load(words)
                return data["possible_answers"]

    def get_possible_guesses(self):
        all_possible_guesses = self.get_all_possible_guesses()

        for possible_guess in all_possible_guesses:
            all_valid_letters = True

            if possible_guess in self.incorrect_words:
                all_valid_letters = False

            for minimized_letter, minimum in self.known_minimums.items():
                if possible_guess.count(minimized_letter) < minimum:
                    all_valid_letters = False

            for maximized_letter, maximum in self.known_maximums.items():
                if possible_guess.count(maximized_letter) > maximum:
                    all_valid_letters = False

            for incorrect_placement, incorrect_letters in self.incorrect_placements.items():
                for incorrect_letter in incorrect_letters:
                    if possible_guess[incorrect_placement] == incorrect_letter:
                        all_valid_letters = False

            for correct_placement, correct_letter in self.correct_placements.items():
                if possible_guess[correct_placement] != correct_letter:
                    all_valid_letters = False

            if all_valid_letters:
                self.possible_guesses.append(possible_guess)

    def get_possible_answers(self):
        all_possible_answers = self.get_all_possible_answers()

        for possible_answer in all_possible_answers:
            all_valid_letters = True

            if possible_answer in self.incorrect_words:
                all_valid_letters = False

            for minimized_letter, minimum in self.known_minimums.items():
                if possible_answer.count(minimized_letter) < minimum:
                    all_valid_letters = False

            for maximized_letter, maximum in self.known_maximums.items():
                if possible_answer.count(maximized_letter) > maximum:
                    all_valid_letters = False

            for incorrect_placement, incorrect_letters in self.incorrect_placements.items():
                for incorrect_letter in incorrect_letters:
                    if possible_answer[incorrect_placement] == incorrect_letter:
                        all_valid_letters = False

            for correct_placement, correct_letter in self.correct_placements.items():
                if possible_answer[correct_placement] != correct_letter:
                    all_valid_letters = False

            if all_valid_letters:
                self.possible_answers.append(possible_answer)
