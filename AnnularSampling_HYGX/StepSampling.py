from config import Config
from util.cmdIO import *
from AnnularSampling_HYGX.util.SampleBase import SampleBase

import time
import matplotlib as mpl
import random

mpl.use('TkAgg')


class StepSampling(SampleBase):
    def __init__(self, args):
        super().__init__()


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
            self.show_pic(data['angle'], data['value'], xlabel='angle', ylabel='dBm', show_pic=show_pic)

        self.save_file(data, save_pic, data_type)


        return data


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
    haha = StepSampling(args)
    # haha.init_pan()

    haha.goback_step()
