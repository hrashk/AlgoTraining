def _generate_balanced_brackets(nbrackets, nleft, nright, s):
    if nleft == nright == nbrackets:
        yield ''.join(s)
        return
    if nleft < nbrackets:
        s.append('(')
        yield from _generate_balanced_brackets(nbrackets, nleft + 1, nright, s)
        s.pop()
    if nright < nleft:
        s.append(')')
        yield from _generate_balanced_brackets(nbrackets, nleft, nright + 1, s)
        s.pop()


def generate_balanced_brackets(nbrackets):
    yield from _generate_balanced_brackets(nbrackets, 0, 0, [])
