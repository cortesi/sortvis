#!/usr/bin/env python
import random, math, sys
from optparse import OptionParser
import libsortvis.sortable
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

    def save(self, fname, vertical):
        """
            Save the image to a file. If vertical is true, rotate by 90 degrees.
        """
        if vertical:
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



def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option(
        "-a",
        dest="algorithm",
        default=[],
        type="choice",
        action="append",
        choices=[i.name for i in libsortvis.sortable.algorithms],
        help="Draw only a named algorithm."
    )
    parser.add_option(
        "-n",
        dest="numelements",
        default="20",
        type="int",
        help="Generate a random sorting sequence of length n"
    )
    parser.add_option(
        "-f",
        dest="readfile",
        help="Read data from file"
    )
    parser.add_option(
        "-o",
        dest="ofname",
        help="Output file name. Only usable when a single algorithm is being drawn.",
        default=""
    )
    parser.add_option(
        "-d",
        dest="dump",
        default=False,
        action="store_true",
        help="Dump sequence"
    )
    parser.add_option(
        "-x",
        dest="width",
        type="int",
        default=None,
        help="Image width"
    )
    parser.add_option(
        "-y",
        dest="height",
        type="int",
        default=None,
        help="Image height"
    )
    parser.add_option(
        "-l",
        dest="line",
        type="int",
        default=6,
        help="Total line width"
    )
    parser.add_option(
        "-b",
        dest="border",
        type="int",
        default=1,
        help="Border width"
    )
    parser.add_option(
        "-r",
        dest="rotate",
        default=False,
        action="store_true",
        help="Rotate images 90 degrees"
    )
    parser.add_option(
        "-i",
        dest="highlight",
        type="int",
        default=[],
        action="append",
        help="Highlight digit N (0-based). Can be passed muiltiple times."
    )
    options, args = parser.parse_args()
    if args:
        parser.error("Script takes no arguments.")
    if options.readfile:
        txt = file(options.readfile).read().split()
        lst = [int(i) for i in txt]
    else:
        lst = range(options.numelements)
        random.shuffle(lst)
    if options.highlight:
        if max(options.highlight) > (len(lst)-1):
            parser.error("Highlight element > than list length.")
    if options.dump:
        for i in lst:
            print i,

    if not options.height:
        options.height = (options.line + options.border + 5) * len(lst)

    if not options.width:
        options.width = int(options.height * 3)

    ldrawer = PathDrawer(
        options.width,
        options.height,
        options.line,
        options.border,
        options.highlight,
    )
    if options.algorithm:
        selected = [i.lower() for i in options.algorithm]

    if options.algorithm:
        todraw = [i for i in libsortvis.sortable.algorithms if i.name in options.algorithm]
    else:
        todraw = [i for i in libsortvis.sortable.algorithms]

    if options.ofname and len(todraw) > 1:
        parser.error("Cannot specify output file name when drawing more than one algorithm.")

    for i in todraw:
        a = i()
        sortd = a(lst)
        ldrawer.draw(sortd, a.name, options.ofname or a.name, options.rotate)


if __name__ == "__main__":
    main()
