from Device_HengYangGuangXue.LZP3 import LZP3
from Device_Ceyear.RX2438 import Rx2438
from config import Config
from util.cmdIO import *

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

        io_rx_test(self.args, self.rx)


        acc, dec, v = io_set_adv(self.args)

        self.init_pan(float(acc), float(dec), float(v))

        self.freq, self.power = io_set_tx(self.args)

    def init_pan(self, acc=5, dec=5, v=5):
        self.pan.init(acc, dec, v)


    def _use_config_dict(self, args):
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
        if args['max_angle'] is None:
            args['max_angle'] = self.args.max_angle
        if args['delay'] is None:
            args['delay'] = self.args.delay
        if args['stride'] is None:
            args['stride'] = self.args.stride
        if args['step_block'] is None:
            args['step_block'] = self.args.step_block
        if args['show_pic'] is None:
            args['show_pic'] = self.args.show_pic
        if args['save_pic'] is None:
            args['save_pic'] = self.args.save_pic
        if args['data_type'] is None:
            args['data_type'] = self.args.data_type

        return args

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

        note = io_get_note(self.args)
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

            io_block(self.args, step_block)

            data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
            data['angle'].append(angle)
            data['value'].append(float(val))
            data[note].append(' ')

            # 旋转到目标角跳出循环
            if (neg and max_angle >= 0) or (not neg and max_angle <= 0):
                break

            # 调用接口类旋转函数
            if neg:
                self.pan.p_rel(-stride)
            else:
                self.pan.p_rel(stride)

            pos = -1
            tmp = -2
            # 通过轮询确定停止位置
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

        # 数据保存
        path = io_get_file_name(self.args)
        if path != 'n' or path != 'N':
            # 默认路径为XXXSampling_/data/，命名格式为 时间戳-频率-功率-命令.对应格式
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
        '''
        往返采样函数，是get_series_step_rel的简单封装，一次往返后回到原点，参数与get_series_step_rel保持一致


        :param max_angle:
        :param delay:
        :param stride:
        :param step_block:
        :param show_pic:
        :param save_pic:
        :param data_type:
        :return:
        '''

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
