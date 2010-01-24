import os.path
from libsortvis import graph, sortable
import libpry


OUTDIR = "tmp"
class _GraphTest(libpry.AutoTree):
    def setUpAll(self):
        if not os.path.exists(OUTDIR):
            os.mkdir(OUTDIR)


class uGrayscale(_GraphTest):
    def test_lineCoords(self):
        p = graph.Grayscale(100, 100)
        r = p.lineCoords([1, 2, 3, 4, 5], 5, 0.02)
        assert r[-1] == (1, 1)
        # Lead-in
        assert r[0][1] == r[1][1]
        assert r[0][0] != r[1][0]
        # Lead-out
        assert r[-1][1] == r[-2][1]
        assert r[-1][0] != r[-2][0]

    def test_draw(self):
        p = graph.Grayscale(100, 100)
        l = range(10)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_grayscale.png"), 3, 2)


class uWeave(_GraphTest):
    def test_draw(self):
        p = graph.Weave()
        l = range(16)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_weave.png"), True)


tests = [
    uGrayscale(),
    uWeave()
]
