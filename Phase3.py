#Stage 1: MJ CODE HERE:
#######################################################
def start_game():
    word = ("pineapple")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lives = 6
    hint = ["_"]*len(word)
    print((f"The word has {len(word)} letters."),hint)

    while True:
        letter = input("Guess a letter").lower()

#FLORENCIA CODE HERE: 
#######################################################



#If letter is already guessed

        if letter not in alphabet:
            print(f"That letter {letter} was already used. Try with another letter.")
            continue

#If letter is in the word

        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    hint[i] = letter
                    print(hint)

#Remove letter from the alphabet

                alphabet = alphabet.replace(letter, "")
                print(alphabet)
                continue

#LILIAN CODE HERE:
#######################################################
#If letter is not in the word



#Check if the word is complete
        if lives !=0 and "_" in hint:
            print(f"You won! The word is: {word}")
            play_again = input("Do you want to play again? (yes/no): ")
            if play_again.lower() =="yes":
                break
            #Go back to phase 1 - start_game()
        else:
            print("Thank you for playing!")
            break

    #Go to phase 2