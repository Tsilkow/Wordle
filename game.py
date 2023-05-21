import string
import argparse
from copy import copy
from enum import Enum
from tqdm import tqdm
from colorama import Fore, Back, Style
from word_bank import WordBank, LetterStatus
from solver import is_valid, get_human_guess, get_random_guess, get_best_letter_guess


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
            if not is_valid(solution, self._word_bank):
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
            (and not marked correct)
        * Absent: letter is not present in solution

        :word: word to be scored
        """
        result = []
        solution_letters_left = list(self._solution)
        for sletter, gletter in zip(self._solution, word):
            if sletter == gletter:
                result.append(LetterStatus.Correct)
                solution_letters_left.remove(sletter)
                continue
            if gletter in self._solution:
                result.append(LetterStatus.Elsewhere)
            else:
                result.append(LetterStatus.Absent)

        # Handle repeating letters
        if len(set(word)) < len(word):
            for i, letter in enumerate(word):
                if result[i] == LetterStatus.Elsewhere:
                    if letter not in solution_letters_left:
                        result[i] = LetterStatus.Absent
                    else:
                        solution_letters_left.remove(letter)

        return result

    def _process_guess(self, guess):
        """
        Method for recording and evaluating guess given by a player and then
        updating the game state.

        :guess: word given by player as a guess
        """
        score = None
        self._guesses.append(guess)
        self._history.append(self._score_word(guess))
        for letter, score in zip(guess, self._history[-1]):
            self.letters_status[letter] = score

        if guess == self._solution:
            self.status = GameStatus.Won
            score = len(self._guesses)
        elif len(self._guesses) >= GAME_LENGTH:
            self.status = GameStatus.Lost

        return score

    def _print_history(self):
        """Colorful visual print of prior guesses and their evaluations"""
        for guess, score in zip(self._guesses, self._history):
            for l, s in zip(guess, score):
                print(f'{LetterStatusColors[s]} {l} {Style.RESET_ALL}', end='')
            print('')

    def play(self, player, silent=False):
        """Method to call, to complete a playthrough"""
        memory = None
        while self.status == GameStatus.Progressing:
            guess, memory = player(
                self._word_bank, self._guesses, self._history, memory, self._laconic)
            score = self._process_guess(guess)
            if not self._laconic:
                self._print_history()
        if not silent:
            if self.status == GameStatus.Won:
                print(f'SOLVED in {len(self._guesses)}')
            if self.status == GameStatus.Lost:
                print(f'LOST ... solution was {self._solution}')
        return self.status, score


def evaluate_against_words(word_bank, player, player_name):
    games_count = 0
    win_count = 0
    score_total = 0
    for word in tqdm(word_bank.get_all_words):
        game = Game(word_bank, word, True)
        status, score = game.play(player, True)
        if status == GameStatus.Won:
            win_count += 1
            score_total += score
        games_count += 1
    print(f'Player {player_name} has won {win_count} games out of {games_count} ({win_count/games_count*100:.2f}%) with average of {score_total/games_count:.2f} guesses.')
    return win_count, games_count, score_total

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-w', '--wordbank', action='store', nargs='?', type=str, const='words_wordle', default='words_wordle',
        help='filename of used word bank')
    parser.add_argument(
        '-s', '--solution', action='store', type=str,
        help='solution to the puzzle')
    parser.add_argument(
        '-p', '--player', action='store', nargs='?', type=str, const='human', default='human',
        help='player of the puzzle (descriptions in solver.py): \'human\', \'random\', \'best_letter\'')
    parser.add_argument(
        '-l', '--laconic', action='store_true',
        help='flag for supressing printing game status; recommended for bulk solver testing')
    parser.add_argument(
        '-e', '--evaluate', action='store_true',
        help='flag for evaluation of given player on all words from word bank')
    args = parser.parse_args()
    if args.player == 'human': player = get_human_guess
    elif args.player == 'random': player =  get_random_guess
    elif args.player == 'best_letter': player = get_best_letter_guess
    
    word_bank = WordBank(args.wordbank)
    if args.evaluate:
        evaluate_against_words(word_bank, player, args.player)
    else:
        game = Game(word_bank, solution=args.solution, laconic=args.laconic)
        game.play(player)
