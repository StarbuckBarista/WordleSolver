from difflib import SequenceMatcher
from itertools import combinations
from pandas import DataFrame

class LastGuesses:
    def __init__(self, possible_answers, progressbar_update):
        self.possible_answers = possible_answers
        self.progressbar_update = progressbar_update

    def guess(self):
        if len(self.possible_answers) == 1:
            return self.possible_answers[0]

        optimal_word = None
        optimal_rating = None

        progressbar_stage = -1

        for possible_guess in self.possible_answers:
            progressbar_stage += 1
            self.progressbar_update(progressbar_stage)

            possible_answers_ratings = []

            for possible_answer in self.possible_answers:
                incorrect_words = [possible_guess]
                known_minimums = {letter: minimum for letter, minimum in
                                  zip([character for character in possible_guess if character in possible_answer],
                                      [abs(possible_guess.count(character) - possible_answer.count(character))
                                       for character in possible_guess if character in possible_answer])}
                known_maximums = {letter: maximum for letter, maximum in
                                  zip([character for character in possible_guess if possible_guess.count(character) >
                                       possible_answer.count(character)],
                                      [possible_answer.count(character) for character in possible_guess if
                                       possible_guess.count(character) > possible_answer.count(character)])}
                incorrect_placements = {word_index: letters for word_index, letters in
                                        zip([index for index in range(len(possible_guess)) if
                                             possible_guess[index] in possible_answer and possible_guess[index] !=
                                             possible_answer[index]],
                                            [[possible_answer[index]] for index in range(len(possible_guess)) if
                                             possible_guess[index] in possible_answer and possible_guess[index] !=
                                             possible_answer[index]])}
                correct_placements = {word_index: letters for word_index, letters in
                                      zip([index for index in range(len(possible_guess)) if
                                           possible_guess[index] in possible_answer and possible_guess[index] ==
                                           possible_answer[index]],
                                          [possible_guess[index] for index in range(len(possible_guess)) if
                                           possible_guess[index] in possible_answer and possible_guess[index] ==
                                           possible_answer[index]])}

                possible_answers_1 = []

                for possible_answer_1 in self.possible_answers:
                    all_valid_letters = True

                    if possible_answer_1 in incorrect_words:
                        all_valid_letters = False

                    for minimized_letter, minimum in known_minimums.items():
                        if possible_answer_1.count(minimized_letter) < minimum:
                            all_valid_letters = False

                    for maximized_letter, maximum in known_maximums.items():
                        if possible_answer_1.count(maximized_letter) > maximum:
                            all_valid_letters = False

                    for incorrect_placement, incorrect_letters in incorrect_placements.items():
                        for incorrect_letter in incorrect_letters:
                            if incorrect_letter not in possible_answer_1 or \
                                    possible_answer_1[incorrect_placement] == incorrect_letter:
                                all_valid_letters = False

                    for correct_placement, correct_letter in correct_placements.items():
                        if possible_answer_1[correct_placement] != correct_letter:
                            all_valid_letters = False

                    if all_valid_letters:
                        possible_answers_1.append(possible_answer_1)

                similarity_rating = self.rate_possible_answers(possible_answers_1)
                length_rating = len(self.possible_answers) - len(possible_answers_1)
                origin_distance = ((similarity_rating ** 2) + (length_rating ** 2)) ** 0.5

                possible_answers_ratings.append(origin_distance)

            average = sum(possible_answers_ratings) / len(possible_answers_ratings)

            if optimal_rating is None or average > optimal_rating:
                optimal_word = possible_guess
                optimal_rating = average

        return optimal_word

    @staticmethod
    def rate_possible_answers(possible_answers):
        if 0 <= len(possible_answers) <= 1:
            return 1

        def similarity(word_one, word_two):
            sequence = SequenceMatcher(a=word_one, b=word_two)
            return sequence.ratio()

        matches = combinations(possible_answers, 2)
        data_frame = DataFrame(list(matches))
        similarities = data_frame.apply(lambda match: similarity(match[0], match[1]), axis=1)

        return similarities.mean()
