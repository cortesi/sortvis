import os.path
from libsortvis import graph, sortable
import libpry


OUTDIR = "tmp"
class _GraphTest(libpry.AutoTree):
    def setUpAll(self):
        if not os.path.exists(OUTDIR):
            os.mkdir(OUTDIR)


class uPathDrawer(_GraphTest):
    def test_lineCoords(self):
        p = graph.PathDrawer(100, 100, 5, 1)
        r = p.lineCoords([1, 2, 3, 4, 5], 5, 0.02)
        assert r[-1] == (1, 1)
        # Lead-in
        assert r[0][1] == r[1][1]
        assert r[0][0] != r[1][0]
        # Lead-out
        assert r[-1][1] == r[-2][1]
        assert r[-1][0] != r[-2][0]

    def test_draw(self):
        p = graph.PathDrawer(100, 100, 5, 1)
        l = range(10)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_draw.png"))


tests = [
    uPathDrawer()
]
