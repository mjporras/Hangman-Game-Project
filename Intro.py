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
        # Display "try again" message for invalid input
        level = input("Select level of difficulty E(Easy), M(Medium), H(Hard):").strip().upper()
        if level in valid_levels:
            break
        print("🛑 Invalid level choice. Please enter E, M, or H. Try again. \n")
        
    word = load_word(level)

    # Initialize game state variables
    initial_lives = 6
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
        
        # Start of Phase 2
        # 1. Get and standardize user input here 
        while True:
            letter = input("Guess a letter: ").strip().upper()

            # 2. Input Validation Block
        
            # Must be exactly one character
            
        
            # Must be a letter (not a number or special character)
        
        
            #if valid input proceed here
        

            # End of Phase 2

            if letter in guessed_letters:
                print(f"That letter {letter} was already used. Try with another one.")
                continue

            guessed_letters.append(letter)

            #If letter is in the word

            if letter in word:
                for i in range(len(word)):
                    if word[i] == letter:
                        hint[i] = letter
                print("Good guess! \n")
                # Check if the word is complete after updating the hint
                if "_" not in hint:
                    print(f"You won! The word is: {word}")
                    play_again = input("Do you want to play again? (yes/no): ")
                    if play_again.lower() == "yes":
                        # Reset game for a new round (but not the whole game)
                        word = load_word(level)
                        initial_lives = 6
                        hint = ["_"] * len(word)
                        guessed_letters.clear()
                        print("-" * 30)
                        print(f"The word has {len(word)} letters. Remaining lives is: {initial_lives}")
                        break  # exit input loop to restart the round display
                    else:
                        print("Thank you for playing! \n")
                        is_running = False
                        break
                # Since it was a correct guess, continue to next guess
                continue

            # Wrong guess case
            initial_lives -= 1
            print(f"Wrong guess! Remaining lives: {initial_lives} \n")
            if initial_lives == 0:
                print(f"Game Over! The word was: {word}")
                play_again = input("Do you want to play again? (yes/no): ")
                if play_again.lower() == "yes":
                    # Reset game for a new round (but not the whole game)
                    word = load_word(level)
                    initial_lives = 6
                    hint = ["_"] * len(word)
                    guessed_letters.clear()
                    print("-" * 30)
                    print(f"The word has {len(word)} letters. Remaining lives is: {initial_lives}")
                    break  # exit input loop to restart the round display
                else:
                    print("Thank you for playing! \n")
                    is_running = False
                    break

if __name__ == "__main__":
    main()