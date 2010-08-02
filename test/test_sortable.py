import random
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
    def test_bitonicsort(self):
        algos.bitonicsort.bitonicsort(sortable.TrackList(range(2**1)))
        algos.bitonicsort.bitonicsort(sortable.TrackList(range(2**3)))
        libpry.raises(AssertionError, algos.bitonicsort.bitonicsort, range(3))
        libpry.raises(AssertionError, algos.bitonicsort.bitonicsort, range(9))

    def test_all(self):
        seqs = [
            range(self.N),
            list(reversed(range(self.N))),
        ]

        l = range(self.N)
        l[0], l[-1] = l[-1], l[0]
        seqs.append(l)

        for i in range(5):
            l = range(self.N)
            random.shuffle(l)
            seqs.append(l)

        for seq in seqs:
            for (k, v) in algos.algorithms.items():
                l = sortable.TrackList(seq)
                v(l)
                if not [x.i for x in l] == range(self.N):
                    print l
                    raise AssertionError("%s failed to sort."%k)


tests = [
    uTrackList(),
    uAlgorithms(),
]

