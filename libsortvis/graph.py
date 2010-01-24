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
    def __init__(self, width, height, line, border, highlights):
        self.width, self.height = width, height
        self.line, self.border = line, border
        self.highlights = highlights

    def _lineCoords(self, elem, l):
        init = 0.02 # Proportional initial length 
        lst = []
        xscale = (1.0-init)/len(elem.path)
        yscale = 1.0/l
        lst.append((0, yscale/2 + (yscale * elem.path[0])))
        lst.append((init, yscale/2 + (yscale * elem.path[0])))
        for i, v in enumerate(elem.path):
            lst.append(((xscale * i) + init, yscale/2 + (yscale * v)))
        lst.append((1, lst[-1][1]))
        return lst

    def draw(self, lst, title, fname, vertical=False):
        c = Canvas(self.width, self.height + 20)
        # Clearer when drawn in this order
        l = reversed(lst)
        ctx = c.ctx()
        for elem in l:
            for i in self._lineCoords(elem, len(lst)):
                ctx.line_to(self.width * i[0], self.height * i[1])
            ctx.set_line_cap(cairo.LINE_CAP_BUTT)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            if elem.i in self.highlights:
                ctx.set_source_rgb(*HIGHLIGHT)
            else:
                x = 1 - (float(elem.i)/len(lst)*0.7)
                ctx.set_source_rgb(x, x, x)
            ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
            ctx.set_line_width(self.line)
            ctx.stroke_border(self.border)

        ctx.select_font_face("Sans")
        ctx.set_font_size(15)
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.move_to(5, self.height + 15)
        # Don't put the number of comparisons in until we've revisited the algorithms
        # to make sure the figures are sensible
        # ctx.text_path(algo.name + "      " + "[%s comparisons]"%algo.comparisons)
        ctx.text_path(title)
        ctx.fill()
        c.save("%s.png"%fname, vertical)

