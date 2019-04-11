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
    def dfs_up(v):
        ref_weight = weights[v]

        visited = set((v,))
        stack = []
        dad = v

        while parent[dad] != dad:
            dad = parent[dad]
            if weights[dad] - ref_weight in (ref_weight, total - 2 * ref_weight):
                print("dfs_up dad:", dad)
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
                        print("dfs_up u:", u)
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
                        print("dfs_down u:", u)
                        return True
        return False

    candidates_up = []
    candidates_down = []

    for v, dad in parent.items():
        if 3 * weights[v] > total and 2 * weights[v] < total:
            candidates_up.append(v)
        if 3 * (total - weights[v]) > total and 2 * (total - weights[v]) < total:
            candidates_down.append(v)

    print("weights:", weights)
    print("candidates_up:", candidates_up)
    print("candidates_down:", candidates_down)

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
    graph = build_adj_list(edges)
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
