"""
Terminal Wordle Clone

This module implements a text-based version of the popular game Wordle,
playable directly inside a command-line interface with ANSI color coding.
"""

import random
import sys

# ANSI Escape Sequences for terminal coloring
GREEN_BG = "\033[42m\033[30m"
YELLOW_BG = "\033[43m\033[30m"
GREY_BG = "\033[100m\033[37m"
RESET = "\033[0m"

def file_into_words_list():
    """
    Reads a text file of valid Wordle words and loads them into a list.

    The file 'valid-wordle-words.txt' should have one word per line.

    Returns:
        list: A list of strings containing all valid 5-letter words.
    """
    word_list = []
    with open("valid-wordle-words.txt", "r") as filetxt:
        row = filetxt.readlines()
    for word in row:
        word_list.append(word.strip("\n"))
    
    return word_list

class Guess:
    """
    Represents a single guess attempt in the Wordle game.

    Attributes:
        word (str): The 5-letter word guessed by the player.
        result (list or None): The evaluation result of the letters.
    """

    def __init__(self, attempt_word, secret_word):
        """
        Initializes a Guess instance and instantly checks it against the secret word.

        Args:
            attempt_word (str): The word guessed by the user.
            secret_word (str): The target word to match against.
        """
        self.word = attempt_word
        self.result = self.check_letters(secret_word)

    def check_letters(self, secret_word):
        """
        Evaluates the letters of the guess against the secret word.

        Applies classic Wordle logic to handle duplicates:
        - Green: Correct letter in the correct position.
        - Yellow: Correct letter in the wrong position.
        - Grey: Letter not present in the remaining secret word pool.

        Prints the color-coded feedback to the console. Exits the game if 
        all 5 letters are green.

        Args:
            secret_word (str): The target word to compare against.
        """
        secret_word_letters = []
        for i in secret_word:
            secret_word_letters.append(i)

        green_letters = []
        yellow_letters = []
        grey_letters = []

        # First pass: check for perfect (green) matches
        for index in range(5):
            if self.word[index] in secret_word:
                if self.word[index] == secret_word[index]:
                    green_letters.append(index)
                    secret_word_letters.remove(self.word[index])

        # Second pass: check for misplaced (yellow) or incorrect (grey) matches
        for index in range(5):
            if self.word[index] in secret_word and index not in green_letters:
                if self.word[index] in secret_word_letters:
                    yellow_letters.append(index)
                    secret_word_letters.remove(self.word[index])
                else:
                    grey_letters.append(index)
            elif self.word[index] not in secret_word:
                grey_letters.append(index)
        
        # Display the formatted output
        for index in range(5):
            if index in green_letters:
                print(f"{GREEN_BG} {self.word[index].upper()} {RESET}", end=" ")
            elif index in yellow_letters:
                print(f"{YELLOW_BG} {self.word[index].upper()} {RESET}", end=" ")
            elif index in grey_letters: 
                print(f"{GREY_BG} {self.word[index].upper()} {RESET}", end=" ")
            
        # Win Condition Check
        if len(green_letters) == 5:
            print("\n\nYOU'VE WON THE GAME, CONGRATULATIONS!")
            sys.exit()


class WordleGame:
    """
    Manages the game state, loop, and user interface for Wordle.

    Attributes:
        secret_word (str): The target word for the current game instance.
        guesses (list): A list tracking previous Guess objects.
        list_of_words (list): Acceptable dictionary words for validation.
    """

    def __init__(self, secret_word, list_of_words):
        """
        Initializes the Wordle game setup.

        Args:
            secret_word (str): The word the user is trying to guess.
            list_of_words (list): List of strings representing valid input words.
        """
        self.secret_word = secret_word
        self.guesses = []
        self.list_of_words = list_of_words
        
    def make_guess(self, user_word):
        """
        Creates a new Guess instance and appends it to the history list.

        Args:
            user_word (str): The validated 5-letter word input by the player.
        """
        new_guess = Guess(user_word, self.secret_word)
        self.guesses.append(new_guess)
    
    def main(self):
        """
        Runs the primary game loop.

        Handles the welcome message, input validation (length, character type,
        dictionary checks), attempt tracking, and the loss condition scenario.
        """
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
