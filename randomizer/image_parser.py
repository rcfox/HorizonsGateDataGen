import pyclipper

def mostly_blue(color):
    r, g, b, _ = color
    if white(color):
        return False
    return (b > r and b > g)

def white(color):
    r, g, b, _ = color
    return (r > 140 and g > 140 and b > 140)

def near_lake_points(point, lake_points):
    for p in lake_points:
        if dist(point, p) < 12:
            return True
    return False

def parse_coasts(img, lake_points):
    points = []

    point_coords = set()

    lines = []

    # Don't try to parse the edges of the map
    inset = 10
    for x in range(inset, img.width - inset):
        for y in range(inset, img.height - inset):

            middle = img.getpixel((x, y))

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx != 0 and dy != 0:
                        p = img.getpixel((x+dx, y+dy))

                        if mostly_blue(p) and (white(middle) or not mostly_blue(middle)):
                            if not near_lake_points((x, y), lake_points):
                                points.append((x, y))
                                point_coords.add((x,y))

    for x, y in point_coords:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx != 0 and dy != 0:
                    x2 = x + dx
                    y2 = y + dy
                    if (x2, y2) in point_coords:
                        lines.append(((x, y), (x2, y2)))
                                
    return lines


def expand_islands(lines):
    pco = pyclipper.PyclipperOffset()
    for line in lines:
        path = list(line) + [(line[0][0]+1, line[0][1])]
        pco.AddPath(path, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
    return pyclipper.CleanPolygons(pco.Execute(7), 2.5)


def draw_islands(img, polygons):
    orig = img.copy()
    draw = ImageDraw.Draw(img)
    color = (255, 0, 0, 255)
    for i, poly in enumerate(polygons):
        for p1, p2 in zip(poly, poly[1:] + poly[:1]):
            if mostly_blue(orig.getpixel(tuple(p1))) and mostly_blue(orig.getpixel(tuple(p2))):
                line = (tuple(p1), tuple(p2))
                draw.line(line, fill=color, width=1)
                x, y = line[0]
                draw.ellipse(((x-3, y-3), (x+3,y+3)), fill=(0, 0, 0, 255))
                draw.ellipse(((x-2, y-2), (x+2,y+2)), fill=color)

    img.show()
