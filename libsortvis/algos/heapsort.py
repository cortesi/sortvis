
def sift(lst, start, count):
    root = start
    while (root * 2) + 1 < count:
        child = (root * 2) + 1
        if child < (count-1) and lst[child] < lst[child+1]:
            child += 1
        if lst[root] < lst[child]:
            lst[root], lst[child] = lst[child], lst[root]
            lst.log()
            root = child
        else:
            return

def heapsort(lst):
    start = (len(lst)/2)-1
    end = len(lst)-1
    while start >= 0:
        sift(lst, start, len(lst))
        start -= 1
    while end > 0:
        lst[end], lst[0] = lst[0], lst[end]
        lst.log()
        sift(lst, 0, end)
        end -= 1
