# %%
import serial, time
import numpy as np
import matplotlib.pyplot as plt


data = np.array([])
mv_avg = 30
time_thr = 0.004
min_angle_diff = 0.02
id = 0
r = 1
p = 2
y = 3
ay = 5
az = 6
WIN = True
USE_YAW = True

fig = plt.figure()
ax = plt.axes(xlim=(0,50), ylim=(-150,150))
line = ax.plot([],[], lw=2)
max_points = 50
line = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float64)*np.nan, lw=2)


class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline_muchbetter(self):
        self.s.reset_input_buffer()
        while self.s.read()=='\n':
            pass
        return self.s.readline()

    def readline(self):
        i = self.buf.find(b'\n')
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b'\n')

            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)


def raw_parsing(_raw):
    _parsed = _raw.decode().split(',')
    return _parsed


def ser_init():
    if WIN:
        _ser = serial.Serial(port='COM5', baudrate=921600) ######### Change Com port
    else:
        _ser = serial.Serial(port='/dev/ttyUSB0', baudrate=921600)
    _ser.close()
    print("serial closed")
    time.sleep(0.3)
    _ser.open()
    print("serial opened")
    time.sleep(0.3)
    return _ser


def main():
    ser = ser_init()
    rl = ReadLine(ser)
    # ser.write(b'<sog1>')
    # # ser.write(b'<soa2>')
    #ser.write(b'<sof1>')
    #time.sleep(2)
    # ser.write(b'<06sid00>')
    # ser.write(b'<00sid06>')
    #time.sleep(3)
    single = True
    start = time.perf_counter()

    while (True):
        res = rl.readline()
        res = raw_parsing(res)
        roll, pitch, yaw = (float(res[1]), float(res[2]), float(res[3]))
        print(roll, pitch, yaw)
        # print(res, len(res))
        if single:
            single = False
            start = time.perf_counter()
    end = time.perf_counter()

    print(end - start)
    ser.close()
    print("Serial Closed and end")

if __name__ == "__main__":
    main()