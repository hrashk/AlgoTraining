#!/bin/python3

import math
import os
import random
import re
import sys


def find(friend, parent):
    while parent[friend] is not None:
        friend = parent[friend]
    return friend

def union(friend1, friend2, parent, size):
    head1 = find(friend1, parent)
    head2 = find(friend2, parent)

    if size[head1] < size[head2]:
        parent[head1] = head2
        size[head2] += size[head1]
    else:
        parent[head2] = head1
        size[head1] += size[head2]

def minTime(roads, machines):
    parent = {i: None for i in range(len(roads) + 1)}
    cost = 0

    for friend1, friend2, time in sorted(roads, key=lambda r: r[2], reverse=True):
        if not union(friend1, friend2, parent, machines):
            cost += time
    assert machines == set(c for c, p in parent.items() if p is None), (parent, roads, machines)
    return cost

# Complete the maxCircle function below.
def maxCircle(queries):
    return [0]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    ans = maxCircle(queries)

    fptr.write('\n'.join(map(str, ans)))
    fptr.write('\n')

    fptr.close()
