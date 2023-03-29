from Device_HengYangGuangXue.LZP3 import LZP3
from Device_Ceyear.RX2438 import Rx2438
from utils.cmdIO import *

import matplotlib.pyplot as plt
import matplotlib as mpl

import pandas

mpl.use('TkAgg')


class SampleBase():
    def __init__(self, args):
        self.args = args
        self.debugPan = args.debugPan

        # if self.debugPan is True:
        self.rx = Rx2438(args=args)
        self.pan = LZP3(args=args)

        io_rx_test(self.args, self.rx)

        self.pan.init_without_adc()

        self.freq, self.power = io_set_tx(self.args)
        self.rx.setFreq((self.freq))

    def init_pan(self, acc=5.0, dec=5.0, v=5.0):
        self.pan.init(acc, dec, v)

    def _use_config_dict(self, args):
        pass

    def show_pic(self, x, y, xlabel='angle', ylabel='dBm', show_pic=True):
        # plt.clf()
        fig = plt.figure()
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if show_pic:
            plt.show()

        return fig

    def get_file_name(self, path):
        # name = './data/' + str(time.time()).split('.')[0] + '-F' + str(self.freq) + '-P' + str(self.power) + path
        name = './data/' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '_' + path
        return name

    def save_file(self, data, fig, save_pic, data_type, path=None):
        # 数据保存
        if path is None:
            path = io_get_file_name(self.args)
        if path != 'n' or path != 'N':
            # 默认路径为XXXSampling_/data/，命名格式为 时间戳-频率-功率-命令.对应格式
            name = self.get_file_name(path)

            if save_pic:
                fig.savefig(name + '.jpg')

            df = pandas.DataFrame(data)
            while 1:
                if data_type == 'xlsx':
                    df.to_excel(name + '.xlsx')
                    break
                elif data_type == 'csv':
                    df.to_csv(name + '.csv')
                    break
                elif data_type == 'txt':
                    df.to_csv(name + '.txt', sep='\t', index=False, header=None)
                    break
                else:
                    data_type = input("文件格式有问题，仅限于txt,xlsx,csv，请重新选择: ")





