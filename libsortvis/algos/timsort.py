from ..sortable import Comparator
class TimBreak(Exception):
    def __init__(self, *args):
        super(TimBreak, self).__init__(*args)

class TimComparator(Comparator):
    comparisons = 0
    limit = 0
    def __init__(self, tracklist, i):
        super(TimComparator, self).__init__(tracklist, i)

    def __cmp__(self, other):
        TimComparator.comparisons += 1
        if TimComparator.comparisons > TimComparator.limit:
            self.tracklist.total_comparisons += 1
            raise TimBreak(self, other)
        return cmp(self.i, other.i)
    

def timsort(lst):
    # we need a hack in this one, as the TrackList.lst pointer to the list
    # is set to [] while lst.sort() is running
    # so what happens here is: we break each sort after limit comparisons,
    # log the outcome, increase limit by 1 and run again from the beginning.
    TimComparator.comparisons = 0
    TimComparator.limit = 0
    lst.setComparator(TimComparator, wrapOldOne=False)
    TimComparator.list = lst
    while 1:
        TimComparator.comparisons = 0
        TimComparator.limit += 1
        lst.reset()
        try:
            lst.sort()
        except TimBreak as t:
            s,o = t
            lst.addComparison(s,o)
            lst.log()
        else:
            lst.log()
            break
    
