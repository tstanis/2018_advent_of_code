from collections import defaultdict

coords = []
max_x = 0
max_y = 0
with open('day_6.txt', 'r') as fp:
    for line in fp:
        x, y = map(int, line.split(', '))
        coords.append((x, y))
        max_x = max(max_x, x)
        max_y = max(max_y, y)

print max_x
print max_y

closest = []
for x in range(0, max_x + 1):
    row = []
    closest.append(row)
    for y in range(0, max_y + 1):
        min_pt = None
        min_dist = 1000000
        for i in range(0, len(coords)):
            point = coords[i]
            dist = abs(point[0] - x)
            dist += abs(point[1] - y)
            if dist == 0:
                min_pt = i
                min_dist = 0
            elif dist < min_dist:
                min_pt = i
                min_dist = dist
            elif dist == min_dist:
                min_pt = "."
                min_dist = dist
        row.append(min_pt)

rows = []
for i in range(0, len(closest)):
    for j in range(0, len(closest[i])):
        if len(rows) < j + 1:
            rows.append([])
        rows[j].append(closest[i][j])

for row in rows:
    print "".join(map(str, row))

infinite = set()
# find the infinite
for edge in closest[0]:
    infinite.add(edge)
for edge in closest[len(closest) - 1]:
    infinite.add(edge)
for edge in closest:
    infinite.add(edge[0])
for edge in closest:
    infinite.add(edge[len(edge) - 1])

counts = defaultdict(int)
for i in range(0, len(closest)):
    for j in range(0, len(closest[i])):
        point = closest[i][j]
        if point not in infinite:
            counts[point] += 1

print infinite
print counts
print max(counts.iteritems(), key=lambda x: x[1])

max_distance = 10000

in_region = []
for x in range(0, max_x + 1):
    for y in range(0, max_y + 1):
        accum = 0
        for point in coords:
            accum += abs(point[0] - x)
            accum += abs(point[1] - y)
        if accum < max_distance:
            in_region.append((x, y))
print in_region
print len(in_region)
