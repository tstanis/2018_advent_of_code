generation = [3, 7]
elf1_recipe = 0
elf2_recipe = 1

def get_str(i, v):
    if i == elf1_recipe: 
        return '(' + str(v) + ')' 
    elif i == elf2_recipe: 
        return '[' + str(v) + ']' 
    else: 
        return ' ' + str(v) + ' '

stop_size = 556061
stop_string = [5, 5, 6, 0, 6, 1]
found_in_a_row = 0
max_g = 100000000
for g in range(0, max_g):
    #print "".join([get_str(i, v) for i, v in enumerate(generation)])

    total = generation[elf1_recipe] + generation[elf2_recipe]
    digits = map(int, str(total))

    found = False
    foundIndex = 0
    for i in range(0, len(digits)):
        if stop_string[found_in_a_row] == digits[i]:
            found_in_a_row += 1
            if found_in_a_row == len(stop_string):
                found = True
                foundIndex = (len(generation) + i) - len(stop_string) + 1
                break
        else:
            found_in_a_row = 0 
    generation.extend(digits)  
    if found:
        #print "".join([get_str(i, v) for i, v in enumerate(generation)])
        print "FOUND AT " + str(foundIndex)
        break 
    elf1_moves = generation[elf1_recipe] + 1
    elf2_moves = generation[elf2_recipe] + 1
    elf1_recipe = (elf1_recipe + elf1_moves) % len(generation)
    elf2_recipe = (elf2_recipe + elf2_moves) % len(generation)
    if g == stop_size + 10:
        #print "".join([get_str(i, v) for i, v in enumerate(generation)])
        print "FINAL 10: " + "".join(map(str, generation[stop_size:stop_size+10]))

    if g % 100000 == 0:
        print str(g) + " " + str(float(g) / max_g)