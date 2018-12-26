track = []
carts = []
orig_track = []

with open('day_13.txt', 'r') as fp:
    for line in fp:
        for i in range(0, len(line)):
            c = line[i]
            if c == ">" or c == "<" or c == "^" or c == "v":
                carts.append((i, len(track), "l"))
        track.append(list(line.strip('\n')))
        orig_track.append(list(line.strip('\n').replace('<', '-') \
            .replace('>', '-').replace('v', '|').replace('^', '|')))

def print_track(track):
    
    for n in range(0, len(track)):
        i = track[n]
        print "{:02d}".format(n) + "".join(i)
    
print_track(track)
print_track(orig_track)

transitions = {
    ('\\', '>') : 'v',
    ('\\', '^') : '<',
    ('\\', '<') : '^',
    ('\\', 'v') : '>',
    ('/', '^') : '>',
    ('/', '<') : 'v',
    ('/', '>') : '^',
    ('/', 'v') : '<',
    ('l', '>') : '^',
    ('r', '>') : 'v',
    ('l', '^') : '<',
    ('r', '^') : '>',
    ('l', 'v') : '>',
    ('r', 'v') : '<',
    ('l', '<') : 'v',
    ('r', '<') : '^',
}

next_turn_map = {
    'l' : 'c',
    'c' : 'r',
    'r' : 'l'
}
crash = False
def clean_track(cart):
    track[cart[1]][cart[0]] = orig_track[cart[1]][cart[0]]
    
for g in range(0, 100000):
    new_carts = []
    carts = sorted(carts, key = lambda x: (x[1], x[0]))
    print carts

    if len(carts) == 1:
        print "Only 1 Cart Remaining"
        exit(0)
    crashed_carts = []
    for cart_num in range(0, len(carts)):
        if cart_num in crashed_carts:
            crashed_carts.remove(cart_num)
            continue
        cart = carts[cart_num]
        char = track[cart[1]][cart[0]]
        if char == '>':
            next_pos = (cart[0] + 1, cart[1])
        elif char == '<':
            next_pos = (cart[0] - 1, cart[1])
        elif char == 'v':
            next_pos = (cart[0], cart[1] + 1)
        else:
            next_pos = (cart[0], cart[1] - 1)
        
        if char == '|' or char == '-':
            print_track(track)
            print("BAD CHAR! " + str(next_pos) + " " + str(cart)) + " g= "+ str(g)
            print carts
            exit(1)

        if next_pos[0] < 0 or next_pos[1] < 0:
            print_track(track)
            print("BAD POS! " + str(next_pos) + " " + str(cart)) + " g= "+ str(g)
            print carts
            exit(1)

        crashed = False
        for cart_num_other in range(0, len(new_carts)):
            new_cart = new_carts[cart_num_other]
            if next_pos[0] == new_cart[0] and next_pos[1] == new_cart[1]:
                crashed = True
                clean_track(new_cart)
                new_carts.pop(cart_num_other)
                print "Crash at " + str(next_pos[0]) + "," + str(next_pos[1]) + " g= "+ str(g)
                break
        for cart_num_other in range(cart_num + 1, len(carts)):
            new_cart = carts[cart_num_other]
            if next_pos[0] == new_cart[0] and next_pos[1] == new_cart[1]:
                crashed = True
                clean_track(new_cart)
                crashed_carts.append(cart_num_other)
                print "Crash at " + str(next_pos[0]) + "," + str(next_pos[1]) + " g= "+ str(g)
                break

        clean_track(cart)

        if crashed:
            continue

        track_char = track[next_pos[1]][next_pos[0]]
        
        next_turn = cart[2]
        if transitions.has_key((track_char, char)):
            next_char = transitions[(track_char, char)]
        elif track_char == '+':
            if transitions.has_key((next_turn, char)):
                next_char = transitions[(next_turn, char)]
            else:
                next_char = char
            next_turn = next_turn_map[next_turn]
        else:
            next_char = char

        track[next_pos[1]][next_pos[0]] = next_char
        new_carts.append((next_pos[0], next_pos[1], next_turn))
    carts = new_carts