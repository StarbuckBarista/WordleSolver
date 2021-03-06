from itertools import combinations
from pandas import DataFrame

class FirstGuesses:
    def __init__(self, incorrect_words, known_minimums, known_maximums, incorrect_placements, correct_placements,
                 possible_guesses, possible_answers, progressbar_update):
        self.incorrect_words = incorrect_words
        self.known_minimums = known_minimums
        self.known_maximums = known_maximums
        self.incorrect_placements = incorrect_placements
        self.correct_placements = correct_placements
        self.possible_guesses = possible_guesses
        self.possible_answers = possible_answers
        self.progressbar_update = progressbar_update

    def guess(self):
        if len(self.possible_answers) == 1:
            return self.possible_answers[0]

        optimal_word = None
        optimal_rating = None

        progressbar_stage = -1

        for possible_guess in self.possible_guesses:
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
                                             possible_guess[index] != possible_answer[index]],
                                            [[possible_answer[index]] for index in range(len(possible_guess)) if
                                             possible_guess[index] != possible_answer[index]])}
                correct_placements = {word_index: letters for word_index, letters in
                                      zip([index for index in range(len(possible_guess)) if
                                           possible_guess[index] in possible_answer and possible_guess[index] ==
                                           possible_answer[index]],
                                          [possible_guess[index] for index in range(len(possible_guess)) if
                                           possible_guess[index] in possible_answer and possible_guess[index] ==
                                           possible_answer[index]])}

                incorrect_words += self.incorrect_words
                known_minimums = self.merge_dictionaries(known_minimums, self.known_minimums)
                known_maximums = self.merge_dictionaries(known_maximums, self.known_maximums)
                incorrect_placements = self.merge_dictionaries(incorrect_placements, self.incorrect_placements)
                correct_placements = self.merge_dictionaries(correct_placements, self.correct_placements)

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
                            if possible_answer_1[incorrect_placement] == incorrect_letter:
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
    def merge_dictionaries(dictionary_one, dictionary_two):
        for key, value in dictionary_two.items():
            if key in dictionary_one:
                if isinstance(dictionary_one[key], list):
                    dictionary_one[key].append(value)
            else:
                dictionary_one[key] = value

        return dictionary_one

    @staticmethod
    def rate_possible_answers(possible_answers):
        if 0 <= len(possible_answers) <= 1:
            return 1

        def similarity(possible_guess, possible_answer):
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
                                         possible_guess[index] != possible_answer[index]],
                                        [[possible_answer[index]] for index in range(len(possible_guess)) if
                                         possible_guess[index] != possible_answer[index]])}
            correct_placements = {word_index: letters for word_index, letters in
                                  zip([index for index in range(len(possible_guess)) if
                                       possible_guess[index] in possible_answer and possible_guess[index] ==
                                       possible_answer[index]],
                                      [possible_guess[index] for index in range(len(possible_guess)) if
                                       possible_guess[index] in possible_answer and possible_guess[index] ==
                                       possible_answer[index]])}

            score = 0
            score += len(known_minimums)
            score += len(known_maximums)
            score += len(correct_placements)

            for incorrect_placement in incorrect_placements.values():
                score += len(incorrect_placement)

            return score / (26 + 26 + (26 * 5) + 5)

        matches = combinations(possible_answers, 2)
        data_frame = DataFrame(list(matches))
        similarities = data_frame.apply(lambda match: similarity(match[0], match[1]), axis=1)

        return similarities.mean()
