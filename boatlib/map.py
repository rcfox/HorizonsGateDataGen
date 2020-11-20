import math
import functools

from .data import Parser

from dijkstar import Graph
import pyclipper
from PIL import Image, ImageDraw, ImageFont

def dist_sq(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1])**2

def mostly_blue(color):
    r, g, b, _ = color
    if white(color):
        return False
    return (b > r and b > g)

def white(color):
    r, g, b, _ = color
    return (r > 140 and g > 140 and b > 140)


class Map:
    def __init__(self, map_image_filename, location_data_filename, zone_data_filename):
        self.img = Image.open(map_image_filename)
        self.img_orig = self.img.copy()
        self.scale_x = 1
        self.scale_y = 1

        self.font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', size=22)

        with open(location_data_filename) as f:
            self.location_data = Parser.parse(f.read())

        with open(zone_data_filename) as f:
            self.zone_data = Parser.parse(f.read())

    def scale(self, x, y):
        w, h = self.img.size
        self.img = self.img.resize((int(w * x), int(h * y)))
        self.scale_x *= x
        self.scale_y *= y

    def scale_point(self, point):
        x, y = point
        return (x * self.scale_x, y * self.scale_y)

    def draw_point(self, point, text=None, color=(255, 0, 0, 255)):
        draw = ImageDraw.Draw(self.img)
        x, y = point
        size = 1
        draw.ellipse((self.scale_point((x-(size+1), y-(size+1))), self.scale_point((x+(size+1),y+(size+1)))), fill=(0, 0, 0, 255))
        draw.ellipse((self.scale_point((x-size, y-size)), self.scale_point((x+size,y+size))), fill=color)

        if text:
            text_width, text_height = self.font.getsize(text)
            text_x, text_y = self.scale_point((x, y))
            draw.text((text_x - text_width / 2, text_y), text, font=self.font, stroke_fill=(0, 0, 0, 255), stroke_width=1)

    def draw_line(self, line, color=(255, 0, 0, 255), draw_points=False):
        p1, p2 = line
        p1_ = self.scale_point(p1)
        p2_ = self.scale_point(p2)
        draw = ImageDraw.Draw(self.img)
        draw.line((p1_, p2_), fill=color, width=1)

        if draw_points:
            self.draw_point(p1, color=color)
            self.draw_point(p2, color=color)

    def show(self):
        self.img.show()

    def save(self, filename):
        self.img.save(filename)

    def get_lake_points(self):
        for record in self.zone_data:
            if 'ID' in record and 'lakeMarker' in record['ID']:
                yield (record['x'], record['y'])

        for p in [(590,460), (600, 460), (200, 242)]:
            yield p

    def get_waypoint_lines(self):
        for record in self.zone_data:
            if 'ID' in record and 'waypoint' in record['ID']:
                if 'specialX' in record:
                    yield ((record['x'], record['y']), (record['specialX'], record['specialY']))


    def parse_coasts(self):
        point_coords = set()

        img = self.img_orig

        # Don't try to parse the edges of the map
        inset = 10
        for x in range(inset, img.width - inset):
            for y in range(inset, img.height - inset):

                middle = img.getpixel((x, y))

                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if not (dx == 0 and dy == 0):
                            p = img.getpixel((x+dx, y+dy))

                            if mostly_blue(p) and (white(middle) or not mostly_blue(middle)):
                                point_coords.add((x,y))

        return point_coords

    def get_coast_lines(self):
        point_coords = self.parse_coats()
        lines = []
        for x, y in point_coords:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if not (dx == 0 and dy == 0):
                        x2 = x + dx
                        y2 = y + dy
                        if (x2, y2) in point_coords:
                            lines.append(((x, y), (x2, y2)))
        return lines

    def filter_invalid_points(self, points):
        lake_points = list(self.get_lake_points())
        def near_lake_points(point):
            for p in lake_points:
                if dist_sq(point, p) < 144:
                    return True
            return False

        return [p for p in points if not near_lake_points(p)]

    def scale_lines(self, lines, scale):
        scaled_lines = []
        for p1, p2 in lines:
            x1, y1 = p1
            x2, y2 = p2
            scaled_lines.append(((x1 * scale, y1 * scale), (x2 * scale, y2 * scale)))
        return scaled_lines

    def get_coast_polygons(self):
        # Turns all of the disjoint lines into polygons, but I need to expand for it to work.
        pco = pyclipper.PyclipperOffset()
        for line in self.parse_coasts():
            path = list(line) + [(line[0][0]+1, line[0][1])]
            pco.AddPath(path, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
        solution = pco.Execute2(1)

        # Undo the expansion.
        pco = pyclipper.PyclipperOffset()
        for polygon in solution.Childs:
            pco.AddPath(polygon.Contour, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
        solution2 = pco.Execute2(-1)

        # I only want the external polygons, this gets rid of lakes and such.
        for polygon2 in solution2.Childs:
            yield polygon2.Contour

    def expand_islands(self, expansion):
        pco = pyclipper.PyclipperOffset()
        for poly in self.get_coast_polygons():
            pco.AddPath(poly, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)

        return pyclipper.CleanPolygons(pco.Execute(expansion))

        # for i, poly in enumerate(polygons):
        #     for p1, p2 in zip(poly, poly[1:] + poly[:1]):
        #         if mostly_blue(self.img_orig.getpixel(tuple(p1))) and mostly_blue(self.img_orig.getpixel(tuple(p2))):
        #             yield (tuple(p1), tuple(p2))

    def polygon_as_lines(self, polygon, scale=1):
        for p1, p2 in zip(polygon, polygon[1:] + polygon[:1]):
            x1, y1 = p1
            x2, y2 = p2
            yield ((x1 / scale, y1 / scale), (x2 / scale, y2 / scale))


    @functools.lru_cache
    def find_rivers(self):
        img = self.img_orig
        points = []

        # Don't try to parse the edges of the map
        inset = 10
        for x in range(inset, img.width - inset):
            for y in range(inset, img.height - inset):

                middle = img.getpixel((x, y))
                if not mostly_blue(middle):
                    continue

                count = 1
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if not (dx == 0 and dy == 0):
                            p = img.getpixel((x+dx, y+dy))
                            if mostly_blue(p):
                                count += 1

                c = min(255, 20 * max(0, 256 // count - 256 // 49))
                if c > 100:
                    points.append((x, y))

        return points

    def create_water_graph(self):
        img = self.img_orig
        graph = Graph(undirected=True)

        inset = 10
        for y in range(inset, img.height - inset):
            for x in range(inset, img.width - inset):
                p1 = (x, y)

                if not mostly_blue(img.getpixel(p1)):
                    continue

                #for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if not (dx == 0 and dy == 0):
                            p2 = (x + dx, y + dy)
                            if mostly_blue(img.getpixel(p2)):
                                graph.add_edge(p1, p2, 5 * dist_sq(p1, p2))

        for x, y in self.find_rivers():
            p1 = (x, y)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if not (dx == 0 and dy == 0):
                        p2 = (x + dx, y + dy)
                        if mostly_blue(img.getpixel(p2)):
                            graph.add_edge(p1, p2, dist_sq(p1, p2))
                        #for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:


        return graph
