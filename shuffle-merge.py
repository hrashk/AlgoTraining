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
    code_stats = count_freqs(codes)
    # for letters in next_letters(codes, code_stats):
    #     print(letters, end=' ', flush=True)
    return ' '.join(next_letters(codes, code_stats))

def count_freqs(codes):
    code_stats = []
    for _ in range(len(ascii_lowercase)):
        code_stats.append({'freq': 0, 'used': 0, 'skipped': 0})
    for c in codes:
        code_stats[c]['freq'] += 1
    for cs in code_stats:
        cs['freq'] //= 2
    return code_stats

def next_letters(codes, code_stats):
    i = 0
    while i < len(codes):
        if code_stats[codes[i]]['used'] >= code_stats[codes[i]]['freq']:
            i += 1
            continue
        elif code_stats[codes[i]]['skipped'] >= code_stats[codes[i]]['freq']:
            yield chr(codes[i] + ord('a'))
            code_stats[codes[i]]['used'] += 1
            i += 1
            continue
        skipped_freqs = [0] * len(ascii_lowercase)
        while i < len(codes):
            if code_stats[codes[i]]['used'] >= code_stats[codes[i]]['freq']:
                i += 1
            elif code_stats[codes[i]]['skipped'] < code_stats[codes[i]]['freq']:
                code_stats[codes[i]]['skipped'] += 1
                skipped_freqs[codes[i]] += 1
                i += 1
            else:
                break
        min_code = next(c for c, f in enumerate(skipped_freqs) if f != 0)
        if i < len(codes) and codes[i] < min_code:
            min_code = codes[i]
            code_stats[min_code]['used'] += 1
            i += 1
            yield chr(min_code + ord('a'))
        else:
            code_stats[min_code]['used'] += skipped_freqs[min_code]
            code_stats[min_code]['skipped'] -= skipped_freqs[min_code]
            # move back
            while codes[i - 1] != min_code:
                i -= 1
                code_stats[codes[i]]['skipped'] -= 1
            yield chr(min_code + ord('a')) * skipped_freqs[min_code]

def code(c):
    return ord(c) - ord('a')

print(solve("tjjvdjxdbbhsjvxtsh"))
