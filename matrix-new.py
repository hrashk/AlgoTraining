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

def delete_leaf(graph, city, dad):
    city_idx = next(i for i,v in enumerate(graph[dad]) if v.city == city)
    del graph[dad][city_idx]
    del graph[city][0]

def delete_road(graph, c1, c2):
    city_idx = next(i for i,v in enumerate(graph[c1]) if v.city == c2)
    del graph[c1][city_idx]

    city_idx = next(i for i,v in enumerate(graph[c2]) if v.city == c1)
    cost = graph[c2][city_idx].cost
    del graph[c2][city_idx]

    return cost


def collapse_city(graph, city, dad):
    city_edges = graph[city]
    target_city = city_edges[0].city if city_edges[0].city != dad else city_edges[1].city

    dad_idx = next(i for i,v in enumerate(graph[dad]) if v.city == city)

    target_idx = next(i for i,v in enumerate(graph[target_city]) if v.city == city)

    cost = min(e.cost for e in city_edges)
    graph[dad][dad_idx] = Edge(target_city, cost)
    graph[target_city][target_idx] = Edge(dad, cost)
    graph[city] = []

    return target_city

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
            dad = parent[top]
            if len(edges) == 1:
                delete_leaf(graph, top, dad)
            elif len(edges) == 2 and not (dad is None or dad in machines):
                new_city = collapse_city(graph, top, dad)
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

    cost = 0
    for c1, c2 in edges_to_delete:
        cost += delete_road(graph, c1, c2)

    print(parent)
    for c, edges in enumerate(graph):
        print(c, edges)
    return cost

if __name__ == '__main__':
    teststr1 = """
5 3
2 1 8
1 0 5
2 4 5
1 3 4
2
4
0
""".strip().split('\n')
    teststr = """
5 3
1 2 3
3 1 7
0 1 4
4 0 2
2
3
4
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
