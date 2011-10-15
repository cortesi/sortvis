
class Sortable:
    def __init__(self, tracklist, i):
        self.tracklist, self.i = tracklist, i
        self.path = []

    def __cmp__(self, other):
        """ Counts each comparison between two elements and redirects
            to the underlying __cmp__ method of the i's wrapped in this."""
        self.tracklist.total_comparisons += 1
        try:
            return cmp(self.i, other.i)
        except AttributeError:
            return cmp(self.i, other)

    def __int__(self):
        return self.i

    def __repr__(self):
        return str(self.i)


class TrackList:
    """
        A list-like object that logs the positions of its elements every time
        the log() method is called.
    """
    def __init__(self, itms):
        self.lst = [Sortable(self, i) for i in itms]
        self.start = self.lst[:]
        self.total_comparisons = 0
        self.log()

    def wrap(self, wrapper):
        """ Allows an additional wrapping of the inner list with the given
            wrapper. See algos.timsort as an example. """
        self.lst = [wrapper(i) for i in self.lst]
        self.start = self.lst[:]

    def reset(self):
        self.total_comparisons = 0
        self.lst = self.start[:]

    def __getattr__(self, attr):
        """ Redirecting every lookup on this object that didn't succeed to
            the internal list (e.g., iterating over self iterates over list)."""
        return getattr(self.lst, attr)
    
    def log(self):
        for i, v in enumerate(self):
            if v is not None:
                v.path.append(i)


class DummySortable(object):
    def __init__(self, i):
        self.i = i
        self.path = []

    def __int__(self):
        return self.i



def read_paths(fp):
    """
        Reads a sorting history from a filepointer, and returns a list of Sortables.

        The sorting history is specified as a set of newline-terminated lists,
        with each list consisting of space-separated numbers.
    """
    sortables = {}
    for i in fp.readlines():
        n = i.split()
        if not sortables:
            for j in n:
                j = int(j)
                sortables[j] = DummySortable(j)
        for offset, j in enumerate(n):
            sortables[int(j)].path.append(offset)
    return sortables.values()

