from collections import defaultdict

ids = []
with open('day_2.txt', 'r') as fp:
    for line in fp:
        ids.append(line.strip())

for i in range(0, len(ids)):
    for j in range (i, len(ids)):
        first = ids[i]
        second = ids[j]
        num_diff = 0
        common = []
        for c in range(0, len(first)):
            if first[c] != second[c]:
                num_diff += 1
            else:
                common.append(first[c])
        if num_diff == 1:
            # found it!
            print first + " : " + second
            print "".join(common)
            exit()
            