import random
from wordlist import WORD_BANK 
#lilian
# Hangman ASCII art for 6 lives (index 0 = no wrong guesses)
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ========
    """
]

# Helper functions
def choose_category(): #Lilian
    categories = list(WORD_BANK.keys())
    print("Choose a category:")
    for idx, cat in enumerate(categories, start=1):
        print(f"  {idx}. {cat.capitalize()}")
    while True:
        choice = input("Enter the number of the category: ").strip()
        print("-"*50)
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= len(categories):
                return categories[i-1]
        print("Invalid input. Please enter a valid number for the category.")

def choose_difficulty(): #Lilian
    levels = ["easy", "medium", "hard"]
    print("Choose difficulty:")
    for idx, lvl in enumerate(levels, start=1):
        print(f"  {idx}. {lvl.capitalize()}")
    while True:
        choice = input("Enter the number of the difficulty: ").strip()
        print("-"*50)
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= 3:
                return levels[i-1]
        print("Invalid input. Please enter 1, 2 or 3.")

def display_alphabet(alphabet_list): #MJ
    rows = []
    per_row = 30
    for start in range(0, 26, per_row):
        rows.append(" ".join(alphabet_list[start:start+per_row]))
    print("\nAvailable letters:")
    for r in rows:
        print("  " + r)

def display_hint(secret_word, revealed_positions): #MJ
    hint = []
    for ch, revealed in zip(secret_word, revealed_positions):
        if ch == " ":
            hint.append(" ")
        elif revealed:
            hint.append(ch)
        else:
            hint.append("_")
    print("\nWord:")
    print("  " + " ".join(hint))
    print(secret_word) #FOR TESTING ONLY. DELETE IT LATER.

def get_single_letter_guess(alphabet_list): #Flor
    while True:
        guess = input("Guess a letter (A-Z): ").strip().upper()
        print("-" * 50)
        if len(guess) != 1:
            print("Please enter exactly one letter.")
            continue
        if not guess.isalpha():
            print("Invalid input. Only letters A-Z are allowed.")
            continue
        idx = ord(guess) - ord('A')
        if alphabet_list[idx] == '_':
            print(f"You already guessed '{guess}'. Choose another letter.")
            continue
        return guess

def play_round(secret_word): #Valentina
    secret_word = secret_word.upper()
    revealed = [False if ch != " " else True for ch in secret_word]
    lives = 6
    wrong_guesses = 0
    alphabet_list = [chr(ord('A') + i) for i in range(26)]

    while True:
        print(HANGMAN_STAGES[wrong_guesses])
        display_alphabet(alphabet_list)
        display_hint(secret_word, revealed)
        print(f"\nLives remaining: {lives}")

        if all(revealed):
            print("=============================================")
            print("🥳 CONGRATULATIONS! You guessed the word!")
            print("The secret word was:", secret_word)
            return True
        
        if lives <= 0:
            print("=============================================")
            print("\n😞 You've run out of lives. Game over.")
            print("The secret word was:", secret_word)
            return False

        guess = get_single_letter_guess(alphabet_list)
        alphabet_list[ord(guess) - ord('A')] = '_'

        if guess in secret_word:
            for i, ch in enumerate(secret_word):
                if ch == guess:
                    revealed[i] = True
            print(f"Good! '{guess}' is in the word.")
        else:
            print(f"Sorry, '{guess}' is NOT in the word.")
            wrong_guesses += 1
            lives -= 1
            if wrong_guesses > 6:
                wrong_guesses = 6

def pick_word(category, difficulty): #MJ
    words = WORD_BANK.get(category, {}).get(difficulty, [])
    if not words:
        return random.choice(["PYTHON", "HANGMAN", "COMPUTER"])
    return random.choice(words)

def ask_play_again(): #Florencia
    while True:
        choice = input("\nDo you want to play again? (Y/N): ").strip().upper()
        if choice in ("Y", "N"):
            return choice == "Y"
        print("Please enter Y or N.")
        print("=============================================") #added

def main(): #Everyone 
    print("=============================================")
    print("     🎉 Welcome to the Hangman Game! 🎉")
    print("=============================================")
    while True:
        category = choose_category()
        difficulty = choose_difficulty()
        secret_word = pick_word(category, difficulty)
        print(f"\nYou picked: Category = {category.capitalize()}, Difficulty = {difficulty.capitalize()}")
        print("Let's start!\n")
        won = play_round(secret_word)
        if won:
            print("\nYou won this round! 🎉")
            print("=============================================") #added
        else:
            print("\nBetter luck next time.")
            print("=============================================") #added

        if not ask_play_again():
            print("\nThank you for playing Hangman. Goodbye!")
            break
        print("-" * 50) #added
        print("\nStarting a new game...\n")

if __name__ == "__main__":
    main()
