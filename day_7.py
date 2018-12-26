from collections import defaultdict

nodes = {}

root_not_possible = {}
with open('day_7.txt', 'r') as fp:
    for line in fp:
        parts = line.split()
        before = parts[1]
        after = parts[7]
        node = (before, [after])
        if nodes.has_key(before):
            nodes[before][1].append(after)
        else:
            nodes[before] = node
        root_not_possible[after] = 1



roots = []
new_nodes = []
for node in nodes.iterkeys():
    if not root_not_possible.has_key(node):
        roots.append(node)
    for dest in nodes[node][1]:
        if not nodes.has_key(dest):
            new_nodes.append((dest, []))
for new_node in new_nodes:
    nodes[new_node[0]] = new_node

dependency = defaultdict(list)
for key, value in nodes.iteritems():
    for after in value[1]:
        dependency[after].append(key)

print "roots"
print roots
print "nodes"
print nodes
print dependency
open = map(lambda x: nodes[x][0], roots)
open.sort()
final_string = ''
visited = {}
started = {}
print "---"


def finish_node(node):
    visited[node[0]] = 1
    for next, deps in dependency.iteritems():
        if visited.has_key(next) or started.has_key(next):
            continue
        ok = True
        for dep in deps:
            if not visited.has_key(dep):
                ok = False
        if ok and next not in open:
            open.append(next)
        open.sort()

num_workers = 5
worker_tasks = []
time = 0
extra_latency = 60

while len(visited) < len(nodes):
    for task in worker_tasks:
        task[1] -= 1
    def test_item(task):
        if task[1] <= 0:
            finish_node(task[0])
            return False
        return True
    worker_tasks = filter(test_item, worker_tasks)
    while len(worker_tasks) < num_workers and open:
        # more work to do
        node = open.pop(0)
        node_name = node[0]
        latency = ord(node_name) - ord('A') + 1 + extra_latency
        worker_tasks.append([node_name, latency])
        started[node[0]] = 1

    print str(time) + " " + str(worker_tasks)
    time += 1

print final_string
print time - 1
