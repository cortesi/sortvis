from functools import total_ordering


class TimBreak(Exception): pass


@total_ordering
class TimWrapper:
    list = None
    comparisons = 0
    limit = 0
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        if TimWrapper.comparisons > TimWrapper.limit:
            raise TimBreak
        TimWrapper.comparisons += 1
        return self.n == other.n

    def __lt__(self, other):
        if TimWrapper.comparisons > TimWrapper.limit:
            raise TimBreak
        TimWrapper.comparisons += 1
        return self.n < other.n

    def __getattr__(self, attr):
        return getattr(self.n, attr)
    

def timsort(lst):
    lst.wrap(TimWrapper)
    TimWrapper.list = lst
    prev = [i.n for i in lst]
    while 1:
        TimWrapper.comparisons = 0
        TimWrapper.limit += 1
        lst.reset()
        try:
            lst.sort()
        except TimBreak:
            if prev != [i.n for i in lst]:
                lst.log()
                prev = [i.n for i in lst]
        else:
            lst.log()
            break
