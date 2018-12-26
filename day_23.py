import re
import heapq

def distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

def num_in_range(coord):
    return len([x for x in nanobots if distance(x, coord) <= x[3]])

def get_extents(nanobots):
    maximums = [0, 0, 0]
    minimums = [0, 0, 0]
    for bot in nanobots:
        for i in range(0, 3):
            maximums[i] = max(maximums[i], bot[i])
            minimums[i] = min(minimums[i], bot[i])
    return (maximums[0], maximums[1], maximums[2]), (minimums[0], minimums[1], minimums[2])

def get_corners(cube):
    return [
        cube[0], cube[1],
        (cube[1][0], cube[0][1], cube[0][2]), 
        (cube[0][0], cube[1][1], cube[0][2]), 
        (cube[0][0], cube[0][1], cube[1][2]),
        (cube[1][0], cube[1][1], cube[0][2]),
        (cube[0][0], cube[1][1], cube[1][2]),
        (cube[1][0], cube[0][1], cube[1][2])]
    num_inside = 0

def get_cube_containment(cube, nanobots):
    corners = get_corners(cube)
    num_inside = 0
    for bot in nanobots:
        if bot[0] <= max(cube[0][0], cube[1][0]) and \
        bot[0] >= min(cube[0][0], cube[1][0]) and \
        bot[1] <= max(cube[0][1], cube[1][1]) and \
        bot[1] >= min(cube[0][1], cube[1][1]) and \
        bot[2] <= max(cube[0][2], cube[1][2]) and \
        bot[2] >= min(cube[0][2], cube[1][2]):
        # inside
            num_inside += 1
            continue
        for corner in corners:
            if distance(bot, corner) <= bot[3]:
                num_inside += 1
                break
    return num_inside

def get_center(cube):
    return (int((cube[0][0] + cube[1][0]) / 2), int((cube[0][1] + cube[1][1]) / 2), int((cube[0][2] + cube[1][2]) / 2))
    
def split_cube(orig_cube):
    cubes = []
    center = get_center(orig_cube)
    corners = get_corners(orig_cube)
    raw_cubes = [(center, x) for x in corners]
    out_cubes = []
    for cube in raw_cubes:
        out_cubes.append(((max(cube[0][0], cube[1][0]), max(cube[0][1], cube[1][1]), max(cube[0][2], cube[1][2])),
        (min(cube[0][0], cube[1][0]), min(cube[0][1], cube[1][1]), min(cube[0][2], cube[1][2]))))
    return out_cubes

def score_cubes(cubes, nanobots):
    return [((-get_cube_containment(cube, nanobots), area_of_cube(cube)), cube) for cube in cubes]

def area_of_cube(cube):
    return abs(1 + cube[0][0] - cube[1][0]) * abs(1 + cube[0][1] - cube[1][1]) * abs(1 + cube[0][2] - cube[1][2])

surrounds = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
nanobots = []
with open('day_23.txt', 'r') as fp:
    for line in fp:
        args = list(map(int, re.findall(r'-?\d+', line)))
        nanobots.append((args[0], args[1], args[2], args[3]))

strongest = max(nanobots, key=lambda x: x[3])
weakest = min(nanobots, key=lambda x: x[3])
in_range = [x for x in nanobots if distance(x, strongest) <= strongest[3]]
print("Num Bots: " + str(len(nanobots)))
print("Strongest: " + str(strongest))
print("Weakest: " + str(weakest))
print("Number In Range Of Strongest: " + str(len(in_range)))

extents = get_extents(nanobots)
print("Extents: " + str(extents))

cubes = split_cube(extents)
scores = score_cubes(cubes, nanobots)

queue = []
for score in scores:
    heapq.heappush(queue, score)

best_small = None
best_small_score = -1
while queue:
    score_tuple, cube = heapq.heappop(queue)
    score, area = score_tuple
    area = area_of_cube(cube)
    print("Next Cube: score=" + str(-score) + " sz=" + str(area) + " " + str(cube) + " queue=" + str(len(queue)))
    cubes = split_cube(cube)
    new_scores = score_cubes(cubes, nanobots)
    for new_score in new_scores:
        if new_score[0][1] > 8 and -new_score[0][0] >= best_small_score: #area
            heapq.heappush(queue, new_score)
        elif new_score[0][1] <= 8:
            if -new_score[0][0] > best_small_score:
                best_small = [new_score[1]]
                best_small_score = -new_score[0][0]
                print("new best " + str(new_score))
            elif -new_score[0][0] == best_small_score:
                best_small.append(new_score[1])

best_point = None
best_point_score = 0
print("Best Small Cube: " + str(best_small))
for cube in best_small:
    for x in range(cube[1][0] , cube[0][0] + 1):
        for y in range(cube[1][1], cube[0][1] + 1):
            for z in range(cube[1][2], cube[0][2] + 1):
                point = (x, y, z)
                score = num_in_range(point)
                if score > best_point_score:
                    best_point_score = score
                    best_point = [point]
                elif score == best_point_score:
                    best_point.append(point)
print("Best Points: " + str(best_point) + " score " + str(best_point_score))
print("Min: " + str(min([(distance(point, (0,0,0)), point) for point in best_point], key=lambda x:x[0])))
