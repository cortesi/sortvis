
def cocktailsort(lst):
    begin, end = 0, len(lst) - 1
    finished = False
    while not finished:
        finished = True
        for i in xrange(begin, end):
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                lst.log()
                finished = False
        if finished:
            break
        finished = True
        end -= 1
        for i in reversed(xrange(begin, end)):
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                lst.log()
                finished = False
        begin += 1

