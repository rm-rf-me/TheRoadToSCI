from HengYangGuangXue.LZP3 import LZP3
from Ceyear.RX2438 import Rx2438
from config import Config

import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas
import random
import tqdm

mpl.use('TkAgg')

class GetData():
    def __init__(self, args):
        self.args = args
        self.debugPan = args.debugPan

        # if self.debugPan is True:
        self.rx = Rx2438(args=args)
        self.pan = LZP3()

    def init_pan(self, acc=5, dec=5, v=5):
        self.pan.init(acc, dec, v)

    # angle正数为顺时针，负数为逆时针
    def get_series_rel(self, end_a, delay=1, stride=2, block=0, show=0):

        note = input("描述这组数据：")
        data = {
            'time': [],
            'angle': [],
            'value': [],
            note: []
        }

        neg = 0
        if end_a < 0:
            neg = 1

        while 1:
            if self.debugPan:
                val = random.random()
            else:
                val = self.rx.getPower()

            now = time.time()
            angle = self.pan.get_p()
            print(now, angle, val)

            if block:
                input("回车继续：")
            data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
            data['angle'].append(angle)
            data['value'].append(float(val))
            data[note].append(' ')

            if (neg and end_a >= 0) or (not neg and end_a <= 0):
                break
            if neg:
                self.pan.p_rel(-stride)
            else:
                self.pan.p_rel(stride)
            pos = -1
            tmp = -2
            while 1:
                if tmp == pos:
                    break
                tmp = pos
                pos = self.pan.get_p()

                time.sleep(0.1)

            time.sleep(delay)

            if neg:
                end_a += stride
            else:
                end_a -= stride

        if show:
            plt.clf()
            plt.plot(data['angle'], data['value'])
            plt.xlabel('angle')
            plt.ylabel('dBm')
            plt.show()

        path = input("需要保存请起名，不保存输n:")
        if path != 'n':
            df = pandas.DataFrame(data)
            df.to_excel('./data/' + str(time.time()).split('.')[0]+'-'+path+'.xlsx')

        return data

    def goback(self, end_a, delay=0.3, stride=2, block=0, show=0):
        self.get_series_rel(end_a, delay, stride, block, show)
        self.get_series_rel(-end_a, delay, stride, block, show)

if __name__ == '__main__':
    config = Config()
    args = config.getArgs()
    haha = GetData(args)
    haha.init_pan()

    haha.goback(-108, show=1)