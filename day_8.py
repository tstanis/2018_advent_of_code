data = []
with open('day_8.txt', 'r') as fp:
    for line in fp:
        data.extend(map(int, line.split()))

def parse_next(data, i):
    num_children = data[i]
    i += 1
    num_metadata = data[i]
    i += 1
    children = []
    for child in range(0, num_children):
        child, i = parse_next(data, i)
        children.append(child)
    metadata = data[i:i+num_metadata]
    return (children, metadata), i+num_metadata

def accum_metadata(node):
    accum = sum(node[1])
    for child in node[0]:
        accum += accum_metadata(child)
    return accum

def node_value(node):
    print node
    if not node[0]:
        return sum(node[1])
    total = 0
    for index in node[1]:
        if index > len(node[0]):
            continue
        total += node_value(node[0][index-1])
    return total
        
root, i = parse_next(data, 0)

print accum_metadata(root)
print node_value(root)