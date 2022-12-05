import time
import timeit
import imu
import serial
from playsound import playsound

time_initialize_paper = 3 # 3 seconds to collect initial data
time_initialize_rock = 3 # 3 seconds to collect initial data
time_initialize_IMU = 3 # 3 seconds to collect initial data
thres_param = [0.4, 0.4, 0.7, 0.7, 0.5] # pinky, ring, middle, index, thumb

def calibration_paper(arduino):
    paper = [0, 0, 0, 0, 0]
    count = 0
    print("open your hand.")
    playsound("sound/beepsound.mp3",True)
    playsound("sound/openhand.mp3", True)
    time.sleep(1.5)
    start_time_1 = timeit.default_timer()
    while timeit.default_timer() < start_time_1 + time_initialize_paper:
        arduino.write(b'a')
        line = arduino.readline().decode()
        line = str(line)
        str_list = line.split(",")
        strains = map(int,str_list)
        res = list(strains)

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
    playsound("sound/beepsound.mp3", True)
    playsound("sound/closehand.mp3", True)
    time.sleep(1.5)
    start_time_2 = timeit.default_timer()
    while timeit.default_timer() < start_time_2 + time_initialize_rock:
        arduino.write(b'a')
        line = arduino.readline().decode()
        line = str(line)
        str_list = line.split(",")
        strains = map(int, str_list)
        res = list(strains)

        for i in range(5):
            rock[i] = rock[i] + res[i]
            if i == 4: count = count + 1
    print("rocks")
    for i in range(5):
        rock[i] = rock[i] / count
        print(rock[i])
    print()

    return rock

def calibration_IMU():
    # serial = imu.ser_init()
    # rl = imu.ReadLine(serial)
    serIMU = serial.Serial('COM5', 921600, timeout=0.2)
    initial_rpy =[0, 0, 0]
    count = 0
    print("Hold still. This is your initial roll pitch yaw.")
    playsound("sound/beepsound.mp3", True)
    playsound("sound/imu.mp3", True)
    time.sleep(1.5)
    start_time_3 = timeit.default_timer()
    serIMU.reset_input_buffer() # clears imu serial buffer
    while timeit.default_timer() < start_time_3 + time_initialize_IMU:
        res = serIMU.readline().decode('utf8').split(',')
        res = [datum for datum in res if datum]
        res.pop(0)
        # res = rl.readline_muchbetter()
        # res = imu.raw_parsing(res)
        # only acknowledge data from imu if 5 arrive
        if len(res) == 4:
            res = [float(datum) for datum in res]
            [roll, pitch, yaw] = [res[0], res[1], res[2]]
            initial_rpy[0] = initial_rpy[0] + roll
            initial_rpy[1] = initial_rpy[1] + pitch
            initial_rpy[2] = initial_rpy[2] + yaw
            count = count + 1
        else:
            continue

    initial_rpy[0] = initial_rpy[0] / count
    initial_rpy[1] = initial_rpy[1] / count
    initial_rpy[2] = initial_rpy[2] / count
    print("IMU")
    print("roll : ",end="")
    print(initial_rpy[0])
    print("pitch : ", end="")
    print(initial_rpy[1])
    print("yaw : ", end="")
    print(initial_rpy[2])
    print("")
    # serial.close()
    serIMU.close()
    return initial_rpy

def rpy(serIMU, initial_rpy):
    # serIMU = serial.Serial('COM5', 921600, timeout=0.2)
    count = 0

    serIMU.reset_input_buffer()  # clears imu serial buffer
    while True:
        res = serIMU.readline().decode('utf8').split(',')
        res = [datum for datum in res if datum]
        res.pop(0)
        # res = rl.readline_muchbetter()
        # res = imu.raw_parsing(res)
        # only acknowledge data from imu if 5 arrive

        if len(res) == 4:
            res = [float(datum) for datum in res]
            return [res[0], res[1], res[2]]
