from functools import total_ordering


@total_ordering
class Sortable:
    def __init__(self, tracklist, i):
        self.tracklist, self.i = tracklist, i
        self.path = []

    def __eq__(self, other):
        """ Counts each comparison between two elements and redirects
            to the underlying comparison of the i's wrapped in this."""
        self.tracklist.total_comparisons += 1
        return self.i == other

    def __lt__(self, other):
        """ Counts each comparison between two elements and redirects
            to the underlying comparison of the i's wrapped in this."""
        self.tracklist.total_comparisons += 1
        return self.i < other.i

    def __int__(self):
        return self.i

    def __repr__(self):
        return str(self.i)


class TrackList(list):
    """
        A list-like object that logs the positions of its elements every time
        the log() method is called.
    """
    def __init__(self, itms):
        super().__init__()
        self.start = [Sortable(self, i) for i in itms]
        self.extend(self.start)
        self.total_comparisons = 0
        self.log()

    def wrap(self, wrapper):
        """ Allows an additional wrapping of the inner list with the given
            wrapper. See algos.timsort as an example. """
        self.start = [wrapper(i) for i in self]
        self.clear()
        self.extend(self.start)

    def reset(self):
        self.total_comparisons = 0
        self.clear()
        self.extend(self.start)

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

