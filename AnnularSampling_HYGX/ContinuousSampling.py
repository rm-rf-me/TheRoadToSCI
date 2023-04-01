import matplotlib.pyplot as plt

from ContinuousConfig import ContinuousConfig
from utils.cmdIO import *
from AnnularSampling_HYGX.util.SampleBase import SampleBase

import time
import matplotlib as mpl
import random

mpl.use('TkAgg')


class ContinuousSampling(SampleBase):
    def __init__(self, args):
        super().__init__(args)

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
        if args['acc_angle'] is None:
            args['acc_angle'] = self.args.acc_angle
        if args['dec_angle'] is None:
            args['dec_angle'] = self.args.dec_angle
        if args['stop_angle'] is None:
            args['stop_angle'] = self.args.stop_angle
        if args['show_pic'] is None:
            args['show_pic'] = self.args.show_pic
        if args['save_pic'] is None:
            args['save_pic'] = self.args.save_pic
        if args['data_type'] is None:
            args['data_type'] = self.args.data_type

        return args

    def _use_config(self, acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name):
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
        if acc_angle is None:
            acc_angle = self.args.acc_angle
        if dec_angle is None:
            dec_angle = self.args.dec_angle
        if stop_angle is None:
            stop_angle = self.args.stop_angle
        if show_pic is None:
            show_pic = self.args.show_pic
        if save_pic is None:
            save_pic = self.args.save_pic
        if data_type is None:
            data_type = self.args.data_type
        if tot_time is None:
            tot_time = self.args.tot_time
        if sampling_gap is None:
            sampling_gap = self.args.sampling_gap
        if save_name is None:
            save_name = self.args.save_name

        return acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name

    def get_series_continuous_rel(self, acc_angle=None, dec_angle=None, stop_angle=None, tot_time=None,
                                  sampling_gap=None, show_pic=None, save_pic=None, data_type=None, save_name=None):
        acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name = self._use_config(
            acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name)


        neg = 0
        if acc_angle < 0 and dec_angle < 0 and stop_angle < 0:
            neg = 1
        elif acc_angle > 0 and dec_angle > 0 and stop_angle > 0:
            neg = 0
        else:
            print("angle error")
            return

        v = (abs(dec_angle) - abs(acc_angle)) / tot_time
        acc = v / (2 * abs(acc_angle) / v)
        dec_len = abs(stop_angle) - abs(dec_angle)
        dec = v / (2 * dec_len / v)
        print("adv: %f %f %f" % (acc, dec, v))
        if acc > self.pan.safe['acc'] or dec > self.pan.safe['dec'] or v > self.pan.safe['v']:
            print("adv not safe")
            return


        note2 = io_get_note(self.args)
        note1 = "freq:%s power:%s acc_angle:%f dec_angle:%f stop_angle:%f tot_time:%f sampling_gap:%f acc:%f dec:%f v:%f" % (
            self.freq,
            self.power,
            acc_angle,
            dec_angle,
            stop_angle,
            tot_time,
            sampling_gap,
            acc,
            dec,
            v
        )
        data = {
            'time': [],
            'use_time': [],
            'angle': [],
            'v': [],
            'value': [],
            note1: [],
            note2: []
        }

        self.pan.set_acc_dec_v(acc, dec, v)
        self.pan.p_rel(stop_angle)
        start_time = time.time()

        pos = -1
        tmp = -2
        while 1:
            if tmp == pos:
                break
            tmp = pos
            pos = self.pan.get_p()

            val = self.rx.getPower()
            angle = abs(self.pan.get_p())
            vv = abs(self.pan.get_v())
            now = time.time()

            print(now, angle, vv, val)

            data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
            data['use_time'].append(now - start_time)
            data['angle'].append(angle)
            data['v'].append(vv)
            data['value'].append(float(val))
            data[note1].append(' ')
            data[note2].append(' ')
            time.sleep(sampling_gap)

        if self.args.cmd is True:
            print(save_name)

        if show_pic or save_pic:
            fig = self.show_pic(data['angle'], data['value'], xlabel='angle', ylabel='dBm', show_pic=show_pic)

        self.save_file(data, fig, save_pic, data_type, save_name)
        plt.close("all")
        return data

    def goback_continuous(self, acc_angle=None, dec_angle=None, stop_angle=None, tot_time=None,
                          sampling_gap=None, show_pic=None, save_pic=None, data_type=None, save_name=None):
        acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name = self._use_config(
            acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name)

        self.get_series_continuous_rel(acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic,
                                       data_type, save_name+'_GO')
        self.get_series_continuous_rel(-acc_angle, -dec_angle, -stop_angle, tot_time, sampling_gap, show_pic, save_pic,
                                       data_type, save_name+'_BACK')

    def goback_single_continuous_batch(self, speeds, acc_angle=None, dec_angle=None, stop_angle=None, tot_time=None,
                                       sampling_gap=None, show_pic=None, save_pic=None, data_type=None, save_name=None, sample_block=None):
        acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name = self._use_config(
            acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name)
        self.args.cmd = False
        for i in range(len(speeds)):
            if save_name is None:
                name = "_T" + str(speeds[i])
            else:
                name = save_name[i] + "_T" + str(speeds[i])

            # self.goback_continuous(acc_angle, dec_angle, stop_angle, i, sampling_gap, show_pic, save_pic, data_type, save_name)
            self.get_series_continuous_rel(acc_angle, dec_angle, stop_angle, speeds[i], sampling_gap, show_pic, save_pic,
                                       data_type, name)

            acc_angle = -acc_angle
            dec_angle = -dec_angle
            stop_angle = -stop_angle
            if sample_block is not None:
                input("回车继续：")

    def goback_goback_continuous_batch(self, speeds, acc_angle=None, dec_angle=None, stop_angle=None, tot_time=None,
                                       sampling_gap=None, show_pic=None, save_pic=None, data_type=None, save_name=None, sample_block=None):
        acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name = self._use_config(
            acc_angle, dec_angle, stop_angle, tot_time, sampling_gap, show_pic, save_pic, data_type, save_name)
        self.args.cmd = False
        for i in range(len(speeds)):
            if save_name is None:
                name = "_T" + str(speeds[i])
            else:
                name = save_name[i] + "_T" + str(speeds[i])

            # self.goback_continuous(acc_angle, dec_angle, stop_angle, i, sampling_gap, show_pic, save_pic, data_type, save_name)
            self.goback_continuous(acc_angle, dec_angle, stop_angle, speeds[i], sampling_gap, show_pic, save_pic,
                                       data_type, name)

            if sample_block is not None and i != len(speeds) - 1:
                input("请移动表面：")

def get_batch(sampling):
    from script.get_lstm_data import get_lstm_one_surface_data
    get_lstm_one_surface_data(sampling)

if __name__ == '__main__':
    config = ContinuousConfig()
    args = config.getArgs()
    haha = ContinuousSampling(args)

    # haha.goback_continuous()
    get_batch(haha)

