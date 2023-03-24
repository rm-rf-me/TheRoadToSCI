from Device_HengYangGuangXue.LZP3 import LZP3
from Device_Ceyear.RX2438 import Rx2438
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
        self.pan = LZP3(args=args)

        print("test rx: " + self.rx.getPower())

        acc, dec, v = input("输入电机参数acc dev v，中间用空格隔开：").split()

        self.init_pan(float(acc), float(dec), float(v))

        qq = input("Config文件中配置当前频率为%s，当前功率为%f，若正确请敲回车，若不正确请输n：" % (
        self.args.freq, self.args.power))
        if qq == 'n' or qq == 'N':
            self.freq = input("当前使用的频率是：")
            self.power = input("当前使用的功率是：")
        else:
            self.freq = self.args.freq
            self.power = self.args.power

    def init_pan(self, acc=5, dec=5, v=5):
        self.pan.init(acc, dec, v)

    def _use_config(self, max_angle, delay, stride, step_block, show_pic, save_pic, data_type):
        '''
        用于保证调用参数优先于配置文件参数
        :param max_angle:
        :param delay:
        :param stride:
        :param step_block:
        :param show_pic:
        :param save_pic:
        :return:
        '''
        if max_angle is None:
            max_angle = self.args.max_angle
        if delay is None:
            delay = self.args.delay
        if stride is None:
            stride = self.args.stride
        if step_block is None:
            step_block = self.args.step_block
        if show_pic is None:
            show_pic = self.args.show_pic
        if save_pic is None:
            save_pic = self.args.save_pic
        if data_type is None:
            data_type = self.args.data_type

        return max_angle, delay, stride, step_block, show_pic, save_pic, data_type

    # angle正数为顺时针，负数为逆时针
    def get_series_step_rel(self, max_angle=None, delay=None, stride=None, step_block=None, show_pic=None,
                            save_pic=None, data_type=None):
        '''
        一步一停测得一组数据

        :param end_a: 最终停止的角度，正数为顺时针，负数为逆时针
        :param delay: 电机每步停止后的休眠时间，用于功率计测量
        :param stride: 步长，以度为单位
        :param block: 每步后是否输入阻塞（暂时废弃）
        :param show: 序列之后是否展示
        :return:
        '''

        max_angle, delay, stride, step_block, show_pic, save_pic, data_type = self._use_config(max_angle, delay, stride,
                                                                                               step_block, show_pic,
                                                                                               save_pic, data_type)

        note = input("描述这组数据，这段话将写入数据文件中：")
        data = {
            'time': [],
            'angle': [],
            'value': [],
            note: []
        }

        neg = 0
        if max_angle < 0:
            neg = 1

        while 1:
            if self.debugPan:
                val = random.random()
            else:
                val = self.rx.getPower()

            now = time.time()
            angle = self.pan.get_p()
            if angle < 0:
                angle = -angle
            print(now, angle, val)

            if step_block:
                input("回车继续：")
            data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
            data['angle'].append(angle)
            data['value'].append(float(val))
            data[note].append(' ')

            if (neg and max_angle >= 0) or (not neg and max_angle <= 0):
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
                max_angle += stride
            else:
                max_angle -= stride

        if show_pic or save_pic:
            plt.clf()
            plt.plot(data['angle'], data['value'])
            plt.xlabel('angle')
            plt.ylabel('dBm')
            if show_pic:
                plt.show()

        path = input("需要保存请起名，不保存输n:")
        if path != 'n' or path != 'N':
            name = './data/' + str(time.time()).split('.')[0] + '-F' + str(self.freq) + '-P' + str(self.power) + path
            if save_pic:
                plt.savefig(name + '.jpg')

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

        return data

    def get_series_continuous_rel(self, end_a, speed, ):
        pass

    def goback_step(self, max_angle=None, delay=None, stride=None, step_block=None, show_pic=None, save_pic=None,
                    data_type=None):
        max_angle, delay, stride, step_block, show_pic, save_pic, data_type = self._use_config(max_angle, delay, stride,
                                                                                               step_block, show_pic,
                                                                                               save_pic, data_type)

        self.get_series_step_rel(max_angle, delay, stride, step_block, show_pic, save_pic, data_type)
        self.get_series_step_rel(-max_angle, delay, stride, step_block, show_pic, save_pic, data_type)


if __name__ == '__main__':
    config = Config()
    args = config.getArgs()
    haha = GetData(args)
    # haha.init_pan()

    haha.goback_step()
