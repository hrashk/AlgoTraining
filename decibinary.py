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
        L = 1
        pow2 = 2
        while n > 9 * (pow2 - 1):
            F[n].append(0)
            L += 1
            pow2 *= 2
        # recursive step
        while pow2 // 2 <= n:
            F[n].append(0)
            for d in range(1, 10):
                next_number = n - d * pow2 // 2
                if next_number < 0:
                    break
                F[n][L] += getF(F, next_number, L)
            F[n][L] += F[n][L - 1]
            L += 1
            pow2 *= 2
        S.append(S[-1] + F[n][-1])
    return F, S

def getF(F, n, L):
    return F[n][L - 1] if L - 1 < len(F[n]) else F[n][-1]


F, S = precompute(10**4)  # todo: repelace with 10**16
if __debug__:
    #     print("The biggest number:", len(F), " Last # stats ", F[-1][-1]," S[-1] =", S[-1])
    for n in range(12):
        print(n, '->', S[n], '->', F[n])


def decibinaryNumbers(x):
    res = 0

    n = bisect_left(S, x)
    if n == 0:
        return 0
    rank = x - S[n-1] # rank in the representations of n
    L = bisect_left(F[n], rank)
    rank -= getF(F, n, L) # rank in the representations of length L
    while L > 1:
        for d in range(1, 10):
            next_number = n - d * 2**(L-1)
            nreps = getF(F, next_number, L)
            if rank <= nreps:
                res += d * 10**(L-1)
                n = next_number
                break
            else:
                rank -= nreps
        L = bisect_left(F[n], rank)
        rank -= getF(F, n, L)
    res += n
    return res


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        q = int(f.readline())

        for q_itr in range(q):
            x = int(f.readline())

            result = decibinaryNumbers(x)

            print(str(result))
