from djitellopy import tello
import time
import serial
import calibrate
import glove

# parameters
thres_param = [0.4, 0.4, 0.7, 0.7, 0.5] # pinky, ring, middle, index, thumb
port = 'COM11'
hand = 1 # left - 1, right - 0

# connect arduino serial
arduino = serial.Serial(port, 115200, timeout=1)
arduino.reset_input_buffer()
if arduino.readable():
    print(str(arduino.readline().decode()),end='')
time.sleep(1)

# create Tello object
me = tello.Tello()
# me.connect()
# print(str(me.get_battery())+"%")
# time.sleep(0.1)

try:
    while True:
        arduino.write(b'a')
        line = arduino.readline().decode()
        line = str(line)
        print(line)

        # initialize (hand open)
        paper = calibrate.calibration_paper(arduino)
        time.sleep(2)
        # initialize (hand closed)
        rock = calibrate.calibration_rock(arduino)
        time.sleep(2)
        print("calculate thresholds")
        thres = [1, 1, 1, 1, 1]
        for i in range(5):
            thres[i] = rock[i] * thres_param[i] + paper[i] * (1 - thres_param[i])
            print(thres[i])
        print("calibration complete\n")

        control_mode = 2
        # 1 - drone
        # 2 - mobile robot
        # 3 - manipulator

        # drone takeoff
        # me.takeoff()
        # print("wait")
        # time.sleep(5)

        # start rasptank

        # dump one line
        glove.signal(arduino, thres, hand)
        indicator_prev = 0

        print("START CONTROL")

        while True:

            indicator = glove.signal(arduino, thres, hand)
            glove.print_signal(int(indicator,2))
            change_mode = glove.mode_change(indicator)

            if(change_mode == True):
                # change mode
                control_mode = glove.mode_check(indicator)

            if control_mode == 1:
                glove.control_drone(indicator,indicator_prev, me)
                time.sleep(0.1)

            elif control_mode == 2:
                pass
            elif control_mode == 3:
                pass

            indicator_prev = indicator


except KeyboardInterrupt:
    print("END ENTIRE SESSION")
    # me.land()
    # me.end()
    arduino.close()
    time.sleep(1)




