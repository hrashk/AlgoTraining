import math
import os
import random
import re
import sys
from bisect import bisect_left


def precompute(maxrank):
    # F[n][i] is the # of decibinary representations of n of length 0..i for i > 0
    F = [[1]]  # sentinel
    S = [1]  # S[i] = sum(F[:i+1][-1])
    n = 0  # the number to represent
    while S[-1] < maxrank:
        n += 1
        F.append([0])

        # find the minimum length of the decibinary representation
        i = 1
        pow2 = 2
        while n > 9 * (pow2 - 1):
            F[n].append(0)
            i += 1
            pow2 *= 2
        # recursive step
        while pow2 // 2 <= n:
            F[n].append(0)
            for d in range(1, 10):
                next_number = n - d * pow2 // 2
                if next_number < 0:
                    break
                F[n][i] += F[next_number][i - 1] if i - \
                    1 < len(F[next_number]) else F[next_number][-1]
            F[n][i] += F[n][i - 1]
            i += 1
            pow2 *= 2
        S.append(S[-1] + F[n][-1])
    return F, S


F, S = precompute(10**4)  # todo: repelace with 10**16
# if __debug__:
#     print("The biggest number:", len(F), " Last # stats ", F[-1][-1]," S[-1] =", S[-1])
# for n, c in enumerate(F):
#     print(n, '->', c)


def decibinaryNumbers(x):
    n = bisect_left(S, x)
    i = bisect_left(F[n], x - S[n-1])
    return n


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        q = int(f.readline())

        for q_itr in range(q):
            x = int(f.readline())

            result = decibinaryNumbers(x)

            print(str(result))
