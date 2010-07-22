
def oddevensort(lst, nloops=2):
    finished = False
    while not finished:
        finished = True
        for n in xrange(nloops):
            for i in xrange(n, len(lst) - 1, nloops):
                if lst[i] > lst[i + 1]:
                    lst[i], lst[i + 1] = lst[i + 1], lst[i]
                    lst.log()
                    finished = False


