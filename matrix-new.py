#!/bin/python3

def find(city, parent):
    while parent[city] is not None:
        city = parent[city]
    return city

def union(city1, city2, parent, machines):
    head1 = find(city1, parent)
    head2 = find(city2, parent)

    if head1 in machines and head2 in machines:
        return False
    elif head1 in machines:
        parent[head2] = head1
    else:
        parent[head1] = head2

    return True

def minTime(roads, machines):
    machines = set(machines)
    parent = {i: None for i in range(len(roads) + 1)}
    cost = 0

    for city1, city2, time in sorted(roads, key=lambda r: r[2], reverse=True):
        if not union(city1, city2, parent, machines):
            cost += time
    assert machines == set(c for c, p in parent.items() if p is None), (parent, roads, machines)
    return cost

from random import randrange

def generate_random_tree_with_1_machine(size):
    roads = []
    for i in range(1, size):
        roads.append([i, randrange(i), randrange(1, 11)])
    machines = [randrange(size)]

    return roads, machines

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

    # result = minTime(roads, machines)
    # print(result)

    roads, machines = [(0, 1, 7)], [0, 1]
    result = minTime(roads, machines)
    assert result == 7

    # single machine
    for _ in range(30):
        roads, machines = generate_random_tree_with_1_machine(100)
        # for r in roads:
        #     print(r)
        result = minTime(roads, machines)
        assert result == 0

    # two connected machines
    for _ in range(30):
        roads, machines = generate_random_tree_with_1_machine(100)
        machine2_id = len(roads) + 1

        roads.append((machine2_id, machines[0], 7))
        machines.append(machine2_id)
        
        result = minTime(roads, machines)
        assert result == 7, result

    for _ in range(30):
        roads, machines = generate_random_tree_with_1_machine(100)
        machines = list(range(len(roads) + 1))
        result = minTime(roads, machines)
        total = sum(r[2] for r in roads)
        assert result == total, str(result) + " vs " + str(total)

    for _ in range(30):
        roads, machines = generate_random_tree_with_1_machine(100)
        machines = list(range(len(roads)))
        result = minTime(roads, machines)
        total = sum(r[2] for r in roads) - roads[-1][2]
        assert result == total, str(result) + " vs " + str(total)

    # two disconnected machines
    for _ in range(30):
        roads, machines = generate_random_tree_with_1_machine(100)
        machine2_id = len(roads) + 1

        roads.append((machine2_id,  (1 + machines[0]) % machine2_id, 20))
        machines.append(machine2_id)

        result = minTime(roads, machines)
        assert 0 < result < 20
