import itertools

def compute_power(x, y, sn):
    return (((((x + 10) * y) + sn) * (x + 10) % 1000) / 100) - 5

patch = {}
def compute_grid(x, y, sz_x, sz_y, sn):
    total = 0
    if patch.has_key((x, y, sz_x, sz_y, sn)):
        return patch[(x, y, sz_x, sz_y, sn)]
    elif sz_x > 2 and sz_y > 2:
        half_x = sz_x / 2
        half_y = sz_y / 2
        total += compute_grid(x, y, half_x, half_y, sn)
        total += compute_grid(x + half_x, y, half_x, half_y, sn)
        total += compute_grid(x, y + half_y, half_x, half_y, sn)
        total += compute_grid(x + half_x, y + half_y, half_x, half_y, sn)
        # compute the last bit around the edges:
        if sz_x % 2 == 1:
            if sz_x > 1:
                total += compute_power(x, y + sz_y -1, half_x, 1, sn)
                total += compute_power(x + half_x, y + sz_y -1, sz_x / 2, 1, sn)

            for i in range(0, sz_x):
                total += compute_power(x + i, y + sz_y - 1, sn)
        if sz_y % 2 == 1:
            for j in range(0, sz_y - 1):
                total += compute_power(x + sz_x - 1, y + j, sn)
    else:
        for i in range(0, sz_x):
            for j in range(0, sz_y):
                total += compute_power(x + i, y + j, sn)
    patch[(x, y, sz_x, sz_y, sn)] = total
    return total

def find_best_grid(sz, sn):
    best = 0
    best_x = None
    best_y = None
    for x in range(0, 300 - sz):
        for y in range(0, 300 - sz):
            total = compute_grid(x, y, sz, sn)
            if total > best:
                best = total
                best_x = x
                best_y = y
    return best, best_x, best_y

sn = 1133
overall_best = 0
overall_best_x = None
overall_best_y = None
overall_best_sz = None
for sz in range(1, 300):
    print sz
    value, x, y = find_best_grid(sz, sn)
    if value > overall_best:
        overall_best = value
        overall_best_x = x
        overall_best_y = y
        overall_best_sz = sz
print overall_best_x
print overall_best_y
print overall_best_sz
print overall_best

