from random import choice, sample, randint, shuffle
from string import ascii_lowercase
from itertools import dropwhile
from itertools import combinations

def solve(s):
    codes = [code(c) for c in s]
    code_stats = count_freqs(codes)
    return ''.join(next_letters(codes, code_stats))

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
        # skip while possible
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

        collected_mins = 0
        if i < len(codes) and codes[i] == min_code: # compare it with the next letter
            while i < len(codes):
                if code_stats[codes[i]]['used'] >= code_stats[codes[i]]['freq']:
                    i += 1
                elif codes[i] == min_code: # skip it
                    collected_mins += 1
                    code_stats[min_code]['used'] += 1
                    i += 1
                elif codes[i] < min_code:
                    break
                elif code_stats[codes[i]]['skipped'] < code_stats[codes[i]]['freq']:
                    code_stats[codes[i]]['skipped'] += 1
                    i += 1
                else:
                    break
        if i < len(codes) and codes[i] < min_code:
            yield chr(min_code + ord('a')) * collected_mins
            continue
        # elif i >= len(codes) or codes[i] > min_code:
        else:
            delta = min(skipped_freqs[min_code],  code_stats[min_code]['freq'] - code_stats[min_code]['used'])
            yield chr(min_code + ord('a')) * (collected_mins + delta)
            # backtrack
            while codes[i - 1] != min_code or skipped_freqs[min_code] > delta:
                assert i > 0
                i -= 1
                if code_stats[codes[i]]['used'] >= code_stats[codes[i]]['freq']:
                    continue
                assert code_stats[codes[i]]['skipped'] > 0
                code_stats[codes[i]]['skipped'] -= 1
                assert skipped_freqs[codes[i]] > 0
                skipped_freqs[codes[i]] -= 1
            code_stats[min_code]['used'] += delta

def code(c):
    return ord(c) - ord('a')


def datagen():
    A = ''.join(choice(ascii_lowercase) for _ in range(randint(3, 10)))
    res = sample(A + A, 2 * len(A))
    return ''.join(res)

def gather_freqs(s):
    freqs = {l: 0 for l in ascii_lowercase}
    for l in s:
        freqs[l] += 1
    return freqs


def combos(s):
    freqs = gather_freqs(s)
    for c in combinations(s, len(s) // 2):
        c_freqs = gather_freqs(c)
        if all(freqs[l] == 2 * c_freqs[l] for l in ascii_lowercase):
            yield c

def testem():
    collector = []
    for _ in range(100):
        s = datagen()
        s1 = solve(s)
        ans = min(''.join(c) for c in combos(s))
        if s1 != ans:
            collector.append(s + ' => ' + ans + ' not ' + s1)
    print(collector)

# testem()
print(solve("mghyyvvgwjgnghwnvjvm")) # must be llnoyyu
