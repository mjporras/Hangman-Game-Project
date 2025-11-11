#Check if letter is in the word
word = ("pineapple")
hint = ["_"]*len(word)
print((f"The word has {len(word)} letters."),hint)

letter = input("Guess a letter").lower()

if letter in word:
    for i in range(len(word)):
        if word[i] == letter:
            hint[i] = letter
            print(hint)