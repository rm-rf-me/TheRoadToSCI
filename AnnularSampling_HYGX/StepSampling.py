from StepConfig import StepConfig
from utils.cmdIO import *
from AnnularSampling_HYGX.util.SampleBase import SampleBase

import time
import matplotlib as mpl
import random

mpl.use('TkAgg')


class StepSampling(SampleBase):
    def __init__(self, args):
        super().__init__(args)

        acc, dec, v = io_set_adv(self.args)

        self.init_pan(float(acc), float(dec), float(v))

        self.check_name = ['max_angle', 'delay', 'stride', 'step_block', 'show_pic', 'save_pic', 'data_type']

    # angle正数为顺时针，负数为逆时针
    def get_series_step_rel(self, cmd_args=None):
        '''
        一步一停测得一组数据

        :param end_a: 最终停止的角度，正数为顺时针，负数为逆时针
        :param delay: 电机每步停止后的休眠时间，用于功率计测量
        :param stride: 步长，以度为单位
        :param block: 每步后是否输入阻塞（暂时废弃）
        :param show: 序列之后是否展示
        :return:
        '''

        if cmd_args is None:
            cmd_args = {}

        cmd_args = self._use_config_dict(cmd_args, self.check_name)

        note = io_get_note(self.args)
        data = {
            'time': [],
            'angle': [],
            'value': [],
            note: []
        }

        neg = 0
        if cmd_args['max_angle'] < 0:
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

            io_block(self.args, cmd_args['step_block'])

            data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
            data['angle'].append(angle)
            data['value'].append(float(val))
            data[note].append(' ')

            # 旋转到目标角跳出循环
            if (neg and cmd_args['max_angle'] >= 0) or (not neg and cmd_args['max_angle'] <= 0):
                break

            # 调用接口类旋转函数
            if neg:
                self.pan.p_rel(-cmd_args['stride'])
            else:
                self.pan.p_rel(cmd_args['stride'])

            pos = -1
            tmp = -2
            # 通过轮询确定停止位置
            while 1:
                if tmp == pos:
                    break
                tmp = pos
                pos = self.pan.get_p()

                time.sleep(0.1)

            time.sleep(cmd_args['delay'])

            if neg:
                cmd_args['max_angle'] += cmd_args['stride']
            else:
                cmd_args['max_angle'] -= cmd_args['stride']

        if cmd_args['show_pic'] or cmd_args['save_pic']:
            fig = self.show_pic(data['angle'], data['value'], xlabel='angle', ylabel='dBm',
                                show_pic=cmd_args['show_pic'])

        self.save_file(data, fig, cmd_args['save_pic'], cmd_args['data_type'])

        return data

    def goback_step(self, cmd_args=None):
        '''
        往返采样函数，是get_series_step_rel的简单封装，一次往返后回到原点，参数与get_series_step_rel保持一致

        :param args:
        :return:
        '''

        if cmd_args is None:
            cmd_args = {}

        cmd_args = self._use_config_dict(cmd_args, self.check_name)

        self.get_series_step_rel(cmd_args)
        self.get_series_step_rel(cmd_args)


if __name__ == '__main__':
    config = StepConfig()
    args = config.getArgs()
    haha = StepSampling(args)

    haha.goback_step()
