import time
import timeit

time_initialize_paper = 3 # 3 seconds to collect initial data
time_initialize_rock = 3 # 3 seconds to collect initial data
thres_param = [0.4, 0.4, 0.7, 0.7, 0.5] # pinky, ring, middle, index, thumb

def calibration_paper(arduino):
    paper = [0, 0, 0, 0, 0]
    count = 0
    print("open your hand.")
    time.sleep(1.5)
    start_time_1 = timeit.default_timer()
    while timeit.default_timer() < start_time_1 + time_initialize_paper:
        arduino.write(b'a')
        line = arduino.readline().decode()
        line = str(line)
        str_list = line.split(",")
        map_obj = map(int, str_list)
        res = list(map_obj)

        for i in range(5):
            paper[i] = paper[i] + res[i]
            if i == 4: count = count + 1
    print("papers")
    for i in range(5):
        paper[i] = paper[i] / count
        print(paper[i])
    print()

    return paper

def calibration_rock(arduino):
    rock = [0, 0, 0, 0, 0]
    count = 0
    print("close your hand.")
    time.sleep(1.5)
    start_time_2 = timeit.default_timer()
    while timeit.default_timer() < start_time_2 + time_initialize_rock:
        arduino.write(b'a')
        line = arduino.readline().decode()
        line = str(line)
        str_list = line.split(",")
        map_obj = map(int, str_list)
        res = list(map_obj)

        for i in range(5):
            rock[i] = rock[i] + res[i]
            if i == 4: count = count + 1
    print("rocks")
    for i in range(5):
        rock[i] = rock[i] / count
        print(rock[i])
    print()

    return rock
