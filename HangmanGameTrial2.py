

import os
import time
import random

# -------------------------------------------
# ASCII Hangman graphics
# -------------------------------------------
HANGMAN_PICS = [
    r"""
      +-------+
      |       |
      O       |
     /|\      |
     / \      |
              |
    ================
    """,
    r"""
      +-------+
      |       |
      O       |
     /|\      |
     /        |
              |
    ================
    """,
    r"""
      +-------+
      |       |
      O       |
     /|\      |
              |
              |
    ================
    """,
    r"""
      +-------+
      |       |
      O       |
     /|       |
              |
              |
    ================
    """,
    r"""
      +-------+
      |       |
      O       |
      |       |
              |
              |
    ================
    """,
    r"""
      +-------+
      |       |
      O       |
              |
              |
              |
    ================
    """,
    r"""
      +-------+
      |       |
              |
              |
              |
              |
    ================
    """
]

# -------------------------------------------
# Word lists by difficulty + categories
# -------------------------------------------
EASY_WORDS = [
    "Apple", "Banana", "Orange", "Pear", "Peach", "Grapes", "Mango", "Kiwi",
    "Pineapple", "Watermelon", "Blueberry", "Strawberry", "Raspberry",
    "Cherry", "Lemon", "Lime"
]

MEDIUM_WORDS = [
    "Papaya", "Dragonfruit", "Lychee", "Persimmon", "Starfruit",
    "Passionfruit", "Guava", "Fig", "Pomegranate", "Tamarind", "Durian",
    "Longan", "Jackfruit"
]

HARD_WORDS = [
    "Boysenberry", "Clementine", "Huckleberry", "Elderberry", "Mulberry",
    "Gooseberry", "Ugli fruit", "Feijoa", "Satsuma", "Jabuticaba"
]

CATEGORY_HINTS = {
    "easy": "Category: Common fruits you see in everyday life.",
    "medium": "Category: Exotic or tropical fruits!",
    "hard": "Category: Rare, unusual, or hard-to-spell fruits!"
}

# -------------------------------------------
# Select difficulty + choose word + hint
# -------------------------------------------
def choose_difficulty():
    print("Welcome to Hangman!")
    print("Select difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            return random.choice(EASY_WORDS).lower(), CATEGORY_HINTS["easy"]
        elif choice == "2":
            return random.choice(MEDIUM_WORDS).lower(), CATEGORY_HINTS["medium"]
        elif choice == "3":
            return random.choice(HARD_WORDS).lower(), CATEGORY_HINTS["hard"]
        else:
            print("Invalid input.")


# -------------------------------------------
# Initialize game state
# -------------------------------------------
def initialize_game(word, category_hint):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    lives = 6
    guessed = ["_" for _ in word]
    
    if " " in word:
        guessed = ["_" if c.isalpha() else c for c in word]

    length_hint = f"The word has {len(word)} characters."
    final_hint = category_hint + " | " + length_hint

    return alphabet, lives, guessed, final_hint


# -------------------------------------------
# Display everything including ASCII art
# -------------------------------------------
def display_state(hint, alphabet, lives, guessed):
     # Clear screen so ASCII hangman stays in the same place
    os.system("cls" if os.name == "nt" else "clear")
    print(HANGMAN_PICS[6-lives])
    print(hint)
    print("Alphabet:", " ".join(alphabet))
    print("Lives:", lives)
    print("Word:", " ".join(guessed))
    print("------------------------\n")


# -------------------------------------------
# Input validation
# -------------------------------------------
def validate_input(letter):
    return len(letter) == 1 and letter.isalpha()


# -------------------------------------------
# Check guess
# -------------------------------------------
def process_guess(letter, word, guessed, lives):
    letter = letter.lower()

    if letter in word:
        print(f"Good job! '{letter}' is in the word.\n")
        for i, char in enumerate(word):
            if char == letter:
                guessed[i] = letter
        return guessed, lives, True
    else:
        print(f"'{letter}' is NOT in the word.\n")
        lives -= 1
        return guessed, lives, False


# -------------------------------------------
# Check end-game
# -------------------------------------------
def check_game_end(guessed, lives, word):
    if "_" not in guessed:
        print("You won! 🎉")
        return True
    if lives == 0:
        print(HANGMAN_PICS[0])
        print(f"You lose! The word was '{word}'.")
        return True
    return False


# -------------------------------------------
# Play again?
# -------------------------------------------
def play_again():
    return input("Play again? (y/n): ").lower() == "y"


# -------------------------------------------
# MAIN GAME
# -------------------------------------------
def hangman():
    while True:
        word, category_hint = choose_difficulty()
        alphabet, lives, guessed, hint = initialize_game(word, category_hint)

        while True:
            display_state(hint, alphabet, lives, guessed)

            letter = input("Enter a letter: ").lower()

            if not validate_input(letter):
                print("Invalid input.\n")
                continue

            if letter.upper() in alphabet:
                alphabet.remove(letter.upper())

            guessed, lives, correct = process_guess(letter, word, guessed, lives)

            if check_game_end(guessed, lives, word):
                break

        if not play_again():
            print("Thank you for playing!")
            break

# Run the game
hangman()