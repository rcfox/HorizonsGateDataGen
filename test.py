import sys
from boatlib.map import Map, dist_sq

img = 'Content/Data/ZoneData/eral.png'
locations = 'Content/SystemSaves/defaultLocations.txt'
zones = 'Content/Data/ZoneData/eral.txt'

m = Map(img, locations, zones)

# for polygon in m.get_coast_polygons():
#     for line in m.polygon_as_lines(polygon):
#         m.draw_line(line)

waypoints = set()
for polygon in m.expand_islands(4):
    for line in m.polygon_as_lines(polygon):
        p1, p2 = line
        waypoints.add(p1)
        waypoints.add(p2)
        m.draw_line(line, color=(255, 0, 255, 255), draw_points=True)

for line in m.get_waypoint_lines():
     m.draw_line(line, color=(255, 255, 0, 255), draw_points=True)

m.scale(2, 2)
m.show()
