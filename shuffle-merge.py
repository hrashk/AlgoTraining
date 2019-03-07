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
    s = [code(c) for c in s]
    freqs = count_freqs(s)
    i = 0
    while True:
        i, letter = next_letter(s, freqs, i)
        print(letter, end=' ')
    return letter

def count_freqs(s):
    freqs = [0] * len(ascii_lowercase)
    for c in s:
        freqs[c] += 1
    return [f // 2 for f in freqs] # halve the freqs

def next_letter(s, freqs, i):
    if i > len(s) - 1:
        raise StopIteration
    elif freqs[s[i]] == 0:
        return i + 1, chr(s[i] + ord('a'))
    
    prefix_freqs = [0] * len(ascii_lowercase)
    while freqs[s[i]] > 0:
        prefix_freqs[s[i]] += 1
        freqs[s[i]] -= 1
        i += 1
    min_char = next(c for c, f in enumerate(prefix_freqs) if f != 0)
    # move back
    while s[i - 1] != min_char:
        i -= 1
        freqs[s[i]] += 1
    return i, chr(min_char + ord('a')) * prefix_freqs[min_char]

def code(c):
    return ord(c) - ord('a')

print(solve("tjjvdjxdbbhsjvxtsh"))
