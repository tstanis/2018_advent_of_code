import string

def react(polymer):
    i = 0
    n = 0
    while i < len(polymer) - 1:
        c1 = polymer[i]
        c2 = polymer[i+1]
        if c1 != c2 and (c1.lower() == c2 or c1 == c2.lower()):
            #print c1 + " " + c2
            # react
            polymer = polymer[:i] + polymer[(i+2):]
            #print polymer
            n += 1
        else:
            i += 1
    return polymer, n
            
def react_completely(polymer):
    n = 1
    while n:
        polymer, n = react(polymer.strip())
    return polymer

with open('day_5.txt', 'r') as fp:
    n = 1
    best_c = None
    best_n = 10000000
    for polymer in fp:
        polymer = polymer.strip()
        for c in string.ascii_uppercase:
            removed = polymer.replace(c, "").replace(c.lower(), "")
            out = react_completely(removed)
            print c + " " + str(len(out))
            if len(out) < best_n:
                best_n = len(out)
                best_c = c
    print best_c
    print best_n
