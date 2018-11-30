from sorting import partition


def test_basic():
    lst = [4, 3, 1, 7, 13, 9, 23]
    pivot_idx = 0
    pivot = lst[pivot_idx]  # == 4
    idx = partition(lst, pivot_idx, 0, len(lst) - 1)
    assert idx == 2
    assert lst[idx] == pivot
    assert all([lst[i] < pivot for i in range(idx)])
    assert all([lst[i] > pivot for i in range(idx + 1, len(lst))])
