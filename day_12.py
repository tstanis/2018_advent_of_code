initial_state = None
rules = {}
with open('day_12.txt', 'r') as fp:
    for line in fp:
        if not initial_state:
            initial_state = line.split()[2]
        elif len(line) > 1:
            parts = line.split()
            rules[parts[0]] = parts[2]

print initial_state

print rules
prefix = "....."
state =  prefix + str(initial_state) + ".................."
index_offset = len(prefix)
segment_length = 5
generations = 100
def score(state):
    return sum(map(lambda a: a[1] if a[0] == "#" else 0, zip(state, range(-index_offset, len(state)))))

scores = [score(state)]
for g in range(0, generations):
    next_state = ".."
    for i in range(2, len(state) - segment_length):
        segment = state[i-2:i+(segment_length-2)]
        if rules.has_key(segment):
            next_state += rules[segment]
            if i == (len(state) - segment_length) - 1:
                next_state += "."
        else:
            next_state += "."
    next_state += "....."
    
    state = next_state
    scores.append(score(state))
    print state

print state

diffs = [scores[i+1]-scores[i] for i in range(len(scores)-1)]
for i in range(0, len(scores)-1):
    print str(i) + " " + str(scores[i]) + " " + str(diffs[i]) + " " + str(((i - 89) * 15) + 2047)

print (((50000000000-1) - 89) * 15) + 2047