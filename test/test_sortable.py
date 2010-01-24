import libpry
from libsortvis import sortable


class uTrackList(libpry.AutoTree):
    def test_simple(self):
        l = [1, 2, 3]
        t = sortable.TrackList(l)
        assert t[0].path == [0]
        t[0], t[1] = t[1], t[0]
        t.log()
        assert t[1].path == [0, 1]


class uAlgorithms(libpry.AutoTree):
    def test_all(self):
        for i in sortable.algorithms:
            l = range(10)
            l.reverse()
            a = i()(l)
            if not [x.i for x in a] == range(10):
                raise AssertionError("%s failed to sort."%i.name)
                assert len(a[0].path) > 5


tests = [
    uTrackList(),
    uAlgorithms(),
]

