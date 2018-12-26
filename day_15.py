from copy import copy, deepcopy
board = []
empty_board = []
elves = []
goblins = []

def set_board(board, x, y, value):
    board[y][x] = value

def clear_board(board, x, y):
    board[y][x] = empty_board[y][x]

def board_adj_empty(board, x, y):
    return filter(lambda x: board[x[1]][x[0]] == ".", adj_cells(board, x, y))

def adj_cells(board, x, y):
    cells = []
    cells.append((x, y - 1))
    cells.append((x - 1, y))
    cells.append((x + 1, y))
    cells.append((x, y + 1))
    return cells

def cell_distance(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def sort_cells(cells):
    return sorted(cells, key=lambda x: (x[1], x[0]))

class Mob:
    def __init__(self, x, y, kind, attack_power):
        self.x = x
        self.y = y
        self.hp = 200
        self.kind = kind
        self.attack_power = attack_power
        self.alive = True
    
    def sort_key(self):
        return (self.y, self.x)

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def distance_to_cell(self, cell):
        return abs(self.x - cell[0]) + abs(self.y - cell[1])

    def get_char(self):
        return "E" if self.kind == "elf" else "G"

    def get_hp_str(self):
        return self.get_char() + "(" + str(self.hp) + ")"

    def best_cell(self, cell1, cell2):
        return (cell_distance(cell1, cell2), cell1[1], cell1[0])

    def is_adj(self, cell):
        return self.distance_to_cell(cell) <= 1

    def search_path_dynamic(self, board, target_cell):
        if self.is_adj(target_cell):
            return [target_cell], 0
        distance_board = deepcopy(board)
        set_board(distance_board, target_cell[0], target_cell[1], "0")
        next_cell = [target_cell]
        found_path = False
        found_min_value = None
        while next_cell:
            cell = next_cell.pop(0)
            value = int(distance_board[cell[1]][cell[0]])
            if found_path and found_min_value < value:
                break
            alladj = board_adj_empty(distance_board, cell[0], cell[1])
            for adj in alladj:
                if self.is_adj(adj):
                    found_path = True
                    found_min_value = value
                set_board(distance_board, adj[0], adj[1], str(value + 1))
                next_cell.append(adj)
        
        if found_path:
            my_adj_cells = adj_cells(distance_board, self.x, self.y)
            num_cells = filter(lambda x: distance_board[x[1]][x[0]].isnumeric(), my_adj_cells)
            best = sorted(num_cells, key=lambda x: (int(distance_board[x[1]][x[0]]), x[1], x[0]))
            return [best[0]], int(distance_board[best[0][1]][best[0][0]])
        else:
            return None, None

    def find_path(self, board, target_cell):
        path, dist = self.search_path_dynamic(board, target_cell)
        return path[0] if path else None

    def move_to(self, cell, board):
        clear_board(board, self.x, self.y)
        self.x = cell[0]
        self.y = cell[1]
        set_board(board, self.x, self.y, 'G' if self.kind == 'goblin' else 'E')

    def adjacent_empty(self, board):
        return board_adj_empty(board, self.x, self.y)

    def enemies(self, elves, goblins):
        return elves if self.kind == 'goblin' else goblins

    def find_target(self, board, elves, goblins):
        closest_enemies = sorted(self.enemies(elves, goblins), key = lambda x: (x.distance_to(self), x.y, x.x))
        cells_src = {}
        cells_dist = {}
        cells = []
        for enemy in closest_enemies:
            if enemy.distance_to(self) == 1:
                # already adjacent
                return enemy, None
            alladjacent = enemy.adjacent_empty(board)
            for adjacent in alladjacent:
                path, dist = self.search_path_dynamic(board, adjacent)
                if path:
                    if adjacent not in cells_dist or cells_dist[adjacent] > dist:
                        cells_src[adjacent] = enemy
                        cells_dist[adjacent] = dist
                        cells.append(adjacent)

        if not cells:
            return None, None
        sorted_cells = sorted(cells, key=lambda x:(cells_dist[x], x[1], x[0]))
        return (cells_src[sorted_cells[0]], sorted_cells[0])

    def attack(self, board, elves, goblins):
        adj_enemies = list(filter(lambda x: x.distance_to(self) == 1, self.enemies(elves, goblins)))
        if adj_enemies:
            best_target = sorted(adj_enemies, key=lambda x: (x.hp, x.y, x.x))[0]
            best_target.take_damage(self.attack_power)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            clear_board(board, self.x, self.y)
            (elves if self.kind == 'elf' else goblins).remove(self)

    def __repr__(self):
        return self.kind + " (" + str(self.x) + "," + str(self.y) + ": " + str(self.hp) + ")"

def get_mob_string(board, i):
    mobs = sorted(filter(lambda x: x.y == i, goblins + elves), key=lambda x: x.x)
    return ", ".join(map(lambda x: x.get_hp_str(), mobs))
    
def print_board(board):
    for i in range(0, len(board)):
        row = board[i]
        print("".join(row) + "   " + get_mob_string(board, i))

def tick():
    sorted_mobs = sorted(elves + goblins, key = lambda x: x.sort_key())
    for mob in sorted_mobs:
        if not elves or not goblins:
            return False
        if not mob.alive:
            continue
        target, cell = mob.find_target(board, elves, goblins)
        if not target:
            continue
        if mob.distance_to(target) > 1:
            next_move = mob.find_path(board, cell)
            if next_move:
                mob.move_to(next_move, board)
        mob.attack(board, elves, goblins)
    #print_board(board)
    return True

def solve(filename, elf_power):
    print("Solving: " + filename)
    global board
    global empty_board
    global elves
    global goblins
    board = []
    empty_board = []
    elves = []
    goblins = []
    with open(filename, 'r') as fp:
        y = 0
        for line in fp:
            line = line.strip()
            board.append(list(line))
            empty_board.append(line.replace('G', '.').replace('E', '.'))
            for x in range(0, len(line)):
                if line[x] == 'G':
                    goblins.append(Mob(x, y, 'goblin', 3))
                elif line[x] == 'E':
                    elves.append(Mob(x, y, 'elf', elf_power))
            y += 1
    
    num_starting_elves = len(elves)
    #print_board(board)
    
    num_complete = 0
    for i in range(0, 500):
        complete = tick()
        if complete:
            num_complete += 1
        if not complete or not elves or not goblins:
            print("Battle complete!")
            winners = elves if elves else goblins
            hp_remaining = sum(map(lambda x: x.hp, winners))
            print("HP Remainig: " + str(hp_remaining))
            print("Round Complete: " + str(num_complete))
            print("Answer= " + str(num_complete * hp_remaining))
            return num_starting_elves - len(elves)
            break

solve('day_15_test.txt', 3)
solve('day_15_test2.txt', 3)
solve('day_15_test3.txt', 3)
solve('day_15_test4.txt', 3)
solve('day_15_test5.txt', 3)
solve('day_15_test6.txt', 3)
solve('day_15_test7.txt', 3)
for atk in range(3, 50):
    dead_elves = solve('day_15.txt', atk)
    if dead_elves == 0:
        break
    print("atk: " + str(atk) + " dead elves: " + str(dead_elves))