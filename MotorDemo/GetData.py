from Arduino.Arduino import Arduino
from Ceyear.RX2438 import Rx2438
from MotorDemo.DemoConfig import Config

import threading
import time
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TkAgg')

class SurfaceData:
    def __init__(self, args):
        self.args = args
        self.rx = Rx2438(self.args)
        self.arduino = Arduino(args)
        self.file_path = self.args.DataPath


    def getOne(self, start_angle, end_angle, speed, dirr=None):
        if dirr is None:
            dirr = self.args.default_dir
        # start
        self.arduino.Round(dirr, start_angle, self.args.default_speed)

        tnum1 = len(threading.enumerate())
        # get data
        seqs = []
        thread_round = threading.Thread(target=self.arduino.Round, args=(dirr, end_angle - start_angle, speed))
        thread_round.start()
        start = time.time()
        while len(threading.enumerate()) != tnum1:
            val = self.rx.getPower()
            now = time.time()
            seqs.append([val, now])
            time.sleep(speed * 2.0 / 1000000)

        print(len(seqs))

        # end
        if dirr == 'CW':
            self.arduino.Round('CCW', end_angle, self.args.default_speed)
        else:
            self.arduino.Round('CW', end_angle, self.args.default_speed)

        return seqs, start


    def _append_file(self, data):
        data.to_csv(self.file_path, mode='a', index=False, header=False)
        return

    def getBatch(self):
        pass


if __name__ == '__main__':
    config = Config()
    args = config.getArgs()
    data = SurfaceData(args)
    data, start = data.getOne(45, 150, 8000)
    print(data)
    x = []
    y = []
    for i in data:
        x.append(i[1]-start)
        y.append(float(i[0]))
    print(x)
    print(y)
    # for i in range(len(x)):
    plt.plot(x, y)

    plt.xlabel("t")
    plt.ylabel("dBm")
    # plt.grid()
    plt.show()