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

        self.check_name = ['acc_angle', 'dec_angle', 'stop_angle', 'tot_time', 'sampling_gap', 'show_pic', 'save_pic',
                           'data_type', 'save_name']

    def get_series_continuous_rel(self, cmd_args):
        if cmd_args is None:
            cmd_args = {}

        cmd_args = self._use_config_dict(cmd_args, self.check_name)

        neg = 0
        if cmd_args['acc_angle'] < 0 and cmd_args['dec_angle'] < 0 and cmd_args['stop_angle'] < 0:
            neg = 1
        elif cmd_args['acc_angle'] > 0 and cmd_args['dec_angle'] > 0 and cmd_args['stop_angle'] > 0:
            neg = 0
        else:
            print("angle error")
            return

        v = (abs(cmd_args['dec_angle']) - abs(cmd_args['acc_angle'])) / cmd_args['tot_time']
        acc = v / (2 * abs(cmd_args['acc_angle']) / v)
        dec_len = abs(cmd_args['stop_angle']) - abs(cmd_args['dec_angle'])
        dec = v / (2 * dec_len / v)
        print("adv: %f %f %f" % (acc, dec, v))
        if acc > self.pan.safe['acc'] or dec > self.pan.safe['dec'] or v > self.pan.safe['v']:
            print("adv not safe")
            return

        note2 = io_get_note(self.args)
        note1 = "freq:%s power:%s acc_angle:%f dec_angle:%f stop_angle:%f tot_time:%f sampling_gap:%f acc:%f dec:%f v:%f" % (
            self.freq,
            self.power,
            cmd_args['acc_angle'],
            cmd_args['dec_angle'],
            cmd_args['stop_angle'],
            cmd_args['tot_time'],
            cmd_args['sampling_gap'],
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
        self.pan.p_rel(cmd_args['stop_angle'])
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
            time.sleep(cmd_args['sampling_gap'])

        if cmd_args['show_pic'] or cmd_args['save_pic']:
            fig = self.show_pic(data['angle'], data['value'], xlabel='angle', ylabel='dBm',
                                show_pic=cmd_args['show_pic'])

        self.save_file(data, fig, cmd_args['save_pic'], cmd_args['data_type'], cmd_args['save_name'])

        return data

    def goback_continuous(self, cmd_args):
        if cmd_args is None:
            cmd_args = {}

        cmd_args = self._use_config_dict(cmd_args, self.check_name)

        self.get_series_continuous_rel(cmd_args)
        self.get_series_continuous_rel(cmd_args)

    def goback_goback_continuous_batch(self, cmd_args=None):
        if cmd_args is None:
            cmd_args = {}
        cmd_args = self._use_config_dict(cmd_args, self.check_name)
        self.args.cmd = False
        for i in cmd_args['speeds']:
            cmd_args['save_name'] += "_T" + str(i)
            self.goback_continuous(cmd_args)


def get_batch(sampling):
    from script.get_lstm_data import get_lstm_all_surface_data
    get_lstm_all_surface_data(sampling)


if __name__ == '__main__':
    config = ContinuousConfig()
    args = config.getArgs()
    haha = ContinuousSampling(args)

    haha.goback_continuous()
