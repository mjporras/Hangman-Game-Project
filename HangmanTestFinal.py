
import os
import random
import string

# Import categories from external file (create categories.py with the CATEGORIES dict)
from categories import CATEGORIES, CATEGORY_HINTS

# Toggle this to True while testing to see the chosen word
SHOW_TEST_WORD = False

# -------------------------------------------
# ASCII Hangman graphics (your provided art)
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
# Utility functions
# -------------------------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_welcome():
    clear_screen()
    print("=============================================")
    print("     🎉 Welcome to the Hangman Game! 🎉")
    print("=============================================")
    print("Guess the word before you run out of lives!")
    print()

# -------------------------------------------
# Category / difficulty selection
# -------------------------------------------
def choose_category_and_difficulty():
    """
    Lets the user pick a category (fruits, animals, etc.) and a difficulty (easy/medium/hard).
    Returns the chosen word (uppercased) and the hint string.
    """
    categories = list(CATEGORIES.keys())

    print("Choose a category:")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat.title()}")

    while True:
        cat_choice = input("Enter category number: ").strip()
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            chosen_category = categories[int(cat_choice) - 1]
            break
        print("Invalid category choice. Try again.")

    print("\nChoose difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    diff_map = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        diff_choice = input("Enter difficulty number: ").strip()
        if diff_choice in diff_map:
            difficulty = diff_map[diff_choice]
            break
        print("Invalid difficulty choice. Try again.")

    # choose a random word from the selected category+difficulty
    word_list = CATEGORIES.get(chosen_category, {}).get(difficulty, [])
    if not word_list:
        # fallback: choose any word from category across difficulties
        combined = []
        for lvl in ("easy", "medium", "hard"):
            combined.extend(CATEGORIES.get(chosen_category, {}).get(lvl, []))
        word_list = combined or ["DEFAULT"]

    chosen_word = random.choice(word_list)

    # Keep original casing for display/hints but use uppercase internally
    hint = CATEGORY_HINTS.get(chosen_category, f"Category: {chosen_category.title()}")

    return chosen_word.upper(), hint

# -------------------------------------------
# Display helpers
# -------------------------------------------
def display_state(hint_text, guessed_letters, lives, guessed_word_display):
    """
    Show the hangman art, hint, alphabet, lives, and the current guessed word display.
    guessed_word_display is a list of characters (with '_' and actual letters/spaces).
    """
    clear_screen()
    # show appropriate hangman art (index based on lives)
    pic_index = max(0, min(len(HANGMAN_PICS) - 1, len(HANGMAN_PICS) - 1 - (6 - lives)))
    # simpler: hangman stage = 6 - lives (0..6) -> index that from end:
    stage = 6 - lives
    if 0 <= stage < len(HANGMAN_PICS):
        print(HANGMAN_PICS[stage])
    else:
        print(HANGMAN_PICS[-1])

    print(hint_text)
    # display alphabet with guessed letters replaced by underscores
    alphabet_display = []
    guessed_up = {g.upper() for g in guessed_letters}
    for ch in string.ascii_uppercase:
        alphabet_display.append("_" if ch in guessed_up else ch)
    print("Available Letters:", " ".join(alphabet_display))
    print("Lives:", lives)
    print("Word:", " ".join(guessed_word_display))
    print("-" * 30)

def display_hint_list(hint_list):
    print(" ".join(hint_list))

# -------------------------------------------
# Game logic helpers
# -------------------------------------------
def initialize_guessed_display(word):
    """
    Return a list for display where letters are '_' and non-letters (spaces, punctuation)
    are shown as-is (e.g., spaces).
    """
    display = []
    for ch in word:
        if ch.isalpha():
            display.append("_")
        else:
            display.append(ch)  # preserve spaces/punctuation
    return display

def process_guess(letter, word, guessed_display, lives):
    """
    Process a single guessed letter.
    Returns (guessed_display, new_lives, result_flag)
      result_flag: True if correct, False if incorrect, None if already guessed
    """
    letter = letter.upper()
    word_upper = word.upper()

    # already guessed?
    if letter in guessed_display or letter == "":
        # letter is already revealed somewhere OR input empty
        return guessed_display, lives, None

    if letter in word_upper:
        # update ALL positions
        for i, ch in enumerate(word_upper):
            if ch == letter:
                guessed_display[i] = letter
        return guessed_display, lives, True
    else:
        return guessed_display, lives - 1, False

def is_game_won(guessed_display):
    return "_" not in guessed_display

# -------------------------------------------
# Input validation
# -------------------------------------------
def get_valid_letter(already_guessed):
    """
    Prompt user until they provide a single alphabetical character that hasn't been guessed.
    Returns the uppercase letter.
    """
    while True:
        letter = input("Enter a letter: ").strip()
        if len(letter) != 1:
            print("Please enter exactly one character.")
            continue
        if not letter.isalpha():
            print("Please enter a letter (A-Z).")
            continue
        letter = letter.upper()
        if letter in already_guessed:
            print(f"You already guessed '{letter}'. Try another letter.")
            continue
        return letter

# -------------------------------------------
# Main game loop
# -------------------------------------------
def main():
    display_welcome()

    while True:
        word, category_hint = choose_category_and_difficulty()
        # Prepare display/hint
        guessed_display = initialize_guessed_display(word)
        lives = 6
        guessed_letters = []  # letters the player has guessed (uppercase)

        length_hint = f"The word has {len([c for c in word if c.isalpha()])} letters (ignoring spaces/punct)."
        final_hint = f"{category_hint} | {length_hint}"

        # Game loop for this word
        while True:
            display_state(final_hint, guessed_letters, lives, guessed_display)
            if SHOW_TEST_WORD:
                print(f"[TEST WORD: {word}]")

            # check for win/lose before asking
            if is_game_won(guessed_display):
                print("You won! 🎉")
                break
            if lives <= 0:
                print(HANGMAN_PICS[0])
                print(f"You lose! The word was: {word}")
                break

            # get input
            letter = get_valid_letter(guessed_letters)
            guessed_letters.append(letter)

            guessed_display, lives, result = process_guess(letter, word, guessed_display, lives)
            if result is True:
                print(f"Good job! '{letter}' is in the word.\n")
            elif result is False:
                print(f"Sorry, '{letter}' is NOT in the word.\n")
            else:
                # already guessed or no-op
                print(f"No change for '{letter}'.\n")

        # play again?
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! Goodbye.")
            break
        # otherwise loop continues and player can pick new category/difficulty

if __name__ == "__main__":
    main()