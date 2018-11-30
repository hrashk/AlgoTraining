def partition(lst, pivot, left, right):
    while left < right:
        while lst[left] < pivot:
            left += 1
        while lst[right] > pivot:
            right -= 1
        lst[left], lst[right] = lst[right], lst[left]

    return left
