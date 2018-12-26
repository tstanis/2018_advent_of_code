import re
import math
from blist import blist
import sys 

sys.setrecursionlimit(40000)

board = []
min_x = math.inf
max_x = 0
min_y = math.inf
max_y = 0
columns = blist([])
rules = []
with open('day_17.txt', 'r') as fp:
    for line in fp:
        h,start,end = list(map(int, re.findall(r'\d+', line)))
        rules.append((line.startswith("y"), h, start, end))
        if line.startswith("y"):
            max_y = max(h, max_y)
            min_y = min(h, min_y)
            min_x = min(start, min_x)
            max_x = max(end, max_x)
        else:
            min_x = min(h, min_x)
            max_x = max(h, max_x)
            max_y = max(end, max_y)
            min_y = min(start, min_y)

for x in range(min_x, max_x + 1):
    columns.append(blist(["." for y in range(0, max_y + 1)]))

for rule in rules:
    starts_with_y, h, start, end = rule
    if starts_with_y:
        for x in range(start, end+1):
            columns[x - min_x][h] = "#"
    else:
        for y in range(start, end+1):
            #print(str((h, y)))
            columns[h - min_x][y] = "#"

columns[500 - min_x][0] = "+"

def print_board():
    for y in range(0, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            #print(str((x,y)))
            row.append(columns[x - min_x][y])
        print("".join(row))

def fill_all_water(x, y, visited):
    if y >= max_y:
        return True
    spill = False
    if columns[x-min_x][y+1] == ".":
        columns[x-min_x][y+1] = "w"
        spill = fill_all_water(x, y+1, visited)
        if spill:
            columns[x-min_x][y+1] = "|"
    elif columns[x-min_x][y+1] == "|":
        columns[x-min_x][y+1] = "|"
        spill = True
    if not spill:
        if x > (min_x - 1):
            if columns[x-min_x - 1][y] == ".":
                columns[x-min_x-1][y] = "|" if spill else "w"
                this_spill = fill_all_water(x-1, y, visited)
                if this_spill:
                    columns[x-min_x-1][y] = "|"
                spill |= this_spill
            elif columns[x-min_x - 1][y] == "|":
                spill = True
        if x < max_x:
            if columns[x-min_x + 1][y] == ".":
                columns[x-min_x+1][y] = "|" if spill else "w"
                this_spill = fill_all_water(x+1, y, visited)
                if this_spill:
                    columns[x-min_x+1][y] = "|"
                    left = x - 1
                    # fill in any cells to the left that should have been spill cells
                    while left > min_x and columns[left-min_x][y] == "w":
                        columns[left-min_x][y] = "|"
                        left -= 1
                spill |= this_spill
            elif columns[x-min_x + 1][y] == "|":
                spill = True
    return spill

print_board()

fill_all_water(500, 0, set())
print_board()
num_cells = 0
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if columns[x-min_x][y] == 'w' or columns[x-min_x][y] == '|':
            num_cells += 1
print("Num Cells: " + str(num_cells))

num_cells = 0
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if columns[x-min_x][y] == 'w':
            num_cells += 1
print("Num Stable Cells: " + str(num_cells))