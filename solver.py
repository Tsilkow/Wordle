from random import choice


best_opener = 'crane'


def best_move(word_bank, guesses, scores, matching=None):
    # If this is the first move, return best opener
    if len(guesses) == 0: return best_opener, None
    
    for g, s in zip(guesses, scores):
        matching_new = word_bank.words_matching(g, s)
        if matching is None: matching = matching_new
        else: matching = list(set(matching_new).intersection(matching))

    result = choice(matching)
    print('>'+result)
    return result, matching
