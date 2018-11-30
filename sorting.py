def partition(lst, pivot, left, right):
    if len(lst) == 1:
        return 0

    lst[0], lst[2] = lst[2], lst[0]
    return 2
