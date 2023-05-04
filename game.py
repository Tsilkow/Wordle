import string
import argparse
from enum import Enum
from colorama import Fore, Back, Style
from word_bank import WordBank, LetterStatus
from solver import is_feasible, get_human_guess, get_random_guess, get_best_letter_guess


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
    def __init__(self, word_bank, solution=None, laconic=False):
        self._word_bank = word_bank
        if solution is not None:
            if not is_feasible(solution, self._word_bank):
                print(f'!Warning! Word {solution} is not valid (either '
                      f'because it\'s not 5-letter, not lowercase or not in '
                      f'word bank). Continuing with random word from word bank.')
                self._solution = None
            else:
                self._solution = solution
        if solution is None: self._solution = self._word_bank.get_word()
        self._laconic = laconic
        self._guesses = []
        self._history = []
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

    def _print_history(self):
        """Colorful visual print of prior guesses and their evaluations"""
        for guess, score in zip(self._guesses, self._history):
            for l, s in zip(guess, score):
                print(f'{LetterStatusColors[s]} {l} {Style.RESET_ALL}', end='')
            print('')

    def play(self, player):
        """Method to call, to complete a playthrough"""
        memory = None
        while self.status == GameStatus.Progressing:
            guess, memory = player(
                self._word_bank, self._guesses, self._history, memory, self._laconic)
            self._process_guess(guess)
            if not self._laconic: self._print_history()
        return self.status


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--solution', action='store',
        help='solution to the puzzle')
    parser.add_argument(
        '-p', '--player', action='store',
        help='player of the puzzle (descriptions in solver.py): \'human\', \'random\', \'best_letter\'')
    parser.add_argument(
        '-l', '--laconic', action='store_true',
        help='flag for supressing printing game status; recommended for bulk solver testing')
    args = parser.parse_args()
    if args.player is None: player = get_human_guess
    elif args.player == 'human': player = get_human_guess
    elif args.player == 'random': player =  get_random_guess
    elif args.player == 'best_letter': player = get_best_letter_guess
    
    word_bank = WordBank()
    game = Game(word_bank, solution=args.solution, laconic=args.laconic)
    game.play(player)
