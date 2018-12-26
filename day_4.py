from collections import defaultdict

guard_sleep = defaultdict(int)
common_minute = {}
last_guard_id = None
sleep_time = 0
with open('day_4_sorted.txt', 'r') as fp:
    for line in fp:
        parts = line.split()
        date_parts = parts[0].split('-')
        month = date_parts[1]
        day = date_parts[2]
        time = parts[1].split(':')
        hour = time[0]
        minute = time[1].split(']')[0]
        what_happened = parts[2]
        if what_happened == 'Guard':
            guard_id = parts[3]
            last_guard_id = guard_id
        elif what_happened == 'falls':
            sleep_time = int(minute)
        elif what_happened == 'wakes':
            total_sleep = (int(minute) - sleep_time)
            guard_sleep[last_guard_id] += total_sleep
            hour_dict = defaultdict(int)
            if common_minute.has_key(last_guard_id):
                hour_dict = common_minute[last_guard_id]
            else:
                common_minute[last_guard_id] = hour_dict
            for i in range(sleep_time, int(minute)):
                hour_dict[i] += 1


guard = max(guard_sleep.iterkeys(), key=lambda key: guard_sleep[key])
print guard
minute = max(common_minute[guard].iterkeys(), key=lambda key: common_minute[guard][key])
print minute
print int(guard[1:]) * minute

max_minute = 0
max_times = 0 
max_guard = None
for guard in guard_sleep.iterkeys():
    for minute in common_minute[guard].iterkeys():
        if common_minute[guard][minute] > max_times:
            max_times = common_minute[guard][minute]
            max_minute = minute
            max_guard = guard

print "max_minute: " + str(max_minute)
print "max_times: " + str(max_times)
print "max_guard: " + str(max_guard)
print int(max_guard[1:]) * max_minute