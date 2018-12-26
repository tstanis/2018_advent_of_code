import sys 

sys.setrecursionlimit(10000)

dirs = {'N' : (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
opp = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

def parse_expr(expr):
    root = {'value': 'R', 'children': [], 'parent': None}
    node = root
    stack = []
    last_child = None
    for i in expr:
        if i == "^":
            node = root
        elif i == "$":
            return root
        elif i in "NSEW":
            new_node = {'value': i, 'children': [], 'parent': node}
            node['children'].append(new_node)
            node = new_node
            last_child = new_node
        elif i == "(":
            stack.append(node)
        elif i == "|":
            node = stack[-1]
            last_child = None
        elif i == ")":
            if last_child == None:
                node['children'].append({'value': "X", 'children': [], 'parent': node})
            node = stack.pop()
        else:
            print("waht?" + i)
            exit(1)

def traverse_extents(tree, current_pos, max_pos, min_pos):
    next_current_pos = current_pos
    next_max_pos = max_pos
    next_min_pos = min_pos
    if tree['value'] in "NSEW":
        dir = dirs[tree['value']]
        next_current_pos = (current_pos[0] + dir[0], current_pos[1] + dir[1])
        next_max_pos = (max(max_pos[0], current_pos[0]), max(max_pos[1], current_pos[1]))
        next_min_pos = (min(min_pos[0], current_pos[0]), min(min_pos[1], current_pos[1]))
    for child in tree['children']:
        next_max_pos, next_min_pos = traverse_extents(child, next_current_pos, next_max_pos, next_min_pos)
    return next_max_pos, next_min_pos

def get_extents(tree):
    max_pos, min_pos = traverse_extents(tree, (0, 0), (0, 0), (0, 0))
    print("etents " + str((max_pos, min_pos)))
    x = (max_pos[0] - min_pos[0]) + 1
    y = (max_pos[1] - min_pos[1]) + 1
    start_pos = (-min_pos[0], -min_pos[1])
    return x, y, start_pos

def traverse(tree):
    #print("Node: " + tree['value'] + " children: " + "".join(map(lambda x: x['value'], tree['children'])))
    for child in tree['children']:
        traverse(child)

def mark_board(tree, pos, board):
    for child in tree['children']:
        if child['value'] == 'X':
            continue
        board[pos[1]][pos[0]][child['value']] = 'd'
        dir = dirs[child['value']]
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        #print(str(new_pos))
        board[new_pos[1]][new_pos[0]][opp[child['value']]] = 'd'
        mark_board(child, new_pos, board)

def create_board(x, y, start_pos):
    board = []
    for i in range(0, y):
        board.append([{'N': 'w', 'S': 'w', 'W': 'w', 'E': 'w'} for x in range(0, x)])
    return board

def print_board(start_pos, board):
    for y in range(0, len(board)):
        def create_row_top(x):
            return "#" + ("-" if board[y][x]['N'] == 'd' else "#")
        def create_row_mid(x):
            return ("|" if board[y][x]['W'] == 'd' else "#") + ("." if x != start_pos[0] or y != start_pos[1] else "X")
        print("".join(map(create_row_top, range(0, len(board[y])))) + "#")
        print("".join(map(create_row_mid, range(0, len(board[y])))) + "#")
    print("".join(["##" for i in range(0, len(board[0]))]) + "#")

def search_path(pos, board, distances, cur_distance):
    if cur_distance < distances[pos[1]][pos[0]] or distances[pos[1]][pos[0]] == -1:
        distances[pos[1]][pos[0]] = cur_distance
    else:
        return
    
    cur_cell = board[pos[1]][pos[0]]
    for dir, door in cur_cell.items():
        if door == 'd':
            offset = dirs[dir]
            new_pos = (pos[0] + offset[0], pos[1] + offset[1])
            search_path(new_pos, board, distances, cur_distance + 1)
    

def find_max_room(start_pos, board):
    board_distances = []
    for x in range(0, len(board)):
        board_distances.append([-1 for x in range(0, len(board[x]))])
    search_path(start_pos, board, board_distances, 0)
    max_distance = max(map(lambda x: max(x), board_distances))
    num_over_1k = 0
    for a in board_distances:
        for b in a:
            if b >= 1000:
                num_over_1k += 1
    print("Max Distance: " + str(max_distance) + " Above 1k: " + str(num_over_1k))

with open('day_20.txt', 'r') as fp:
    for line in fp:
        tree = parse_expr(line)
        traverse(tree)
        x, y, start_pos = get_extents(tree)
        print(str((x, y, start_pos)))
        board = create_board(x, y, start_pos)
        print_board(start_pos, board)
        mark_board(tree, start_pos, board)
        print_board(start_pos, board)
        find_max_room(start_pos, board)
