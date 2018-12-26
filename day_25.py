import re

points = []

def distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2]) + abs(x[3] - y[3])

with open('day_25.txt', 'r') as fp:
    for line in fp:
        numbers = list(map(int, re.findall(r'-?\d+', line)))
        points.append((numbers[0], numbers[1], numbers[2], numbers[3]))


constellations = {}
next_constellation_id = 0
for point in points:
    cur_constellation_id = None
    if point in constellations:
        cur_constellation_id = constellations[point]
    else:
        cur_constellation_id = next_constellation_id
        next_constellation_id += 1
        constellations[point] = cur_constellation_id
    for other_point in points:
        if other_point == point:
            continue
        dist = distance(point, other_point)
        if dist <= 3:
            if other_point in constellations:
                other_constellation_id = constellations[other_point]
                if other_constellation_id != cur_constellation_id:
                    constellations.update((k,other_constellation_id) for k in constellations if constellations[k] == cur_constellation_id)
                    cur_constellation_id = other_constellation_id
            else:
                constellations[other_point] = cur_constellation_id
        
print(points)
print(constellations)
print("Num Constellations: " + str(len(set(constellations.values()))))
