import pytest
from sorting import partition


def test_basic():
    lst = [4, 3, 1, 7, 13, 9, 23]
    pivot = lst[0]  # == 4
    idx = partition(lst, pivot, 0, len(lst) - 1)
    assert idx == 2
    assert lst[idx] == pivot
    assert all([lst[i] < pivot for i in range(idx)])
    assert all([lst[i] > pivot for i in range(idx + 1, len(lst))])


def test_edges():
    assert partition([1], 0, 0, 0) == 0
    assert partition([1, 2], 4, 0, 0) == 0
    assert partition([1, 2], 4, 1, 1) == 1


def test_exceptions():
    with pytest.raises(IndexError):
        partition([], 0, 0, 1)
    with pytest.raises(IndexError):
        partition([1, 2], 0, -3, 1)
    with pytest.raises(IndexError):
        partition([1, 2], 0, 0, 2)
