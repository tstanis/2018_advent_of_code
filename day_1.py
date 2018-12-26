with open('day_1.txt', 'r') as fp:  
    total_sum = 0
    for line in fp:
        if line[0] == "+":
            number = int(line[1:])
        else:
            number = int(line)
        print number
        total_sum += number
    print total_sum
        