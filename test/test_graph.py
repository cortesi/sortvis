import os.path
from libsortvis import graph, sortable
import libpry


OUTDIR = "tmp"
class _GraphTest(libpry.AutoTree):
    def setUpAll(self):
        if not os.path.exists(OUTDIR):
            os.mkdir(OUTDIR)

class uWeave(_GraphTest):
    def test_lineCoords(self):
        p = graph.Weave(100, 100, 20, graph.rgb("ffffff"))
        r = p.lineCoords([1, 2, 3, 4, 5], 5, 0.02)
        assert r[-1] == (1, 1)
        # Lead-in
        assert r[0][1] == r[1][1]
        assert r[0][0] != r[1][0]
        # Lead-out
        assert r[-1][1] == r[-2][1]
        assert r[-1][0] != r[-2][0]

    def test_draw(self):
        p = graph.Weave(100, 100, 20, graph.rgb("ffffff"))
        l = range(10)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_grayscale.png"), 3, 2)


class uDense(_GraphTest):
    def test_draw(self):
        p = graph.DenseFruitsalad(20, graph.rgb("ffffff"))
        l = range(8)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_weave.png"), True)


class uUtils(libpry.AutoTree):
    def test_rgb(self):
        assert graph.rgb((255, 255, 255)) == (1, 1, 1)
        assert graph.rgb("ffffff") == (1, 1, 1)
        assert graph.rgb("000000") == (0, 0, 0)


tests = [
    uWeave(),
    uDense(),
    uUtils()
]
