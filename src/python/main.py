from guesses.guess import Guess

"""
Default Values

incorrect_words = []
known_minimums = {}
known_maximums = {}
incorrect_placements = {}
correct_placements = {}
"""

incorrect_words = ["aurei"]
known_minimums = {"i": 1}
known_maximums = {"a": 0, "u": 0, "r": 0, "e": 0}
incorrect_placements = {4: ["i"]}
correct_placements = {}
scrape_web = True  # Uses words.json if False

if __name__ == "__main__":
    def print_guess(guess):
        print(f"Best Guess: {guess}")

    Guess(incorrect_words, known_minimums, known_maximums, incorrect_placements, correct_placements, scrape_web, print_guess)
