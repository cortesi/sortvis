
def mergesort(lst, left=0, right=None):
    if right is None:
        right = len(lst) - 1
    if left >= right:
        return
    middle = (left + right) // 2
    mergesort(lst, left, middle)
    mergesort(lst, middle + 1, right)
    i, end_i, j = left, middle, middle + 1
    while i <= end_i and j <= right:
        if lst[i] < lst[j]:
            i += 1
            continue
        lst[i], lst[i+1:j+1] = lst[j], lst[i:j]
        lst.log()
        i, end_i, j = i + 1, end_i + 1, j + 1
