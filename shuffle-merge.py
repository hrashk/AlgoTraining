from random import choice, sample, randint, shuffle
from string import ascii_lowercase
from itertools import dropwhile

# s = sample(range(100), k=50)
def datagen():
    s = list(choice(ascii_lowercase) for _ in range(randint(3, 10)))
    rs = s + s
    shuffle(rs)
    return ''.join(rs)

# for _ in range(10):
#     print(datagen())

def solve(s):
    codes = [code(c) for c in s]
    char_stats = count_freqs(codes)
    print(char_stats)
    i = 0
    while True:
        i, letters = next_letters(codes, char_stats, i)
        print(letters, end=' ')
    return letters

def count_freqs(codes):
    char_stats = []
    for _ in range(len(ascii_lowercase)):
        char_stats.append({'freq': 0, 'used': 0, 'skipped': 0})
    for c in codes:
        char_stats[c]['freq'] += 1
    for cs in char_stats:
        cs['freq'] //= 2
    return char_stats

def next_letters(codes, char_stats, i):
    if i > len(codes) - 1:
        raise StopIteration
    elif char_stats[codes[i]]['skipped'] == char_stats[codes[i]]['freq']:
        return i + 1, chr(codes[i] + ord('a'))
    
    prefix_freqs = [0] * len(ascii_lowercase)
    while i < len(codes):
        if char_stats[codes[i]]['used'] == char_stats[codes[i]]['freq']:
            i += 1
        elif char_stats[codes[i]]['skipped'] < char_stats[codes[i]]['freq']:
            char_stats[codes[i]]['skipped'] += 1
            prefix_freqs[codes[i]] += 1
            i += 1
        else:
            break
    min_char = next(c for c, f in enumerate(prefix_freqs) if f != 0)
    # move back
    while codes[i - 1] != min_char:
        i -= 1
        if char_stats[codes[i]]['used'] != char_stats[codes[i]]['freq']:
            char_stats[codes[i]]['skipped'] -= 1
    return i, chr(min_char + ord('a')) * prefix_freqs[min_char]

def code(c):
    return ord(c) - ord('a')

print(solve("tjjvdjxdbbhsjvxtsh"))
