import string
from random import choice
from word_bank import WordBank, LetterStatus


best_opener = 'crane'


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
        matching_new = word_bank.words_matching(g, s)
        if matching is None: matching = matching_new
        else: matching = list(set(matching_new).intersection(matching))
    return matching


def random_matching_move(word_bank, guesses, scores, matching=None):
    """
    Strategy of choosing a random feasible word.
    
    :word_bank: instance of WordBank, source of words and matches
    :guesses: words guessed so far
    :scores: letter results previous guesses achieved
    :matching: set of previously feasible words; defaults to None (no previous calculations were done)
    """
    # If this is the first move, return best opener
    if len(guesses) == 0: return best_opener, None
    
    matching = calc_new_matching(word_bank, guesses, scores, matching)
    
    result = choice(matching)
    print('>'+result)
    return result, matching


def best_letter_matching_move(word_bank, guesses, scores, matching=None):
    """
    Strategy of choosing a feasible word with most untried letters.
    
    :word_bank: instance of WordBank, source of words and matches
    :guesses: words guessed so far
    :scores: letter results previous guesses achieved
    :matching: set of previously feasible words; defaults to None (no previous calculations were done)
    """
    # If this is the first move, return best opener
    if len(guesses) == 0: return best_opener, None
    
    matching = calc_new_matching(word_bank, guesses, scores, matching)

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

    print('>'+result)
    return result, matching
