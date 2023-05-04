import string
from random import choice
from word_bank import WordBank, LetterStatus


best_opener = 'crane'


def is_valid(word, word_bank):
    """
    Checks if word is valid: 5-letter, all lowercase and in word bank

    :word: word to confirm
    :word_bank: word_bank the word is supposed to be in
    """
    if len(word) != 5: return False
    for l in word:
        if l not in string.ascii_lowercase: return False
    if not word_bank.verify_word(word): return False
    return True


def get_human_guess(word_bank, guesses, scores, memory, laconic=False):
    """Loop for prompting human player for a guess until it's valid"""
    while True:
        guess = input('>')
        if is_valid(guess, word_bank): break
    return guess, memory


def calc_new_matching(word_bank, guesses, scores, matching=None):
    """
    Function for calculating current set of feasible words.
    Prerequiste to any automatic strategies.

    :word_bank: instance of WordBank, source of words and matches
    :guesses: words guessed so far
    :scores: letter results previous guesses achieved
    :matching: set of previously feasible words; defaults to None (no previous calculations were done)
    """
    for g, s in zip(guesses, scores):
        matching = word_bank.words_matching(g, s, matching)
    return matching


def get_random_guess(word_bank, guesses, scores, matching=None, laconic=False):
    """
    Strategy of choosing a random feasible word that matches history.
    Note: if matching is not None, it will be assumed that scores other than the last were already
    taken into account.
    
    :word_bank: instance of WordBank, source of words and matches
    :guesses: words guessed so far
    :scores: letter results previous guesses achieved
    :matching: set of previously feasible words; defaults to None (no previous calculations were done)
    """
    # If this is the first move, return best opener
    if len(guesses) == 0: return best_opener, None

    if matching is None: matching = calc_new_matching(word_bank, guesses, scores, matching)
    else: matching = calc_new_matching(word_bank, guesses[-1:], scores[-1:], matching)
    
    result = choice(matching)
    if not laconic: print('>'+result)
    return result, matching


def get_best_letter_guess(word_bank, guesses, scores, matching=None, laconic=False):
    """
    Strategy of choosing a feasible word with most untried letters that matches history.
    Note: if matching is not None, it will be assumed that scores other than the last were already
    taken into account.
    
    :word_bank: instance of WordBank, source of words and matches
    :guesses: words guessed so far
    :scores: letter results previous guesses achieved
    :matching: set of previously feasible words; defaults to None (no previous calculations were done)
    """
    # If this is the first move, return best opener
    if len(guesses) == 0: return best_opener, None

    if matching is None: matching = calc_new_matching(word_bank, guesses, scores, matching)
    else: matching = calc_new_matching(word_bank, guesses[-1:], scores[-1:], matching)

    letter_scores = {l:LetterStatus.Untried for l in string.ascii_lowercase}
    for guess, score in zip(guesses, scores):
        for l, s in zip(guess, score):
            letter_scores[l] = s

    result = None
    best_new_letters = 0
    for word in matching:
        new_letters = 0
        for l in word:
            if letter_scores[l] is LetterStatus.Untried: new_letters += 1
        if new_letters > best_new_letters:
            result = word
    if result is None: result = choice(matching)

    if not laconic: print('>'+result)
    return result, matching
