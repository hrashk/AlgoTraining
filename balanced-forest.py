#!/bin/python3

import math
import os
import random
import re
import sys

from itertools import combinations
from collections import deque

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
    def dfs_up(v):
        ref_weight = weights[v]

        visited = set((v,))
        stack = []
        dad = v

        while parent[dad] != dad:
            dad = parent[dad]
            if weights[dad] - ref_weight in (ref_weight, total - 2 * ref_weight):
                # print("dfs_up dad:", dad)
                return True
            stack.append(dad)
            visited.add(dad)
        
        while len(stack) > 0:
            top = stack[-1]
            unvisited = [u for u in graph[top] if u not in visited and weights[u] >= total - 2 * ref_weight]

            if len(unvisited) == 0:
                stack.pop()
            else:
                stack.extend(unvisited)
                visited.update(unvisited)
                
                for u in unvisited:
                    if weights[u] in (ref_weight, total - 2 * ref_weight):
                        # print("dfs_up u:", u)
                        return True
        return False
    
    def dfs_down(v):
        ref_weight = total - weights[v]
        visited = set((v,))
        stack = [v]
        while len(stack) > 0:
            top = stack[-1]
            unvisited = [u for u in graph[top] if u not in visited and weights[u] >= total - 2 * ref_weight]

            if len(unvisited) == 0:
                stack.pop()
            else:
                stack.extend(unvisited)
                visited.update(unvisited)
                
                for u in unvisited:
                    if weights[u] in (ref_weight, total - 2 * ref_weight):
                        # print("dfs_down u:", u)
                        return True
        return False

    candidates_up = []
    candidates_down = []

    for v, dad in parent.items():
        if 3 * weights[v] >= total and 2 * weights[v] <= total:
            candidates_up.append(v)
        if 3 * (total - weights[v]) >= total and 2 * (total - weights[v]) <= total:
            candidates_down.append(v)

    # print("weights:", weights)
    # print("candidates_up:", candidates_up)
    # print("candidates_down:", candidates_down)

    min_up = min((3 * weights[v] - total for v in candidates_up if dfs_up(v)), default=-1)
    min_down = min((3 * weights[v] - total for v in candidates_down if dfs_down(v)), default=-1)
    
    if min_up == -1:
        return min_down
    elif min_down == -1:
        return min_up
    else:
        return min(min_up, min_down)

# Complete the balancedForest function below.
def balancedForest(c, edges):
    if len(c) < 3:
        return -1
    graph = build_adj_list(edges)
    weights, parent = dfs_augment_weight(graph, c, edges[0][0] - 1)
    total = sum(c)
    res = dfs_cut(graph, weights, parent, total)
    return res

def gen_tree():
    n = random.randrange(7, 15)
    edges = [(1+i, 1+random.randrange(i)) for i in range(1, n)]
    c = [random.randrange(1, n) for _ in range(n)]
    return c, edges

def delete_edge(graph, e):
    v1, v2 = e
    graph[v1-1].remove(v2-1)
    graph[v2-1].remove(v1-1)

def add_edge(graph, e):
    v1, v2 = e
    graph[v1-1].append(v2-1)
    graph[v2-1].append(v1-1)

def count_weights(graph, c):
    visited = set()
    Q = deque()
    weights = []

    for v in range(len(graph)):
        if v in visited:
            continue
        Q.append(v)
        visited.add(v)
        weight = 0
        while len(Q) > 0:
            top = Q.popleft()
            weight += c[top]
            for u in graph[top]:
                if u not in visited:
                    Q.append(u)
                    visited.add(u)
        weights.append(weight)

    return weights

def brute_force(c, edges):
    if len(c) < 3:
        return -1
    graph = build_adj_list(edges)
    total = sum(c)

    found = []

    for e1, e2 in combinations(edges, 2):
        delete_edge(graph, e1)
        delete_edge(graph, e2)

        w1, w2, w3 = count_weights(graph, c)
        
        if w1 == w2 and 3 * w1 - total >= 0:
            found.append( 3 * w1 - total)
        if w1 == w3 and 3 * w1 - total >= 0:
            found.append(3 * w1 - total)
        if w3 == w2 and 3 * w2 - total >= 0:
            found.append(3 * w2 - total)
        
        add_edge(graph, e1)
        add_edge(graph, e2)
    
    return min(found, default=-1)

if __name__ == '__main__':
    # q = int(input())

    # for q_itr in range(q):
    #     n = int(input())

    #     c = list(map(int, input().rstrip().split()))

    #     edges = []

    #     for _ in range(n - 1):
    #         edges.append(list(map(int, input().rstrip().split())))

    #     result = balancedForest(c, edges)

    #     print(result)

        c = [2, 2, 3, 1, 1, 1, 1, 3, 2, 2]

        edges = [(1+i, 1+i + 1) for i in range(len(c)-1)]
        # random.randrange

        result = balancedForest(c, edges)
        bf = brute_force(c, edges)
        assert result == 3 == bf, (result, bf)

        c = [4, 4, 4]

        edges = [(1,2), (1,3)]
        # random.randrange

        result = balancedForest(c, edges)
        bf = brute_force(c, edges)
        assert result == 0 == bf, (result, bf)

        for _ in range(100):
            c, edges = gen_tree()
            result = balancedForest(c, edges)
            bf = brute_force(c, edges)
            assert result == bf, (result, bf, c, edges)
