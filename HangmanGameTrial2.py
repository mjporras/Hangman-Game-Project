
from Categories import CATEGORIES, CATEGORY_HINTS
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
              |
              |
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
     /|       |
              |
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
     / \      |
              |
    ================
    """
]

# -------------------------------------------
# SELECT CATEGORY + DIFFICULTY
# -------------------------------------------
def choose_category_and_word():
    print("=============================================")
    print("     🎉 Welcome to the Hangman Game! 🎉")
    print("=============================================")
    print("Guess the word before you run out of lives!")
    print()
    
    category_list = list(CATEGORIES.keys())
    
    for i, cat in enumerate(category_list, start=1):
        print(f"{i}. {cat.title()}")

    while True:
        cat_choice = input("\nSelect the Category: ")

        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(category_list):
            chosen_category = category_list[int(cat_choice) - 1]
            break
        else:
            print("Invalid category choice.")

    print("\nSelect difficulty:")
    print("E. Easy")
    print("M. Medium")
    print("H. Hard")

    while True:
        diff_choice = input("Enter difficulty level: ")

        if diff_choice == "E":
            difficulty = "easy"
            break
        elif diff_choice == "M":
            difficulty = "medium"
            break
        elif diff_choice == "H":
            difficulty = "hard"
            break
        else:
            print("Invalid difficulty.")

    word = random.choice(CATEGORIES[chosen_category][difficulty]).lower()
    hint = CATEGORY_HINTS[chosen_category]

    return word, hint


# -------------------------------------------
# Initialize game state
# -------------------------------------------
def initialize_game(word, category_hint):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") 
    lives = 6
    guessed = ["_" if c.isalpha() else c for c in word]

    length_hint = f"The word has {len(word)} characters."
    final_hint = category_hint + " | " + length_hint

    return alphabet, lives, guessed, final_hint


# -------------------------------------------
# Display everything including ASCII
# -------------------------------------------
def display_state(hint, alphabet, lives, guessed):
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
# Process guess
# -------------------------------------------
def process_guess(letter, word, guessed, lives):
    letter = letter.lower()

    if letter in word:
        for i, char in enumerate(word):
            if char == letter:
                guessed[i] = letter
        
        print("Word:", " ".join(guessed))   # show updated word immediately
        print(f"Good job! '{letter}' is in the word.\n")
    
        return guessed, lives, True
    
    else:
        print(f"'{letter}' is NOT in the word.\n")
        lives -= 1
        return guessed, lives, False


# -------------------------------------------
# Check end
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
# MAIN GAME LOOP
# -------------------------------------------
def hangman():
    while True:
        word, category_hint = choose_category_and_word()
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