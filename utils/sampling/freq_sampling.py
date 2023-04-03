from .base_sampling import SampleBase
from utils.cmdIO import *
import matplotlib.pyplot as plt

import random

class FreqSamplingBase(SampleBase):
    def __init__(self, args):
        super(FreqSamplingBase, self).__init__(args)

        self.check_name = [
            'power',
            'multi',
            'start_freq',
            'end_freq',
            'stride',
            'delay',
            'show_pic',
            'save_pic',
            'data_type',
            'save_name'
        ]

    def get_series_step_freq(self, cmd_args=None):
        if cmd_args is None:
            cmd_args = {}

        cmd_args = self._use_config_dict(cmd_args, self.check_name)


        if (cmd_args['start_freq'] > cmd_args['end_freq']) or cmd_args['stride'] < 0:
            print("freq step config error")
            return

        note2 = io_get_note(self.args)
        note1 = "multi:%s power:%s start_freq:%f end_freq:%f stride:%f" % (
            self.multi,
            self.power,
            cmd_args['start_freq'],
            cmd_args['end_freq'],
            cmd_args['stride'],
        )

        data = {
            'time': [],
            'use_time': [],
            'freq': [],
            'value': [],
            note1: [],
            note2: []
        }

        start_time = time.time()
        sq = cmd_args['start_freq']
        eq = cmd_args['end_freq']
        ss = cmd_args['stride']

        while 1:
            if sq > eq:
                break

            self.tx.setFreq(str(sq))
            self.rx.setFreq(str(sq))
            time.sleep(cmd_args['delay'])
            val = self.rx.getPower()
            now = time.time()

            print(now, sq, val)

            data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
            data['use_time'].append(now - start_time)
            data['freq'].append(sq)
            data['value'].append(float(val))
            data[note1].append(' ')
            data[note2].append(' ')

            sq += ss

        if self.args.cmd is True:
            print(cmd_args['save_name'])

        if cmd_args['show_pic'] or cmd_args['save_pic']:
            fig = self.show_pic(data['freq'], data['value'], xlabel='GHz', ylabel='dBm',
                                show_pic=cmd_args['show_pic'])

        self.save_file(data, fig, cmd_args['save_pic'], cmd_args['data_type'], cmd_args['save_name'])
        plt.close("all")
        return data


