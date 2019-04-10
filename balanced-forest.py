#!/bin/python3

import math
import os
import random
import re
import sys

def build_adj_list(edges):
    graph = [[] for _ in range (len(edges) + 1)]
    for v1, v2 in edges:
        graph[v1-1].append(v2-1)
        graph[v2-1].append(v1-1)
    return graph

def dfs_augment_weight(graph, c, start):
    weights = {}
    parent = {start: start}
    stack = [start]

    while len(stack) > 0:
        top = stack[-1]
        unvisited = [v for v in graph[top] if v not in parent]

        if len(unvisited) > 0:
            stack.extend(unvisited)
            parent.update({v: top for v in unvisited})
        else:
            weights[top] = c[top] + sum(weights[v] for v in graph[top] if v != parent[top])
            stack.pop()

    return weights, parent

def dfs_cut(graph, weights, parent, total):
    candidates1 = []
    candidates2 = []

    for v, dad in parent.items():
        if 3 * weights[v] > total and 2 * weights[v] < total:
            candidates1.append(v)
        if 3 * (total - weights[v]) > total and 2 * (total - weights[v]) < total:
            candidates2.append(v)

    print("candidates1:", candidates1)
    print("candidates2:", candidates2)

    return 0

# Complete the balancedForest function below.
def balancedForest(c, edges):
    graph = build_adj_list(edges)
    print(graph)
    weights, parent = dfs_augment_weight(graph, c, edges[0][0] - 1)
    total = sum(c)
    res = dfs_cut(graph, weights, parent, total)
    return res

if __name__ == '__main__':
    q = int(input())

    for q_itr in range(q):
        n = int(input())

        c = list(map(int, input().rstrip().split()))

        edges = []

        for _ in range(n - 1):
            edges.append(list(map(int, input().rstrip().split())))

        result = balancedForest(c, edges)

        print(result)
