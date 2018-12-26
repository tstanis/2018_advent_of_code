from collections import defaultdict
import itertools

coverage = defaultdict(int)
claims = []
with open('day_3.txt', 'r') as fp:
    for line in fp:
        parts = line.split()
        id = parts[0]
        location = parts[2]
        dim = parts[3]
        x,y = location.split(",")
        x = int(x)
        y = int(y.split(':')[0])
        dim_x, dim_y = map(int, dim.split("x"))
        claims.append((x, y, dim_x, dim_y, id))
        for loc in itertools.product(range(x, x+dim_x), range(y, y+dim_y)):
            coverage[loc] += 1

print len([i for i, x in enumerate(coverage.iterkeys()) if coverage[x] > 1])

for claim in claims:
    x,y,dim_x,dim_y,id = claim
    all_ok = True
    for loc in itertools.product(range(x, x+dim_x), range(y, y+dim_y)):
        if coverage[loc] != 1:
            all_ok = False
    if all_ok:
        print id
