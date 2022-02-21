from guesses.guess import Guess

"""
Default Values

incorrect_words = []
known_minimums = {}
known_maximums = {}
incorrect_placements = {0: [], 1: [], 2: [], 3: [], 4: []}
correct_placements = {}
"""

incorrect_words = []
known_minimums = {}
known_maximums = {}
incorrect_placements = {0: [], 1: [], 2: [], 3: [], 4: []}
correct_placements = {}
scrape_web = True  # Uses words.json if False

if __name__ == "__main__":
    def print_guess(guess):
        print(f"Best Guess: {guess}")

    Guess(incorrect_words, known_minimums, known_maximums, incorrect_placements, correct_placements, scrape_web,
          print_guess)
