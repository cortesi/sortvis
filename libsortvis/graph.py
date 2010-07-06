import cairo
import math

try:
    import scurve
except ImportError:
    scurve = None


def rgb(x):
    if isinstance(x, tuple) or isinstance(x, list):
        return (x[0]/255.0, x[1]/255.0, x[2]/255.0)
    elif isinstance(x, basestring):
        if len(x) != 6:
            raise ValueError("RGB specifier must be 6 characters long.")
        return rgb([int(i, 16) for i in (x[0:2], x[2:4], x[4:6])])
    raise ValueError("Invalid RGB specifier.")
                
    
class NiceCtx(cairo.Context):
    defaultBorderColour = rgb((0x7d, 0x7d, 0x7d))
    def stroke_border(self, border):
        src = self.get_source()
        width = self.get_line_width()
        self.set_source_rgba(*self.defaultBorderColour)
        self.stroke_preserve()
        self.set_source(src)
        self.set_line_width(width - (border * 2))
        self.stroke()
        self.set_line_width(width)


class Canvas:
    def __init__(self, width, height, background):
        self.width, self.height = width, height
        self.background = background
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.set_background(background)

    def ctx(self):
        return NiceCtx(self.surface)

    def set_background(self, color):
        c = self.ctx()
        c.set_source_rgb(*color)
        c.rectangle(0, 0, self.width, self.height)
        c.fill()
        c.stroke()

    def save(self, fname, rotate):
        """
            Save the image to a file. If rotate is true, rotate by 90 degrees.
        """
        if rotate:
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.height, self.width)
            ctx = cairo.Context(surf)
            ctx.translate(self.height*0.5, self.width*0.5)
            ctx.rotate(math.pi/2)
            ctx.translate(-self.width*0.5, -self.height*0.5)
            ctx.set_source_surface(self.surface)
            ctx.paint()
        else:
            surf = self.surface
        surf.write_to_png(fname)
            

class _PathDrawer:
    TITLEGAP = 5
    def lineCoords(self, positions, length, edge=0.02):
        """
            Returns a list of proportional (x, y) co-ordinates for a given list
            of Y-offsets. Each co-ordinate value is a floating point number
            between 0 and 1, inclusive.
        """
        xscale = (1.0-(2*edge))/(len(positions)-1)
        yscale = 1.0/length
        coords = []
        coords.append((0, positions[0]*yscale))
        for i, v in enumerate(positions):
            coords.append(((xscale * i) + edge, v*yscale))
        coords.append((1, v*yscale))
        return coords

    def drawPaths(self, canvas, linewidth, borderwidth, width, height, lst):
        ctx = canvas.ctx()
        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_width(linewidth)
        for elem in lst:
            for i in self.lineCoords(elem.path, len(lst)):
                ctx.line_to(width * i[0], linewidth + height * i[1])
            ctx.set_source_rgb(*self.getColor(elem.i, len(lst)))
            ctx.stroke_border(borderwidth)

    def drawPixels(self, canvas, lst, unmoved):
        ctx = canvas.ctx()
        for elem in lst:
            ctx.set_source_rgb(*self.getColor(elem.i, len(lst)))
            moved = unmoved
            for x, y in enumerate(elem.path):
                if y != elem.path[0]:
                    moved = True
                if moved:
                    ctx.rectangle(x, y, 1, 1)
                    ctx.fill()

    def drawTitle(self, canvas, title, xpos, ypos, size, font="Sans"):
        ctx = canvas.ctx()
        ctx.select_font_face(font)
        ctx.set_font_size(size)
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.move_to(xpos, ypos)
        ctx.text_path(title)
        ctx.fill()

    def getColor(self, x, n):
        """
            Retrieve the color for item x out of n.
        """
        raise NotImplementedError


class Weave(_PathDrawer):
    def __init__(self, width, height, titleHeight, background):
        self.width, self.height, self.titleHeight = width, height, titleHeight
        self.background = background

    def getColor(self, x, n):
        v = 1 - (float(x)/n*0.7)
        return (v, v, v)

    def draw(self, lst, title, fname, linewidth, borderwidth, rotate=False):
        c = Canvas(self.width, self.height, self.background)
        # Clearer when drawn in this order
        lst.reverse()
        if title:
            self.drawPaths(
                c,
                linewidth,
                borderwidth,
                self.width,
                self.height-self.titleHeight,
                lst
            )
        else:
            self.drawPaths(c, linewidth, borderwidth, self.width, self.height, lst)
        if title:
            self.drawTitle(
                c,
                title,
                5,
                self.height-self.TITLEGAP,
                self.titleHeight-self.TITLEGAP
            )
        c.save(fname, rotate)



class Dense(_PathDrawer):
    def __init__(self, titleHeight, background):
        self.titleHeight = titleHeight
        self.background = background

    def draw(self, lst, title, fname, unmoved):
        height = len(lst)
        width = len(lst[0].path)
        c = Canvas(width, height + (self.titleHeight if title else 0), self.background)
        # Clearer when drawn in this order
        lst.reverse()
        self.drawPixels(c, lst, unmoved)
        if title:
            self.drawTitle(
                c,
                title,
                5,
                height+self.titleHeight-self.TITLEGAP,
                self.titleHeight-self.TITLEGAP
            )
        c.save(fname, False)


class DenseGrayscale(Dense):
    def getColor(self, x, n):
        return [x/float(n), x/float(n), x/float(n)]


if scurve:
    class DenseFruitsalad(Dense):
        csource = None
        def findSize(self, n):
            """
                Return the smallest Hilbert curve size larger than n. 
            """
            for i in range(100):
                s = 2**(3*i)
                if s >= n:
                    return s
            raise ValueError("Number of elements impossibly large.")

        def getColor(self, x, n):
            if not self.csource:
                self.csource = scurve.fromSize("hilbert", 3, self.findSize(n))
            d = float(self.csource.dimensions()[0])
            # Scale X to sample evenly from the curve, if the list length isn't
            # an exact match for the Hilbert curve size.
            x = x*int(len(self.csource)/float(n))
            return [i/d for i in self.csource.point(x)]

