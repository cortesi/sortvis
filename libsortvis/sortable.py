"""
    Some of these algorithms are taken rather literally from Knuth - as a
    consequence they're not very Pythonic, and not terribly readable.

    In some cases I've modified the algorithm to make sure that all items are
    present once and only once in the array of sortables every time we memoizePath
    (i.e. that the algorithm is in-place). 

    Page numbers refer to The Art of Computer Programming vol. 3.

    This code is in the public domain - do whatever you like with it.
"""

class Sortable:
    comparisons = 0
    def __init__(self, i):
        self.i = i
        self.path = []

    def __cmp__(self, other):
        Sortable.comparisons += 1
        return cmp(self.i, other.i)

    def __repr__(self):
        return str(self.i)


class TrackList:
    """
        A list-like object that logs the positions of its elements every time
        the log() method is called.
    """
    def __init__(self, itms, wrapper=None):
        self.lst = [Sortable(i) for i in itms]
        if wrapper:
            self.lst = [wrapper(i) for i in self.lst]
        self.start = self.lst[:]
        self.log()

    def reset(self):
        Sortable.comparisons = 0
        self.lst = self.start[:]

    def __getattr__(self, attr):
        return getattr(self.lst, attr)
    
    def log(self):
        for i, v in enumerate(self):
            v.path.append(i)
    

class Algorithm:
    def makeList(self, entries):
        return TrackList(entries)

    def __call__(self, lst):
        #self.comparisons = Sortable.comparisons
        lst = self.makeList(lst)
        lst.reset()
        self.sort(lst)
        return lst


# The TimSort stuff can be done more neatly, by inspecting the list from within
# the __cmp__ method. This way we can also perform the entire trick with only
# one sort. Then again, I'm lazy, and this works. ;)
class TimBreak(Exception): pass


class TimWrapper:
    list = None
    comparisons = 0
    limit = 0
    def __init__(self, n):
        self.n = n

    def __cmp__(self, other):
        if TimWrapper.comparisons > TimWrapper.limit:
            raise TimBreak
        TimWrapper.comparisons += 1
        return cmp(self.n, other.n)

    def __getattr__(self, attr):
        return getattr(self.n, attr)
    

class Tim(Algorithm):
    name = "timsort"
    def makeList(self, entries):
        l = TrackList(entries, TimWrapper)
        TimWrapper.list = l
        return l

    def sort(self, lst):
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


class Bubble(Algorithm):
    name = "bubblesort"
    def sort(self, lst):
        bound = len(lst)-1
        while 1:
            t = 0
            for j in range(bound):
                if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    lst.log()
                    t = j
            if t == 0:
                break
            bound = t
    

class ListInsertion(Algorithm):
    """
        Broadly based on the list insertion sort on p 97.  
    """
    name = "insertionsort"
    def sort(self, lst):
        for i in range(1, len(lst)):
            for j in range(i):
                if lst[i] < lst[j]:
                    x = lst.pop(i)
                    lst.insert(j, x)
                    lst.log()


class Shell(Algorithm):
    """
        Shell's method, p. 84
    """
    name = "shellsort"
    def sort(self, lst):
        t = [5, 3, 1]
        for h in t:
            for j in range(h, len(lst)):
                i = j - h
                r = lst[j]
                flag = 0
                while i > -1:
                    if r < lst[i]:
                        flag = 1
                        lst[i+h], lst[i] = lst[i], lst[i+h]
                        i -= h
                        lst.log()
                    else:
                        break
                lst[i+h] = r


class Selection(Algorithm):
    """
        Selection Sort, p. 139
    """
    name = "selectionsort"
    def sort(self, lst):
        for j in range(len(lst)-1, -1, -1):
            m = lst.index(max(lst[:j+1]))  # No, this is not efficient ;)
            lst[m], lst[j] = lst[j], lst[m]
            if m != j:
                lst.log()


class Heap(Algorithm):
    """
        Algorithm from http://en.wikipedia.org/wiki/Heapsort
    """
    name = "heapsort"
    def sift(self, lst, start, count):
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

    def sort(self, lst):
        start = (len(lst)/2)-1
        end = len(lst)-1
        while start >= 0:
            self.sift(lst, start, len(lst))
            start -= 1
        while end > 0:
            lst[end], lst[0] = lst[0], lst[end]
            lst.log()
            self.sift(lst, 0, end)
            end -= 1


class Quick(Algorithm):
    """
        http://www.cs.indiana.edu/classes/a348-dger/lectures/tsort/1.0.2/QSortAlgorithm.java
    """
    name = "quicksort"
    def sort(self, lst, left=0, right=None):
        if right is None:
            right = len(lst) - 1
        l = left
        r = right
        if l <= r:
            mid = lst[(left+right)/2]
            while l <= r:
                while l <= right and lst[l] < mid:
                    l += 1
                while r > left and lst[r] > mid:
                    r -= 1
                if l <= r:
                    lst[l], lst[r] = lst[r], lst[l]
                    if l != r:
                        lst.log()
                    l+=1
                    r-=1
            if left < r:
                self.sort(lst, left, r)
            if l < right:
                self.sort(lst, l, right)


algorithms = [Tim, Quick, Heap, Selection, ListInsertion, Bubble, Shell]
