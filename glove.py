
from playsound import playsound

def strain(arduino, threshold, hand_number):
    arduino.write(b'a')
    line = arduino.readline().decode()
    line = str(line)
    str_list = line.split(",")
    # strains = map(int, str_list[0:5])
    strains = map(int, str_list)
    res = list(strains)

    indicator = 0
    if hand_number == 0:
        for i in range(5):
            if res[i] > threshold[i]: indicator = indicator + pow(2, i)
    elif hand_number == 1:
        for i in range(5):
            if res[i] > threshold[i]: indicator = indicator + pow(2,4-i)

    return indicator

def mode_check(signal):

    if signal == 0b00100:
        print("drone control")
        playsound("sound/beepsound.mp3", True)
        playsound("sound/controlmode1.mp3", True)
        change = 10
        return change
    elif signal == 0b01000:
        print("mobile robot control")
        playsound("sound/beepsound.mp3", True)
        playsound("sound/controlmode2.mp3", True)
        change = 20
        return change
    elif signal == 0b01101:
        print("manipulator control")
        playsound("sound/beepsound.mp3", True)
        playsound("sound/controlmode3.mp3", True)
        change = 30
        return change

def mode_transfer(signal, signal_prev):
    if signal == 0b10101 and signal_prev == 0b10101:
        print("CHANGING MODE")
        return True
    else:
        return False

