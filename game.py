import string
from enum import Enum
from colorama import Fore, Back, Style
from word_bank import WordBank, LetterStatus


GAME_LENGTH = 6


LetterStatusColors = {
    LetterStatus.Correct: Fore.BLACK+Back.GREEN,
    LetterStatus.Elsewhere: Fore.BLACK+Back.YELLOW,
    LetterStatus.Absent: Fore.BLACK+Back.WHITE,
    LetterStatus.Untried: Fore.BLACK+Back.BLUE,
}
GameStatus = Enum('GameStatus', ['Won', 'Lost', 'Progressing'])


class Game:
    """
    Game class for Wordle, an NYT word game: https://www.nytimes.com/games/wordle/index.html
    It holds word bank and data of the game, it does the main game loop,
    processes input and guesses and then scores them

    :word_bank: WordBank instance with words to be used in the game
    """
    def __init__(self, word_bank):
        self._word_bank = word_bank
        self._solution = self._word_bank.get_word()
        self._guesses = []
        self._history = []
        self._matching = None
        self.letters_status = {letter:LetterStatus.Untried
                               for letter in list(string.ascii_lowercase)}
        self.status = GameStatus.Progressing

    def _score_word(self, word):
        """
        Scores a word based on how many letters are matching with the solution.
        Follows this intepretation of letter scores:
        * Correct: letter is correct and in the same position as the original word
        * Elsewhere: letter is correct but is at different position in solution
        * Absent: letter is not present in solution

        :word: word to be scored
        """
        result = []
        for sl, gl in zip(self._solution, word):
            if sl == gl:
                result.append(LetterStatus.Correct)
                continue
            if gl in self._solution:
                result.append(LetterStatus.Elsewhere)
            else:
                result.append(LetterStatus.Absent)
        return result

    def _process_guess(self, guess):
        """
        Method for recording and evaluating guess given by a player and then
        updating the game state.

        :guess: word given by player as a guess
        """
        self._guesses.append(guess)
        self._history.append(self._score_word(guess))
        for letter, score in zip(guess, self._history[-1]):
            self.letters_status[letter] = score

        if guess == self._solution:
            self.status = GameStatus.Won
            print(f'SOLVED in {len(self._guesses)}')
        elif len(self._guesses) >= GAME_LENGTH:
            self.status = GameStatus.Lost
            print(f'LOST ... solution was {self._solution}')

        return self.status

    def _input_guess(self):
        """Loop for prompting player for a guess until it's valid"""
        while True:
            guess = input('>')
            if len(guess) != 5: continue
            for l in guess:
                if l not in string.ascii_lowercase: continue
            if not self._word_bank.verify_word(guess): continue
            break
        return guess

    def _print_history(self):
        """Colorful visual print of prior guesses and their evaluations"""
        for guess, score in zip(self._guesses, self._history):
            for l, s in zip(guess, score):
                print(f'{LetterStatusColors[s]} {l} {Style.RESET_ALL}', end='')
            print('')

    def _update_matching(self):
        """Update of words present in the word bank that can be the solution"""
        matching_new = self._word_bank.words_matching(self._guesses[-1], self._history[-1])
        if self._matching is None: self._matching = matching_new
        else: self._matching = list(set(matching_new).intersection(self._matching))
        print(sorted(self._matching))

    def play(self):
        """Method to call, to complete a playthrough"""
        while self.status == GameStatus.Progressing:
            guess = self._input_guess()
            self._process_guess(guess)
            self._print_history()
            self._update_matching()
        return self.status


if __name__ == '__main__':
    word_bank = WordBank()
    game = Game(word_bank)
    game.play()

    
