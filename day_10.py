import sys
import math

points = []
with open('day_10.txt', 'r') as fp:
    for line in fp:
        line = line.strip()
        parts = line.split("<")
        x = int(parts[1].split(',')[0])
        y = int(parts[1].split(',')[1].split('>')[0])
        vel_x = int(parts[2].split(',')[0])
        vel_y = int(parts[2].split(',')[1].split('>')[0])
        points.append((x, y, vel_x, vel_y))

cur_points = []
for point in points:
    cur_points.append((point[0], point[1]))

def move_points(cur_points):
    return list(map(lambda z: (z[0][0] + z[1][2], z[0][1] + z[1][3]), zip(cur_points, points)))

def get_dim(cur_points):
    max_x, max_y, min_x, min_y = -math.inf, -math.inf, math.inf, math.inf
    for point in cur_points:
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])
        min_x = min(min_x, point[0])
        min_y = min(min_y, point[1])
    return min_x, max_x, min_y, max_y

def print_points(cur_points):
    min_x, max_x, min_y, max_y = get_dim(cur_points)
    board = []
    for i in range(0, abs(max_x - min_x) + 1):
        board.append(["." for _ in range(min_y, max_y + 1)])
    for point in cur_points:
        board[point[0] - min_x][point[1] - min_y] = "#"
    for y in range(0, abs(min_y - max_y) + 1):
        for x in range(0, abs(min_x - max_x) + 1):
            sys.stdout.write(board[x][y])
        sys.stdout.write('\n')

def size_of_points(cur_points):
    min_x, max_x, min_y, max_y = get_dim(cur_points)
    return abs(max_x - min_x) + abs(max_y - min_y)

size_decreasing = True
last_size = math.inf
prev_points = None
seconds = 0
while size_decreasing:
    seconds += 1
    prev_points = cur_points
    cur_points = move_points(cur_points)
    size = size_of_points(cur_points)
    size_decreasing = last_size > size
    last_size = size
print_points(prev_points)
print(seconds - 1)
print(size_of_points(prev_points))
