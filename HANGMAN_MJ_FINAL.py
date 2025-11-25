import random
from wordlist import WORD_BANK 

#Lilian
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
        choice = input("\nEnter the number of the category: ").strip()
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
        choice = input("\nEnter the number of the difficulty: ").strip()
        print("-"*50)
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= 3:
                return levels[i-1]
        print("Invalid input. Please enter 1, 2 or 3.")

def display_alphabet(alphabet_list): #MJ
    print("\nAvailable letters:")
    print("  " + " ".join(alphabet_list))

def display_word(secret_word, revealed_positions): #MJ
    word_state = [] #holds the current condition of the word (letters + underscores: guessed/revealed or not)
    for ch, revealed in zip(secret_word, revealed_positions):
        if ch == " ":
            word_state.append(" ")
        elif revealed:
            word_state.append(ch)
        else:
            word_state.append("_")
    print("\nWord:")
    print("  " + " ".join(word_state))
    print(secret_word) #FOR TESTING ONLY. DELETE IT LATER.

def load_scores():
    """Load player scores from scores.txt and return them as a dictionary."""
    scores = {}
    try:
        with open("scores.txt", "r") as file:
            for line in file:
                if ":" in line:
                    name, value = line.strip().split(":")
                    scores[name.strip()] = int(value.strip())
    except FileNotFoundError:
        pass
    return scores

def save_scores(scores):
    """Save player scores to scores.txt."""
    with open("scores.txt", "w") as file:
        for name, points in scores.items():
            file.write(f"{name}: {points}\n")

def display_high_scores(scores):
    print("\n================ HIGH SCORES ================")
    if not scores:
        print("No scores saved yet.")
        return

    # Sort from highest to lowest
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for rank, (name, score) in enumerate(sorted_scores[:10], start=1):
        print(f"{rank}. {name} — {score} pts")
    print("=============================================")

def reset_scores():
    with open("scores.txt", "w") as file:
        pass
    print("\nAll scores have been reset!\n")

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

def play_round(secret_word): #Val
    secret_word = secret_word.upper()
    revealed = [False if ch != " " else True for ch in secret_word]
    lives = 6
    wrong_guesses = 0
    alphabet_list = [chr(ord('A') + i) for i in range(26)]

    score = 0
    hint_used = False

    def give_hint():
        nonlocal score
        hidden_positions = [i for i, shown in enumerate(revealed) if not shown]
        if not hidden_positions:
            print("No hints available, all letters already revealed.")
            return

        reveal_index = random.choice(hidden_positions)
        revealed[reveal_index] = True

        penalty = 20
        score -= penalty
        print(f"\n💡 Hint used! A letter has been revealed. (-{penalty} points)\n")

    while True:
        print(HANGMAN_STAGES[wrong_guesses])
        display_alphabet(alphabet_list)
        display_word(secret_word, revealed) #changed hint to word
        print(f"\nLives remaining: {lives}")
        print(f"Current Score: {score}")

        if all(revealed):
            print("=============================================")
            print("🥳 CONGRATULATIONS! You guessed the word!")
            print("The secret word was:", secret_word)
            score += 50
            return True, score
        
        if lives <= 0:
            print("=============================================")
            print("\n😞 You've run out of lives. Game over.")
            print("The secret word was:", secret_word)
            return False, score

        guess = get_single_letter_guess(alphabet_list)
        alphabet_list[ord(guess) - ord('A')] = '_'

        if guess in secret_word:
            for i, ch in enumerate(secret_word):
                if ch == guess:
                    revealed[i] = True
            print(f"Good! '{guess}' is in the word.")
            score += 10
        else:
            print(f"Sorry, '{guess}' is NOT in the word.")
            wrong_guesses += 1
            lives -= 1
            score -= 5
            if wrong_guesses > 6:
                wrong_guesses = 6
        
            if lives == 2 and not hint_used:
                print("=============================================")
                want_hint = input("You're low on lives. \nDo you want a hint (-20 points)? (Y/N): \n").strip().upper()
                print("=============================================")
                if want_hint == "Y":
                    give_hint()
                    hint_used = True

def pick_word(category, difficulty): #MJ
    words = WORD_BANK.get(category, {}).get(difficulty, [])
    if not words:
        print(f"⚠️  No words available for category '{category}' and difficulty '{difficulty}'. Using a default word instead.")
        return random.choice(["PYTHON", "HANGMAN", "COMPUTER"])
    return random.choice(words)

def ask_play_again(): #Flor
    while True:
        choice = input("\nDo you want to play again? (Y/N): ").strip().upper()
        if choice in ("Y", "N"):
            return choice == "Y"
        print("Please enter Y or N.")
        print("=============================================")

def show_game_rules(): #
    print("\n================ GAME RULES ================")
    print("1. Choose a category and difficulty.")
    print("2. Guess one letter at a time.")
    print("3. Each wrong guess removes one life.")
    print("4. You have 6 lives total.")
    print("5. Points system:")
    print("   - Correct letter: +10 points")
    print("   - Incorrect letter guessed: -5 points")
    print("   - Word guessed correctly: +50 points")
    print("   - Using a hint: -20 points")
    print("6. Hints:")
    print("   - You can use a hint only when you have 2 lives remaining.")
    print("   - The hint will reveal a random hidden letter.")
    print("7. The game ends when you:")
    print("   - Guess the full word (You win!)")
    print("   - Lose all lives (Game over)")
    print("=============================================\n")

def start_menu(): #MJ
    print("=============================================")
    print("     🎉 Welcome to the Hangman Game! 🎉")
    print("=============================================")
    print("1. View Game Rules")
    print("2. Play the Game")
    print("3. View High Scores")
    print("4. Reset Scores")
    print("5. Exit")
    while True:
        choice = input("\nEnter your choice (1/2/3/4/5): ").strip()
        print("-" * 50)
        if choice == "1":
            show_game_rules()
            return start_menu()  # Return to menu after showing rules
        elif choice == "2":
            print("\nStarting game...\n")
            return True
        elif choice == "3":
            scores = load_scores()
            display_high_scores(scores)
            return start_menu()
        elif choice == "4":
            reset_scores()
            return start_menu()
        elif choice == "5":
            print("\nThank you for visiting Hangman. Goodbye!")
            return False
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

def main(): #Everyone
    proceed = start_menu()
    if not proceed:
        return  # Exit the program if player chose 3
    scores = load_scores()

    player_name = input("Enter your name: ").strip()
    if player_name not in scores:
        scores[player_name] = 0  # First time player
    print(f"\nWelcome, {player_name}! Your current total score is {scores[player_name]}.\n")

    while True:
        category = choose_category()
        difficulty = choose_difficulty()
        secret_word = pick_word(category, difficulty)
        print(f"\nYou picked: Category = {category.capitalize()}, Difficulty = {difficulty.capitalize()}")
        print("Let's start!\n")
        won, round_score = play_round(secret_word)
        if won:
            print("\nYou won this round! 🎉")
            print("=============================================")
        else:
            print("\nBetter luck next time.")
            print("=============================================")

        print(f"Score for this round: {round_score}")

        scores[player_name] += round_score
        print(f"Your total score is now: {scores[player_name]}")
        save_scores(scores)
        print("=============================================")

        if not ask_play_again():
            print("\nThank you for playing Hangman. Goodbye!")
            break
        print("-" * 50)
        print("\nStarting a new game...\n")

if __name__ == "__main__":
    main()
