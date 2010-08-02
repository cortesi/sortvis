
class Sortable:
    def __init__(self, tracklist, i):
        self.tracklist, self.i = tracklist, i
        self.path = []

    def __cmp__(self, other):
        self.tracklist.total_comparisons += 1
        return cmp(self.i, other.i)

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
        self.lst = [wrapper(i) for i in self.lst]
        self.start = self.lst[:]

    def reset(self):
        self.total_comparisons = 0
        self.lst = self.start[:]

    def __getattr__(self, attr):
        return getattr(self.lst, attr)
    
    def log(self):
        for i, v in enumerate(self):
            v.path.append(i)
