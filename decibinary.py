import math
import os
import random
import re
import sys
from bisect import bisect_left

def precompute(maxrank):
    # F[n][i] is the # of decibinary representations of n of length i for i > 0
    F = [[1] * 20] # sentinel
    S = [1] # S[i] = sum(F[:i+1])
    n = 0 # the number to represent
    while S[-1] < maxrank:
        n += 1
        F.append([0] * 20)

        # find the minimum length of the decibinary representation
        i = 1
        pow2 = 2
        while n > 9 * (pow2 - 1):
            i += 1
            pow2 *= 2
        # recursive step
        while pow2 // 2 <= n:
            for d in range(1, 10):
                next_number = n - d * pow2 // 2
                if next_number >= 0:
                    F[n][i] += F[next_number][i-1]
            i += 1
            pow2 *= 2
        S.append(S[-1] + sum(F[n]))

    # F[n][0] is the total # of decibinary representations of n
    # for n in range(len(F)):
    #     F[n][0] = sum(F[n][1:])
    return F, S

F, S = precompute(10**2) # todo: repelace with 10**16
from pprint import pprint
pprint(F)
pprint(S)

def decibinaryNumbers(x):
    n = bisect_left(S, x)
    return n

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        q = int(f.readline())

        for q_itr in range(q):
            x = int(f.readline())

            result = decibinaryNumbers(x)

            print(str(result))

