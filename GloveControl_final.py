# glove - strain *****, IMU ***
# 1 - drone control
# 2 - mobile robot control
# 3 - manipulator

import time
import serial
import calibrate
import glove
import imu
import socket
from djitellopy import tello
import subprocess
# parameters
thres_param = [0.4, 0.4, 0.6, 0.7, 0.5]   # pinky, ring, middle, index, thumb
roll_1 = -45
roll_2 = 45
port = 'COM11'   # arduino port
hand = 1   # left - 1, right - 0
me = tello.Tello()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
arduino = serial.Serial(port, 115200, timeout=1)
arduino.reset_input_buffer()
if arduino.readable():
    print(str(arduino.readline().decode()), end='')
time.sleep(1)

try:
    arduino.write(b'a')
    line = arduino.readline().decode()
    line = str(line)
    print(line)   # print "connected"

    paper = calibrate.calibration_paper(arduino)
    time.sleep(2)
    rock = calibrate.calibration_rock(arduino)
    time.sleep(2)

    print("calculate thresholds")
    thres = [1, 1, 1, 1, 1]
    for i in range(5):
        thres[i] = rock[i] * thres_param[i] + paper[i] * (1 - thres_param[i])
        print(thres[i])
    initial_rpy = calibrate.calibration_IMU()
    print("calibration complete\n")

    # dump one line
    glove.strain(arduino, thres, hand)
    indicator_prev = 0
    rpy_prev = [0, 0, 0]
    serial_imu = imu.ser_init()   # reopen imu serial

    control_mode = 75
    change_mode = 75

    print("START CONTROL")

    while True:
        indicator = glove.strain(arduino, thres, hand)
        rpy = calibrate.rpy(serial_imu, initial_rpy)
        print(format(indicator, '05b'), rpy)

        # check if we are changing modes
        if glove.mode_transfer(indicator, indicator_prev) == True:
            change_mode = glove.mode_check(indicator)
            print("waiting for mode input", end="")
            while change_mode != 10 and change_mode != 20 and change_mode != 30:
                indicator = glove.strain(arduino, thres, hand)
                change_mode = glove.mode_check(indicator)
                print(".", end="")
                time.sleep(0.5)

        # change_mode = glove.mode_check(indicator)
        if change_mode == 10 and control_mode != 1:   # from raspberry pi to drone
            output = subprocess.check_output("netsh wlan connect name=TELLO-F0ADF7")
            print("connecting", end="")
            line_count = 0
            while line_count < 20:
                output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                wifi_info = output.decode('cp949')
                lines = wifi_info.splitlines()
                line_count = len(lines)
                time.sleep(0.2)
                print(".", end="")
            print("")

            output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
            wifi_info = output.decode('cp949')
            lines = wifi_info.splitlines()
            line_index = 0
            if len(lines) < 20:
                print("no wifi connection")
            else:
                for i in range(len(lines)):
                    line_index = lines[i + 1].find('SSID')
                    if line_index != -1:
                        break

                wifi_line = lines[i + 1]
                index = wifi_line.find(':')
                print(index)
                print("connected to TELLO wifi")

            # me = tello.Tello()
            # print("creating drone object")
            me.connect()
            print(str(me.get_battery())+"%")
            time.sleep(0.1)
            me.takeoff()
            print("drone takeoff")
            print("wait for drone logs to appear on prompt")
            control_mode = 1

        elif change_mode == 20:   # from drone to raspberry pi
            if control_mode == 3:
                control_mode = 2
            elif control_mode == 1:
                print("disconnecting drone")
                # me.land()
                me.end()

                output = subprocess.check_output("netsh wlan connect name=SRBL5G")
                print("connecting to SRBL5G", end="")
                line_count = 0
                while line_count < 20:
                    output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                    wifi_info = output.decode('cp949')
                    lines = wifi_info.splitlines()
                    line_count = len(lines)
                    time.sleep(0.2)
                    print(".", end="")
                print("")
                output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                wifi_info = output.decode('cp949')
                lines = wifi_info.splitlines()
                line_index = 0
                if len(lines) < 20:
                    print("no wifi connection")
                else:
                    for i in range(len(lines)):
                        line_index = lines[i + 1].find('SSID')
                        if line_index != -1:
                            break
                    wifi_line = lines[i + 1]
                    index = wifi_line.find(':')
                    print(wifi_line[index + 2:])

                # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                control_mode = 2
            elif control_mode == 75:
                output = subprocess.check_output("netsh wlan connect name=SRBL5G")
                print("connecting to SRBL5G", end="")
                line_count = 0
                while line_count < 20:
                    output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                    wifi_info = output.decode('cp949')
                    lines = wifi_info.splitlines()
                    line_count = len(lines)
                    time.sleep(0.2)
                    print(".", end="")
                print("")
                output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                wifi_info = output.decode('cp949')
                lines = wifi_info.splitlines()
                line_index = 0
                if len(lines) < 20:
                    print("no wifi connection")
                else:
                    for i in range(len(lines)):
                        line_index = lines[i + 1].find('SSID')
                        if line_index != -1:
                            break
                    wifi_line = lines[i + 1]
                    index = wifi_line.find(':')
                    print(wifi_line[index + 2:])
                control_mode = 2

        elif change_mode == 30:
            if control_mode == 2:
                control_mode = 3
            elif control_mode == 1:
                print("disconnecting drone")
                # me.land()

                me.end()

                output = subprocess.check_output("netsh wlan connect name=SRBL5G")
                print("connecting to SRBL5G", end="")
                line_count = 0
                while line_count < 20:
                    output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                    wifi_info = output.decode('cp949')
                    lines = wifi_info.splitlines()
                    line_count = len(lines)
                    time.sleep(0.2)
                    print(".", end="")
                print("")
                output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                wifi_info = output.decode('cp949')
                lines = wifi_info.splitlines()
                line_index = 0
                if len(lines) < 20:
                    print("no wifi connection")
                else:
                    for i in range(len(lines)):
                        line_index = lines[i + 1].find('SSID')
                        if line_index != -1:
                            break
                    wifi_line = lines[i + 1]
                    index = wifi_line.find(':')
                    print(wifi_line[index + 2:])

                # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                control_mode = 3
            elif control_mode == 75:
                output = subprocess.check_output("netsh wlan connect name=SRBL5G")
                print("connecting to SRBL5G", end="")
                line_count = 0
                while line_count < 20:
                    output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                    wifi_info = output.decode('cp949')
                    lines = wifi_info.splitlines()
                    line_count = len(lines)
                    time.sleep(0.2)
                    print(".", end="")
                print("")
                output = subprocess.check_output("netsh wlan show interface name=\"Wi-Fi\" ^| findstr \"SSID\"")
                wifi_info = output.decode('cp949')
                lines = wifi_info.splitlines()
                line_index = 0
                if len(lines) < 20:
                    print("no wifi connection")
                else:
                    for i in range(len(lines)):
                        line_index = lines[i + 1].find('SSID')
                        if line_index != -1:
                            break
                    wifi_line = lines[i + 1]
                    index = wifi_line.find(':')
                    print(wifi_line[index + 2:])
                control_mode = 3

        if control_mode == 75:
            print("test mode")
            time.sleep(0.1)

        if control_mode == 1:
            lr, fb, ud, yv = 0, 0, 0, 0
            speed = 40
            signal = indicator
            if signal == 0b00000:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00001:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00010:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00011:
                if rpy[0] < roll_1:
                    [lr, fb, ud, yv] = [0, 0, 0, speed]
                elif rpy[0] > roll_2:
                    [lr, fb, ud, yv] = [0, 0, 0, -speed]
                else:
                    [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00100:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00101:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00110:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b00111:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01000:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01001:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01010:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01011:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01100:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                if indicator_prev != 0b01100:
                    me.flip_forward()
            elif signal == 0b01101:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01110:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b01111:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10000:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10001:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10010:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10011:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10100:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10101:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10110:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b10111:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11000:
                if rpy[0] < roll_1:
                    [lr, fb, ud, yv] = [speed, 0, 0, 0]
                elif rpy[0] > roll_2:
                    [lr, fb, ud, yv] = [-speed, 0, 0, 0]
                else:
                    [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11001:
                [lr, fb, ud, yv] = [0, speed, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11010:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11011:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11100:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11101:
                [lr, fb, ud, yv] = [0, 0, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11110:
                if rpy[0] < roll_1:
                    ud = -speed
                elif rpy[0] > roll_2:
                    ud = speed
                else:
                    ud = 0
                print(lr, fb, ud, yv)
                me.send_rc_control(lr, fb, ud, yv)
            elif signal == 0b11111:
                [lr, fb, ud, yv] = [0, -speed, 0, 0]
                me.send_rc_control(lr, fb, ud, yv)
            time.sleep(0.1)

        elif control_mode == 2:
            signal = indicator
            if signal == 0b11000:
                if rpy[0] < roll_1:
                    a = "A"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                elif rpy[0] > roll_2:
                    a = "D"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                else:
                    a = "Z"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            elif signal == 0b11001:
                a = "W"
                sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            elif signal == 0b11111:
                a = "S"
                sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            else:
                a = "Z"
                sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))

            time.sleep(0.05)

        elif control_mode == 3:
            signal = indicator
            if signal == 0b11110:
                if rpy[0] < roll_1:
                    a = "K"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                elif rpy[0] > roll_2:
                    a = "I"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                else:
                    a = "Z"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            elif signal == 0b11000:
                if rpy[0] < roll_1:
                    a = "J"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                elif rpy[0] > roll_2:
                    a = "L"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                else:
                    a = "Z"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            elif signal == 0b11100:
                if rpy[0] < roll_1:
                    a = ";"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                elif rpy[0] > roll_2:
                    a = "P"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
                else:
                    a = "Z"
                    sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            elif signal == 0b11111:
                a = "U"
                sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            elif signal == 0b01110:
                a = "O"
                sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))
            else:
                a = "Z"
                sock.sendto(a.encode('utf-8'), ('192.168.0.169', 24000))

            time.sleep(0.05)

        indicator_prev = indicator
        rpy_prev = rpy

except KeyboardInterrupt:
    sock.close()
    print("END ENTIRE SESSION")
