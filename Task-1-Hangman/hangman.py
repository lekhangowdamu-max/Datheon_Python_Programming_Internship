import random

WORD_FILE = "words.txt"
MAX_ATTEMPTS = 6

HANGMAN_PICTURES = [
    """
     +---+
         |
         |
         |
        ===
    """,
    """
     +---+
     O   |
         |
         |
        ===
    """,
    """
     +---+
     O   |
     |   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ===
    """
]


def load_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = [
                line.strip().lower()
                for line in file
                if line.strip().isalpha() and len(line.strip()) >= 3
            ]

        return words

    except FileNotFoundError:
        print("Error: words.txt file not found!")
        print("Keep words.txt in the same folder as hangman.py.")
        return []


def display_game(secret_word, guessed_letters, wrong_guesses):

    print(HANGMAN_PICTURES[wrong_guesses])

    displayed_word = ""

    for letter in secret_word:
        if letter in guessed_letters:
            displayed_word += letter + " "
        else:
            displayed_word += "_ "

    print("Word:", displayed_word)

    print("Guessed letters:", " ".join(sorted(guessed_letters)))

    print("Incorrect guesses left:", MAX_ATTEMPTS - wrong_guesses)


def play_hangman():

    words = load_words(WORD_FILE)

    if not words:
        print("No valid words available.")
        return

    secret_word = random.choice(words)

    guessed_letters = set()

    wrong_guesses = 0

    print("\n========== HANGMAN ==========")
    print("Guess the hidden word one letter at a time.")
    print("You have 6 incorrect guesses.")

    while wrong_guesses < MAX_ATTEMPTS:

        display_game(secret_word, guessed_letters, wrong_guesses)

        if all(letter in guessed_letters for letter in secret_word):
            print("\nYOU WIN!")
            print("Congratulations!")
            print("The word was:", secret_word)
            return

        guess = input("\nEnter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter only one letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter!")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
        else:
            wrong_guesses += 1
            print("Wrong guess!")

    display_game(secret_word, guessed_letters, wrong_guesses)

    print("\nGAME OVER!")
    print("You ran out of attempts.")
    print("The correct word was:", secret_word)


if __name__ == "__main__":
    play_hangman()