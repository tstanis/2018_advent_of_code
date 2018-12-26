# depth = 510
# target = (10, 10)
depth = 3198
target = (12,757)
board_sz = (target[0] * 2, target[1] * 2)
type = {0: '.', 1: '=', 2: "|"}
passage = {'.': 'ct', '=': 'cn', '|': 'tn'}

def errosion(gi):
    return (gi + depth) % 20183

def get_risk(e):
    return e % 3
    
def get_type(e):
    return type[e % 3]

def gen_board(sz):
    board = []
    for y in range(0, sz[1] + 1):
        board.append([{} for x in range(0, sz[0] + 1)])
        board[y][0]['errosion'] = errosion(48271 * y)

    for x in range(0, sz[0] + 1):
        board[0][x]['errosion'] = errosion(16807 * x)

    def fill(x, y):
        board[y][x]['errosion'] = errosion(board[y-1][x]['errosion'] * board[y][x-1]['errosion'])

    for i in range(1, max(sz[0] + 1, sz[1] + 1)):
        if i < sz[1] + 1:
            for x in range(i, sz[0] + 1):
                fill(x, i)
        if i < sz[0] + 1:
            for y in range(i, sz[1] + 1):
                fill(i, y)
    board[0][0]['errosion'] = 0
    board[target[1]][target[0]]['errosion'] = 1
    return board

def print_board(board):
    for row in board:
        print("".join(map(get_type, map(lambda x: x['errosion'], row))))

def calc_risk(board):
    return sum([sum(map(lambda x: get_risk(x['errosion']), row)) for row in board])

def best_time():
    best = None
    for path, value in theboard[target[1]][target[0]].items():
        if path in 'cnt':
            time = value['time']
            full_path = value['path'].copy()
            if path != 't':
                time += 7
                full_path += ['t']
            if best == None or time < best['time']:
                best = {'time': time, 'path': full_path}
    return best

def calc_best_path(board, sz, target):
    def ok_tool(cur, dest):
        return cur  in passage[get_type(dest['errosion'])]

    def visit(x, y, open_queue):
        for key, value in board[y][x].items():
            if key in "cnt":
                time = value['time']
                path = value['path']
                for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    destx = x + dir[0]
                    desty = y + dir[1]
                    if destx < 0 or desty < 0 or desty > sz[1] or destx > sz[0]:
                        continue
                    dest = board[desty][destx]
                    for next_tool in "cnt":
                        if not ok_tool(next_tool, dest):
                            continue
                        next_time = time
                        next_path = path.copy()
                        if next_tool != key:
                            next_time += 7
                            next_path.append(next_tool)
                        next_time += 1
                        next_path.append(dir)
                        #if next_tool in dest:
                            #print("Prev: " + str(dest[next_tool]))
                        if next_tool in dest and dest[next_tool]['time'] <= next_time:
                            continue
                        dest[next_tool] = {'time': next_time, 'path': next_path}
                        #print("path: " + str((x, y)) + " to " + str((destx, desty)) + " : " + next_tool + str((next_time, next_path)))
                        if (destx, desty) not in open_queue:
                            open_queue.add((destx, desty, next_time))

    board[0][0]['t'] = {'time':0, 'path':[]}
    #board[0][0]['c'] = {'time':7, 'path':['c']}
    #board[0][0]['n'] = {'time':7, 'path':['n']}
    open_queue = set()
    open_queue.add((0,0,0))
    i = 0
    while open_queue:
        x, y, time = open_queue.pop()
        cur_best = best_time()
        if not cur_best or time < cur_best['time']:
            visit(x, y, open_queue)

        i += 1
        if i % 1000 == 0:
            cur_best_time = best_time()
            thetime = "None" if not cur_best_time else cur_best_time['time']
            print(str(i) + " " + str(len(open_queue)) + " best: " + str(thetime))

theboard = gen_board(board_sz)
print_board(theboard)
print("Risk: " + str(calc_risk(theboard)))
calc_best_path(theboard, board_sz, target)
best = best_time()
print("Best: " + str(best) + " best: " + str(best_time()))
print(str(sum(map(lambda x: 7 if not isinstance(x, tuple) else 1, best['path']))))