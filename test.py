from collections import defaultdict
import sys
from boatlib.map import Map, dist_sq, mostly_blue
from dijkstar.algorithm import single_source_shortest_paths, extract_shortest_path_from_predecessor_list

img = 'Content/Data/ZoneData/eral.png'
locations = 'Content/SystemSaves/defaultLocations.txt'
zones = 'Content/Data/ZoneData/eral.txt'

m = Map(img, locations, zones)

# for p in m.parse_coasts():
#     m.img.putpixel(p, (255, 255, 0, 255))

# waypoints = set()
# for polygon in m.expand_islands(4):
#     for line in m.polygon_as_lines(polygon):
#         p1, p2 = line
#         waypoints.add(p1)
#         waypoints.add(p2)
#         m.draw_line(line, color=(255, 0, 255, 255), draw_points=True)

# for x in range(m.img.width):
#     for y in range(m.img.height):
#         p = (x, y)
#         if mostly_blue(m.img.getpixel(p)):
#             m.img.putpixel(p, (0, 0, 255, 255))
#         else:
#             m.img.putpixel(p, (0, 0, 0, 255))

# for p in m.find_rivers():
#     m.img.putpixel(p, (255, 0, 255, 255))

g = m.create_water_graph()
preds = single_source_shortest_paths(g, (20, 20))#(300, 300))

point_paths = defaultdict(list)

for n in m.find_rivers():
    if n in preds:
        path = extract_shortest_path_from_predecessor_list(preds, n)
        for p in path.nodes:
            point_paths[p].append(path.nodes)

longests = []
for point, paths in point_paths.items():
    paths.sort(key=len, reverse=True)
    longests.append(paths[0])

def simplify_path(path):
    simplified = [path[0]]
    x1, y1 = path[0]
    x2, y2 = path[1]
    if x2 == x1:
        slope = float('inf')
    else:
        slope = (y2 - y1) / (x2 - x1)
    for i, p in enumerate(path[2:], start=2):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        if x2 == x1:
            slope2 = float('inf')
        else:
            slope2 = (y2 - y1) / (x2 - x1)
        if slope2 != slope:
            simplified.append(path[i-1])
        slope = slope2
    simplified.append(path[-1])
    return simplified

def path_as_lines(path):
    for i, _ in enumerate(path[1:], start=1):
        yield path[i-1], path[i]

for path in longests[:1]:
    for line in path_as_lines(simplify_path(path)):
        m.draw_line(line)
m.scale(6, 6)            
###m.img.putpixel(p, (255, 0, 255, 255))
        
#m.save('1.png')
m.show()
# for p in m.get_lake_points():
#     m.draw_point(p, color=(255, 0, 0, 255))

# for line in m.get_waypoint_lines():
#      m.draw_line(line, color=(255, 255, 0, 255), draw_points=True)

#m.find_rivers()

#m.show()
