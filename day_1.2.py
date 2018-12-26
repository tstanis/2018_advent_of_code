
total_sum = 0
sums = {0: 1}
while 1:    
    with open('day_1.txt', 'r') as fp:  
        for line in fp:
            if line[0] == "+":
                number = int(line[1:])
            else:
                number = int(line)
            total_sum += number
            if sums.has_key(total_sum):
                print total_sum
                exit()
            else:
                sums[total_sum] = 1
        