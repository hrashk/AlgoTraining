#!/bin/python3

import math
import os
import random
import re
import sys

from collections import namedtuple

Edge = namedtuple('Edge', ['city', 'cost'])

def build_adj_list(roads):
    graph = [[] for _ in range(len(roads) + 1)]
    for v1, v2, cost in roads:
        graph[v1].append(Edge(v2, cost))
        graph[v2].append(Edge(v1, cost))
    return graph

def delete_city(graph, city, parent):
    pass

def collapse_city(graph, city, parent):
    edges = graph[city]
    return edges[0].city if edges[0].city != parent[city] else edges[1].city

def collapse_cities_without_machines(graph, start, machines):
    forest = [start]
    stack = [start]
    parent = {start: None}
    edges_to_delete = []

    while len(stack) > 0:
        top = stack[-1]
        edges = graph[top]
        unvisited = [e.city for e in edges if e.city not in parent]

        if not top in machines:
            if len(edges) == 1:
                delete_city(graph, top, parent)
            elif len(edges) == 2 and unvisited[0] not in machines:
                new_city = collapse_city(graph, top, parent)
                stack[-1] = new_city
                continue
        else:
            edges_to_delete.extend((top, city) for city in unvisited if city in machines)                

        if len(unvisited) == 0:
            stack.pop()
        else:
            parent.update({city: top for city in unvisited})
            stack.extend(unvisited)

    return edges_to_delete, parent

def minTime(roads, machines):
    start = machines[0]
    machines = set(machines)
    graph = build_adj_list(roads)
    edges_to_delete, parent = collapse_cities_without_machines(graph, start, machines)

    print(edges_to_delete)
    print(parent)
    return 0

if __name__ == '__main__':
    teststr = """
5 3
2 1 8
1 0 5
2 4 5
1 3 4
2
4
0
""".strip().split('\n')

    nk = teststr[0].split()

    n = int(nk[0])

    k = int(nk[1])

    roads = []

    for i in range(1, n):
        roads.append([int(x) for x in teststr[i].split()])

    machines = []

    for i in range(n, n + k):
        machines.append(int(teststr[i]))

    result = minTime(roads, machines)
    print(result)
