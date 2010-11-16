from copy import copy

class Comparator(object):
    """ A comparator wrapping a list element and doing all the counts.
        In the rare case of extending this class, make sure that the 
        wrapped element is always self.i, and has a self.path list."""
    def __init__(self, tracklist, i):
        self.tracklist, self.i = tracklist, i
        self.path = []

    def __cmp__(self, other):
        """ Counts each comparison between two elements and redirects
            to the underlying __cmp__ method of the i's wrapped in this."""
        self.tracklist.total_comparisons += 1
        self.tracklist.log()
        self.tracklist.addComparison(self,other)
        return cmp(self.i, other.i)
    
    def __repr__(self):
        return str(self.i)


class TrackList(object):
    """
        A list-like object that logs the positions of its elements every time
        the log() method is called.
    """
    def __init__(self, itms, comparator=Comparator):
        """ You can either specify a comparator at init or set a different one later."""
        self.lst = [comparator(self, i) for i in itms]
        self.start = copy(self.lst)
        self.total_comparisons = 0
        self.comparisonList = []
        self.log()

    def setComparator(self, comparator, wrapOldOne=False):
        """ Allows an additional wrapping of the inner list with the given
            wrapper or substitution of the existing one (wrapOldOne=False).
            See algos.timsort as an example. """
        if wrapOldOne:
            self.lst = [comparator(self, i) for i in self.lst]
        else:
            self.lst = [comparator(self, i.i) for i in self.lst]
            self.log()
        self.start = copy(self.lst)

    def reset(self):
        """ reset original ordering. Does _not_ reset counts or path info."""
#        self.total_comparisons = 0
        self.lst = copy(self.start)

    def __getattr__(self, attr):
        """ Redirecting every lookup (aside from special method lookups)
            on this object that didn't succeed to the internal list
            (e.g., iterating over self iterates over list)."""
        return getattr(self.lst, attr)
    
    # special method lookups need to be defined explicitly in new style classes.
    def __len__(self):
        return len(self.lst)
    def __getitem__(self, index):
        return self.lst[index]
    def __setitem__(self, index, value):
        self.lst[index] = value
    def __delitem__(self, index):
        del self.lst[index]
    def __iter__(self):
        return iter(self.lst)
    def __reversed__(self):
        return reversed(self.lst)
    def __contains__(self, value):
        return value in self.lst
    
    def addComparison(self,cmps,cmpo):
        spos,opos = None, None
        if cmps.i == cmpo.i: print "stupid self comparison", cmps.i
        for j,k in enumerate(self.lst):
            if k.i == cmps.i: spos = j
            if k.i == cmpo.i: opos = j
        assert spos != None
        assert opos != None
        self.comparisonList.append((spos, opos))
    
    def log(self):
        """ logs list whenever the comparison counter was changed."""
        for i, v in enumerate(self.lst):
            v.path.append(i)
