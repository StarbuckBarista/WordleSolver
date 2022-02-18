from guesses.guess import Guess

"""
Default Values

incorrect_words = []
known_minimums = {}
known_maximums = {}
incorrect_placements = {}
correct_placements = {}
"""

incorrect_words = []
known_minimums = {}
known_maximums = {}
incorrect_placements = {}
correct_placements = {}
scrape_web = True  # Uses words.json if False

if __name__ == "__main__":
    def print_guess(guess):
        print(guess)

    Guess(incorrect_words, known_minimums, known_maximums, incorrect_placements, correct_placements, scrape_web, print_guess)
