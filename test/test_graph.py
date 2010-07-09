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
        csource = graph.ColourGradient((1, 1, 1), (0, 0, 0))
        p = graph.Weave(
            csource, 100, 100, 20, graph.rgb("ffffff"),
            False, 6, 1
        )
        r = p.lineCoords([1, 2, 3, 4, 5], 5, 0.02)
        assert r[-1] == (1, 1)
        # Lead-in
        assert r[0][1] == r[1][1]
        assert r[0][0] != r[1][0]
        # Lead-out
        assert r[-1][1] == r[-2][1]
        assert r[-1][0] != r[-2][0]

    def test_draw(self):
        csource = graph.ColourGradient((1, 1, 1), (0, 0, 0))
        p = graph.Weave(
            csource, 100, 100, 20, graph.rgb("ffffff"),
            False, 6, 1
        )
        l = range(10)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_grayscale.png"))


class uDense(_GraphTest):
    def test_draw(self):
        csource = graph.ColourGradient((1, 1, 1), (0, 0, 0))
        p = graph.Dense(csource, 20, graph.rgb("ffffff"), False)
        l = range(8)
        l.reverse()
        a = sortable.ListInsertion()(l)
        p.draw(a, "test", os.path.join(OUTDIR, "test_weave.png"))


class uUtils(libpry.AutoTree):
    def test_rgb(self):
        assert graph.rgb((255, 255, 255)) == (1, 1, 1)
        assert graph.rgb("ffffff") == (1, 1, 1)
        assert graph.rgb("000000") == (0, 0, 0)


class uColourSource(libpry.AutoTree):
    def test_gradient(self):
        g = graph.ColourGradient((1, 1, 1), (0, 0, 0))
        assert g.colour(0, 10) == (1.0, 1.0, 1.0)
        assert g.colour(10, 10) == (0, 0, 0)
        assert g.colour(5, 10) == (0.5, 0.5, 0.5)

        g = graph.ColourGradient((0, 0, 0), (1, 1, 1))
        assert g.colour(0, 10) == (0, 0, 0)
        assert g.colour(10, 10) == (1.0, 1.0, 1.0)
        assert g.colour(5, 10) == (0.5, 0.5, 0.5)

    def test_hilbert(self):
        g = graph.ColourHilbert()
        assert g.colour(50, 200)
        assert g.colour(50, 200)



tests = [
    uWeave(),
    uDense(),
    uUtils(),
    uColourSource()
]
