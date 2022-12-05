import time
import socket

import RPIservo
import functions
import switch
import move
import robotLight

switch.switchSetup()
switch.set_all_switch_off()

move.setup()

scGear = RPIservo.ServoCtrl()
scGear.moveInit()

P_sc = RPIservo.ServoCtrl()
P_sc.start()
T_sc = RPIservo.ServoCtrl()
T_sc.start()
H1_sc = RPIservo.ServoCtrl()
H1_sc.start()
H2_sc = RPIservo.ServoCtrl()
H2_sc.start()
G_sc = RPIservo.ServoCtrl()
G_sc.start()

init_pwm0 = scGear.initPos[0]
init_pwm1 = scGear.initPos[1]
init_pwm2 = scGear.initPos[2]
init_pwm3 = scGear.initPos[3]
init_pwm4 = scGear.initPos[4]


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.0.169', 24000))

RL = robotLight.RobotLight()
RL.start()
RL.breath(70,70,255)

speed_set = 100

while True:

    data,addr = sock.recvfrom(1)
    command = data.decode('utf-8')
    print(command)
    # print(addr)
    if command == 'A': # turn left
        move.move(speed_set, 'no', 'left', 0.5)
    elif command == 'D': # turn right
        move.move(speed_set, 'no', 'right', 0.5)
    elif command == 'W': # move forward
        move.move(speed_set, 'forward', 'no', 0.5)
    elif command == 'S': # move backward
        move.move(speed_set, 'backward', 'no', 0.5)
    elif command == 'I': # arm up
        H1_sc.singleServo(12, 1, 7)
    elif command == 'K': # arm down
        H1_sc.singleServo(12, -1, 7)
    elif command == 'J': # arm left turn
        P_sc.singleServo(14, -1, 5)
    elif command == 'L': # arm right turn
        P_sc.singleServo(14, 1, 5)
    elif command == 'P': # hand up
        H2_sc.singleServo(13, -1, 7)
    elif command == ';': # hand down
        H2_sc.singleServo(13, 1, 7)
    elif command == 'U': # grab
        G_sc.singleServo(15, 1, 3)
    elif command == 'O': # loose
        G_sc.singleServo(15, -1, 3)
    elif command == 'X': # kill
        move.motorStop()
        H1_sc.stopWiggle()
        H2_sc.stopWiggle()
        G_sc.stopWiggle()
        P_sc.stopWiggle()
        RL.set_all_switch_off()
        break
    else:
        move.motorStop()
        H1_sc.stopWiggle()
        H2_sc.stopWiggle()
        G_sc.stopWiggle()
        P_sc.stopWiggle()
    time.sleep(0.01)

time.sleep(1)

sock.close()