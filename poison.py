from random import choice, sample
from itertools import chain


def one_day(arr):
    i = len(arr) - 1
    while i > 0:
        if arr[i] > arr[i-1]:
            del arr[i]
        i -= 1


def poisonousPlants(p):
    if len(p) < 2:
        return 0
    top = -1
    infinity = 10**9 + 7
    p.append(-1)
    stack = [0]
    doomsday = [infinity] * len(p)

    for idx in range(1, len(p)):
        if p[idx] > p[idx - 1]:
            doomsday[idx] = 1
        elif p[idx] == p[idx - 1]:
            doomsday[idx] = infinity if doomsday[idx - 1] == infinity else doomsday[idx - 1] + 1
            stack.pop()
        else:
            maxdays = doomsday[stack[top]]
            while len(stack) > 0 and p[idx] <= p[stack[top]]:
                maxdays = max(maxdays, doomsday[stack[top]])
                stack.pop()
            if maxdays == infinity or len(stack) == 0:
                doomsday[idx] = infinity
            else:  # TODO: turn into binary search!
                r = len(stack) - 1
                while doomsday[stack[r]] <= maxdays:
                    r -= 1
                    assert r >= 0
                doomsday[idx] = (1 + maxdays) if doomsday[stack[r]] < infinity or p[idx] > p[stack[r]] else infinity
        stack.append(idx)
    # print(doomsday)
    return max(filter(lambda x: x != infinity, doomsday), default=0)


def brute_force(s):
    old_L = len(s)
    # print(s)
    one_day(s)
    L = len(s)
    days = 0
    while L < old_L:
        # print(s)
        days += 1
        old_L = L
        one_day(s)
        L = len(s)
    assert all(s[i] > s[i+1] for i in range(0, L - 1))
    return days

for _ in range(1000):
    s = sample(range(100), k=50)
    bf = brute_force(s.copy())
    pp = poisonousPlants(s.copy())
    assert bf == pp, str(bf) + ' brute force days vs ' + str(pp) + ' poisonous days'
