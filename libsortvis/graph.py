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


class ColourGradient:
    """
        A straight line drawn through the colour cube from a start value to an
        end value.
    """
    name = "gradient"
    def __init__(self, start, end):
        self.start, self.end = start, end

    def colour(self, x, l):
        scale = x/float(l)
        parts = list(self.start)
        for i, v in enumerate(parts):
            parts[i] = parts[i] + (self.start[i]-self.end[i])*scale*-1
        return tuple(parts)


class ColourHilbert:
    """
        A Hilbert-order traversal of the colour cube. 
    """
    def __init__(self):
        self.size = None
        self.curve = None

    def findSize(self, n):
        """
            Return the smallest Hilbert curve size larger than n. 
        """
        for i in range(100):
            s = 2**(3*i)
            if s >= n:
                return s
        raise ValueError("Number of elements impossibly large.")

    def colour(self, x, n):
        if n != self.size:
            self.curve = scurve.fromSize("hilbert", 3, self.findSize(n))
        d = float(self.curve.dimensions()[0])
        # Scale X to sample evenly from the curve, if the list length isn't
        # an exact match for the Hilbert curve size.
        x = x*int(len(self.curve)/float(n))
        return tuple([i/d for i in self.curve.point(x)])
                
    
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

    def set_background(self, colour):
        c = self.ctx()
        c.set_source_rgb(*colour)
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
    def __init__(self, csource):
        """
            csource: A colour source
        """
        self.csource = csource

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
            c = self.csource.colour(elem.i, len(lst)) + (1,)
            ctx.set_source_rgba(*c)
            if borderwidth:
                ctx.stroke_border(borderwidth)
            else:
                ctx.stroke()

    def drawPixels(self, canvas, lst, unmoved):
        ctx = canvas.ctx()
        for elem in lst:
            ctx.set_source_rgb(*self.csource.colour(elem.i, len(lst)))
            moved = unmoved
            for x, y in enumerate(elem.path):
                if y != elem.path[0]:
                    moved = True
                if moved:
                    ctx.rectangle(x, y, 1, 1)
                    ctx.fill()

    def drawTitle(self, canvas, title, xpos, ypos, size, colour, font="Sans"):
        ctx = canvas.ctx()
        ctx.select_font_face(font)
        ctx.set_font_size(size)
        ctx.set_source_rgb(*colour)
        ctx.move_to(xpos, ypos)
        ctx.text_path(title)
        ctx.fill()


class Weave(_PathDrawer):
    def __init__(self, csource, width, height, titleHeight, titleColour, background,
                       rotate, linewidth, borderwidth):
        _PathDrawer.__init__(self, csource)
        self.width, self.height, self.titleHeight = width, height, titleHeight
        self.titleColour = titleColour
        self.background = background
        self.rotate, self.linewidth, self.borderwidth = rotate, linewidth, borderwidth

    def getColor(self, x, n):
        v = 1 - (float(x)/n*0.7)
        return (v, v, v)

    def draw(self, lst, title, fname):
        c = Canvas(self.width, self.height, self.background)
        # Clearer when drawn in this order
        lst.reverse()
        if title:
            self.drawPaths(
                c,
                self.linewidth,
                self.borderwidth,
                self.width,
                self.height-self.titleHeight,
                lst
            )
        else:
            self.drawPaths(c, self.linewidth, self.borderwidth, self.width, self.height, lst)
        if title:
            self.drawTitle(
                c,
                title,
                5,
                self.height-self.TITLEGAP,
                self.titleHeight-self.TITLEGAP,
                self.titleColour
            )
        c.save(fname, self.rotate)


class Dense(_PathDrawer):
    def __init__(self, csource, titleHeight, titleColour, background, unmoved):
        _PathDrawer.__init__(self, csource)
        self.titleColour = titleColour
        self.titleHeight = titleHeight
        self.background = background
        self.unmoved = unmoved

    def draw(self, lst, title, fname):
        height = len(lst)
        width = len(lst[0].path)
        c = Canvas(width, height + (self.titleHeight if title else 0), self.background)
        # Clearer when drawn in this order
        lst.reverse()
        self.drawPixels(c, lst, not self.unmoved)
        if title:
            self.drawTitle(
                c,
                title,
                5,
                height+self.titleHeight-self.TITLEGAP,
                self.titleHeight-self.TITLEGAP,
                self.titleColour
            )
        c.save(fname, False)


