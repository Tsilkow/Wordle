from random import choice
import re
from enum import Enum

LetterStatus = Enum('LetterStatus', ['Correct', 'Elsewhere', 'Absent', 'Untried'])


class WordBank:
    """
    Structure for loading, storing and searching through words used in the game

    :filename: filename of file with words that will be loaded
    """
    def __init__(self, filename):
        self._words = []
        with open(filename, 'r') as f:
            for word in f.readlines():
                self._words.append(word.strip('\n').strip('\t'))

    def get_word(self):
        """Returns random word"""
        return choice(self._words)

    @property
    def get_all_words(self):
        return self._words

    def verify_word(self, word):
        """
        For a given word returns whether it's in the WordBank

        :word: word to be verified
        """
        return (word in self._words)

    def words_matching(self, word, letters_status, candidates=None):
        """
        Returns words that are possible solution based on scoring of one, given word

        :word: word used in scoring
        :letters_status: scoring given to the word
        :candidates: words to consider as possible solutions; if None, considers all words; defaults to None
        """
        if candidates is None: candidates = self._words
        result = []
        positive_regexs = []
        negative_regexs = []
        tmp = '.....'
        for i, (l, s) in enumerate(zip(word, letters_status)):
            if s == LetterStatus.Correct:
                positive_regexs.append(tmp[:i] + l + tmp[i+1:])
            elif s == LetterStatus.Elsewhere:
                positive_regexs.append(l)
                negative_regexs.append(tmp[:i] + l + tmp[i+1:])
            elif s == LetterStatus.Absent:
                negative_regexs.append(l)
        
        for w in candidates:
            allowed_word = True
            for r in positive_regexs:
                if not re.search(r, w):
                    allowed_word = False
                    break
            if not allowed_word: continue
            for r in negative_regexs:
                if re.search(r, w):
                    allowed_word = False
                    break
            if not allowed_word: continue
            result.append(w)
        return result
