import random
import sys


"""
print(f"{GREEN_BG} {letter.upper()} {RESET}", end=" ")
                    secret_word_letters.remove(letter)

                elif letter in secret_word_letters:
                    print(f"{YELLOW_BG} {letter.upper()} {RESET}", end=" ")
                    secret_word_letters.remove(letter)
            else:
                print(f"{GREY_BG} {letter.upper()} {RESET}", end=" ")

        if i == 5:
            print("\n\nYOU'VE WON THE GAME, CONGRATULATIONS!")
            sys.exit()¨

        print(f"{GREEN_BG} {letter.upper()} {RESET}", end=" ")
"""

GREEN_BG = "\033[42m\033[30m"
YELLOW_BG = "\033[43m\033[30m"
GREY_BG = "\033[100m\033[37m"

RESET = "\033[0m"

def file_into_words_list():
    lista = []
    with open("valid-wordle-words.txt", "r") as filetxt:
        row = filetxt.readlines()
    for word in row:
        lista.append(word.strip("\n"))
    
    return lista


class Guess:

    def __init__(self, attempt_word, secret_word):
        self.word = attempt_word
        self.result = self.check_letters(secret_word)


    def check_letters_v2(self, secret_word):
        pass


            
            


    def check_letters(self, secret_word):
        secret_word_letters = []
        for i in secret_word:
            secret_word_letters.append(i)

        green_letters = []
        yellow_letters = []
        grey_letters = []


        for index in range(5):
            if self.word[index] in secret_word:
                if self.word[index] == secret_word[index]:
                    green_letters.append(index)
                    secret_word_letters.remove(self.word[index])

        for index in range(5):
            if self.word[index] in secret_word and index not in green_letters:
                if self.word[index] in secret_word_letters:
                    yellow_letters.append(index)
                    secret_word_letters.remove(self.word[index])
                else:
                    grey_letters.append(index)
            elif self.word[index] not in secret_word:
                grey_letters.append(index)
        
        for index in range(5):
            if index in green_letters:
                print(f"{GREEN_BG} {self.word[index].upper()} {RESET}", end=" ")
            elif index in yellow_letters:
                print(f"{YELLOW_BG} {self.word[index].upper()} {RESET}", end=" ")
            elif index in grey_letters: 
                print(f"{GREY_BG} {self.word[index].upper()} {RESET}", end=" ")
            
        if len(green_letters) == 5:
            print("\n\nYOU'VE WON THE GAME, CONGRATULATIONS!")
            sys.exit()
        



class WordleGame:
    def __init__(self, secret_word, list_of_words):
        self.secret_word = secret_word
        self.guesses = []
        self.list_of_words = list_of_words
        
    def make_guess(self, user_word):
        new_guess = Guess(user_word, self.secret_word)
        self.guesses.append(new_guess)
    
    def main(self):
        print("WELCOME TO TERMINAL WORDLE!\n\n"+
        "Your objective is to guess the secret 5 letter word in 6"+
        " tries or less.\nEach guess must be a valid 5-letter word." +
        "\nTo quit, simply type 'q' and enter.\n\nGOOD LUCK!\n")
        attempts = 0
        while attempts != 6:
            user_word = input().lower()
            if len(user_word) == 5 and user_word.isalpha():
                    if user_word in self.list_of_words:
                        self.make_guess(user_word)
                        attempts += 1
                        print()
                    else:
                        print("\nNot in our dictionary unfortunately\n")


            elif user_word == "q":
                sys.exit()

            else:
                print("\nwrite a 5-letter word\n")
        
        print("\n\nyou've lost unfortunately, the word was "
         + self.secret_word + "\n\n")




if __name__ == "__main__":
    wordlist = file_into_words_list()
    secret_word = random.choice(wordlist)
    wg = WordleGame(secret_word, wordlist)
    wg.main()