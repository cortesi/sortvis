import libpry
from libsortvis import sortable, algos


class uTrackList(libpry.AutoTree):
    def test_simple(self):
        l = [1, 2, 3]
        t = sortable.TrackList(l)
        assert t[0].path == [0]
        t[0], t[1] = t[1], t[0]
        t.log()
        assert t[1].path == [0, 1]


class uAlgorithms(libpry.AutoTree):
    # This value needs to be a power of 2, because bitonic sort requires it.
    N = 2**5
    def test_all(self):
        for (k, v) in algos.algorithms.items():
            l = range(self.N)
            l.reverse()
            l = sortable.TrackList(l)
            v(l)
            if not [x.i for x in l] == range(self.N):
                print l
                raise AssertionError("%s failed to sort."%k)


tests = [
    uTrackList(),
    uAlgorithms(),
]

