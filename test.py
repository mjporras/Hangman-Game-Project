import random
import string

def load_word(difficulty):
    """
    Loads a single random word from the appropriate text file based on difficulty.
    Handles file not found and empty file errors.
    Assumes words are separated by commas (,) in the file.
    """
    # Standardize input to uppercase immediately
    level_key = difficulty.upper() 
    
    # Determine the filename
    if level_key == "E":      
        filename = "easy_words.txt"
    elif level_key == "M":
        filename = "medium_words.txt"
    else:
        filename = "hard_words.txt"

    try:
        with open(filename, "r") as file:
            # Read all content and split by comma to handle single-line, 
            # comma-separated word lists (Fix for "returning the list" issue)
            content = file.read()
            words = [word.strip() for word in content.split(',') if word.strip()]
        
        # Ensures there are words to choose from
        if not words:
            print(f"Error: {filename} is empty. Returning a fallback word.")
            return "DEFAULT"
            
    except FileNotFoundError:
        print(f"Error: File not found: {filename}. Returning a fallback word.")
        return "DEFAULT"

    # Returns one randomly selected, uppercase word.
    return random.choice(words).upper()

def display_hint(hint):
    """Prints the current state of the word hint (e.g., _ A _ P L E)."""
    print(" ".join(hint))

def display_alphabet(guessed_letters):
    """
    Displays the alphabet A–Z, replacing guessed letters with an underscore (_).
    It uses the list of ALL guessed letters passed to it.
    """
    # Ensure guessed_letters are all uppercase for comparison with string.ascii_uppercase
    guessed_letters_upper = [letter.upper() for letter in guessed_letters]
    
    alphabet_display = []
    for letter in string.ascii_uppercase:
        if letter in guessed_letters_upper:
            alphabet_display.append("_")  # Hide guessed letters
        else:
            alphabet_display.append(letter)
            
    print("\nAvailable Letters: " + " ".join(alphabet_display))
    print("-" * 30)

def display_welcome():
    print("=============================================")
    print("     🎉 Welcome to the Hangman Game! 🎉")
    print("=============================================")
    print("Guess the word before you run out of lives!")
    print()
    
# --- Main Program ---
def main():
    display_welcome()

    valid_levels = {'E', 'M', 'H'}

    while True:
        level = input("Select level of difficulty E(Easy), M(Medium), H(Hard):").strip().upper()
        if level in valid_levels:
            break
        # Display "try again" message for invalid input
        print("🛑 Invalid level choice. Please enter E, M, or H. Try again.")

    word = load_word(level)
    initial_lives = 6
    # Initialize game state variables
    is_running = True
    hint = ["_"] * len(word)
    
    # THIS IS THE CRITICAL FIX: Tracks ALL guesses throughout the game
    guessed_letters = [] 
    
    print("-" * 30)
    print(f"The word has {len(word)} letters. Remaining lives is: {initial_lives}")

    while is_running:
        display_hint(hint)
        display_alphabet(guessed_letters)
        
        # Display the word for testing purposes (remove later)
        print(f"[TEST WORD: {word}]") 
        
        # 1. Get and standardize input
        user_input = input("Enter a letter:").strip().upper()
        
        # 2. Input Validation Block
        
        # Must be exactly one character
        if len(user_input) != 1:
            print("🛑 Invalid input. Please enter **only one** character.")
            continue
            
        # Must be a letter (not a number or special character)
        if not user_input.isalpha():
            print(f"🛑 Invalid input. '{user_input}' is not a letter. Try again.")
            continue
        
        # Input Validation
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
            
        if user_input in guessed_letters:
            print(f"You already guessed the letter '{user_input}'. Try again.")
            continue
            
        # Add the valid new guess to the tracking list
        guessed_letters.append(user_input)
      
        # Check if the guess is correct
        if user_input in word:  
            print(f"Correct! '{user_input}' is in the word.")
            # Update the hint
            for i in range(len(word)):
                if word[i] == user_input:
                    hint[i] = user_input
        else:
            print(f"Incorrect. '{user_input}' is not in the word.")
        
        # Win Condition Check
        if "_" not in hint:
            print("\n" + "="*40)
            print(f"🥳 CONGRATULATIONS! You guessed the word: **{word}**")
            print("="*40)
            is_running = False
        
        # (Optional: You would add a life/guess counter and loss condition here)
        
if __name__ == "__main__":
    main()