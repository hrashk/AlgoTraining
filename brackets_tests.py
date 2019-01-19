import pytest
from brackets import generate_balanced_brackets


def test_0_brackets():
    seqs = list(generate_balanced_brackets(0))
    assert seqs == ['']


def test_1_bracket():
    seqs = list(generate_balanced_brackets(1))
    assert seqs == ['()']


def test_2_brackets():
    seqs = list(generate_balanced_brackets(2))
    assert seqs == ['(())', '()()']


def test_3_brackets():
    seqs = list(generate_balanced_brackets(3))
    assert seqs == [
        '((()))',
        '(()())',
        '(())()',
        '()(())',
        '()()()']


def test_order():
    seq = generate_balanced_brackets(10)
    prev = next(seq)
    try:
        while True:
            curr = next(seq)
            assert curr > prev
            prev = curr
    except StopIteration:
        pass


def test_size():
    sizes = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786]
    for i, s in enumerate(sizes):
        assert sum(1 for _ in generate_balanced_brackets(i)) == s
