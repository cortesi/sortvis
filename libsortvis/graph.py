import cairo


def intRGB(r, g, b):
        return (r/255.0, g/255.0, b/255.0)


HIGHLIGHT=intRGB(0xff, 0x72, 0x72)


class NiceCtx(cairo.Context):
    defaultBorderColour = intRGB(0x7d, 0x7d, 0x7d)
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
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.background(1, 1, 1)

    def ctx(self):
        return NiceCtx(self.surface)

    def background(self, r, g, b):
        c = self.ctx()
        c.set_source_rgb(r, g, b)
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
            

class PathDrawer:
    TITLEGAP = 5
    def __init__(self, width, height, line, border, highlights):
        self.width, self.height = width, height
        self.line, self.border = line, border
        self.highlights = highlights

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

    def drawPaths(self, canvas, width, height, lst):
        ctx = canvas.ctx()
        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_width(self.line)
        for elem in lst:
            for i in self.lineCoords(elem.path, len(lst)):
                ctx.line_to(self.width * i[0], self.line + self.height * i[1])
            if self.highlights and elem.i in self.highlights:
                ctx.set_source_rgb(*HIGHLIGHT)
            else:
                x = 1 - (float(elem.i)/len(lst)*0.7)
                ctx.set_source_rgb(x, x, x)
            ctx.stroke_border(self.border)

    def draw(self, lst, title, fname, titleHeight = 20, rotate = False):
        if title:
            c = Canvas(self.width, self.height + titleHeight)
        else:
            c = Canvas(self.width, self.height)
        # Clearer when drawn in this order
        lst.reverse()
        self.drawPaths(c, self.width, self.height, lst)

        if title:
            ctx = c.ctx()
            ctx.select_font_face("Sans")
            ctx.set_font_size(titleHeight-self.TITLEGAP)
            ctx.set_source_rgb(0.3, 0.3, 0.3)
            ctx.move_to(5, self.height + titleHeight - self.TITLEGAP)
            ctx.text_path(title)
            ctx.fill()

        c.save(fname, rotate)

