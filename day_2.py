from collections import defaultdict

with open('day_2.txt', 'r') as fp:
    num_twos = 0
    num_threes = 0
    for line in fp:
        counts = defaultdict(int)
        has_two = False
        has_three = False
        for character in line:
            counts[character] += 1
        for key in counts.iterkeys():
            if counts[key] == 2:
                has_two = True
            if counts[key] == 3:
                has_three = True
        if has_two:
            num_twos += 1
        if has_three:
            num_threes += 1
    print "Num Twos: " + str(num_twos)
    print "Num Threes: " + str(num_threes)
    print "Checksum: " + str(num_twos * num_threes)