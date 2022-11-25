import math
from djitellopy import tello

def signal(arduino, threshold, hand_number):
    arduino.write(b'a')
    line = arduino.readline().decode()
    line = str(line)
    str_list = line.split(",")
    map_obj = map(int, str_list)
    res = list(map_obj)

    indicator = 0
    if hand_number == 0:
        for i in range(5):
            if res[i] > threshold[i]: indicator = indicator + pow(2, i)
    elif hand_number == 1:
        for i in range(5):
            if res[i] > threshold[i]: indicator = indicator + pow(2,4-i)
    return bin(indicator)

def mode_change(signal):
    if signal == 0b10000 or signal == 0b00010 or signal == 0b10110: # drone
        change = True
    else:
        change = False
    return change

def mode_check(signal):
    if signal == 0b10000: # drone
        mode = 1
    if signal == 0b00010: # mobile robot
        mode = 2
    if signal == 0b10110: # manipulator
        mode = 3
    return mode

drone_obj = tello.Tello()

def control_drone(signal, signal_prev, drone_obj):
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30
    if signal == 0b00000:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b00001:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b00010:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b00011:
        [lr, fb, ud, yv] = [-speed, 0, 0, 0]
        [lr, fb, ud, yv] = [speed, 0, 0, 0]
    elif signal == 0b00100:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b00101:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b00110:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
        if signal_prev != 0b00110:
            drone_obj.flip_forward()
    elif signal == 0b00111:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01000:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01001:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01010:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01011:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01100:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01101:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01110:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b01111:
        [lr, fb, ud, yv] = [0, 0, speed, 0]
        [lr, fb, ud, yv] = [0, 0, -speed, 0]
    elif signal == 0b10000:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b10001:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b10010:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b10011:
        [lr, fb, ud, yv] = [0, speed, 0, 0]
    elif signal == 0b10100:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b10101:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b10110:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b10111:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11000:
        [lr, fb, ud, yv] = [0, 0, 0, -speed]
        [lr, fb, ud, yv] = [0, 0, 0, speed]
    elif signal == 0b11001:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11010:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11011:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11100:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11101:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11110:
        [lr, fb, ud, yv] = [0, 0, 0, 0]
    elif signal == 0b11111:
        [lr, fb, ud, yv] = [0, -speed, 0, 0]

    drone_obj.send_rc_control(lr, fb, ud, yv)

def print_signal(number):
    if number != 0b0:
        str_of_signal = str(bin(number))
        message = ""
        digits = math.floor(math.log2(number))
        for i in range(4 - digits):
            message = message + "0"
        message = message + str_of_signal[2:]
        print(message)
    else:
        print("00000")
