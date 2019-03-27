#!/bin/python3

import math
import os
import random
import re
import sys

def collect_word_sites(crossword):
    res = []
    n = len(crossword)
    m = len(crossword[0])
    for i in range(n):
        for j in range(m):
            if crossword[i][j] == '-' and (j == 0 or crossword[i][j-1] in ('+', 'X')):
                res.append((i,j,'H')) # horizontal place
            if crossword[i][j] == '-' and (i == 0 or crossword[i-1][j] in ('+', 'X')):
                res.append((i,j,'V')) # vertical place
    return res

def fit_word(crossword, word, site):
    i, j, D = site
    c = 0
    isOk = lambda: c < len(word) and i < len(crossword) and j < len(crossword[0]) and (crossword[i][j] == '-' or crossword[i][j] == word[c])
    dashes_changed = []
    if D == 'H':
        while isOk():
            if crossword[i][j] == '-':
                dashes_changed.append((i, j))
            crossword[i][j] = word[c]
            j += 1
            c += 1
    else:
        assert D == 'V', D
        while isOk():
            if crossword[i][j] == '-':
                dashes_changed.append((i, j))
            crossword[i][j] = word[c]
            i += 1
            c += 1
    return c == len(word) and len(dashes_changed) > 0 and (i >= len(crossword) or j >= len(crossword[0]) or crossword[i][j] in ('+', 'X')), dashes_changed

def unfit_word(crossword, dashes_changed):
    for i, j in dashes_changed:
        crossword[i][j] = '-'

def dfs(crossword, words, word_idx, sites):
    if word_idx >= len(words):
        return crossword
    for s in sites:
        fits, dashes_changed = fit_word(crossword, words[word_idx], s)
        if fits:
            # for s in crossword:
            #     print(''.join(s))
            success = dfs(crossword, words, word_idx + 1, sites)
            if success is not None:
                return success
        unfit_word(crossword, dashes_changed)
    return None



# Complete the crosswordPuzzle function below.
def crosswordPuzzle(crossword, words):
    cross = list(list(s) for s in crossword)
    sites = collect_word_sites(crossword)
    res = dfs(cross, words, 0, sites)
    return [''.join(s) for s in res]

if __name__ == '__main__':
    crossword_text = \
"""
+-++++++++
+-++++++++
+-------++
+-++++++++
+-++++++++
+------+++
+-+++-++++
+++++-++++
+++++-++++
++++++++++
"""

    crossword = crossword_text.strip().split()

    words = "AGRA;NORWAY;ENGLAND;GWALIOR".strip().split(";")

    result = crosswordPuzzle(crossword, words)

    print('\n'.join(result))
