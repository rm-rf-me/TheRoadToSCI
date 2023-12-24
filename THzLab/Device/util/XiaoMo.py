import serial
import time
from baseLogger import BaseLogger

xiaomo_config = {
    "Baud": 115200,
    "Timeout": None,
}


class XiaoMo(BaseLogger):
    def __init__(self, args, motor_config, comm, angle_reverse=False):
        '''
        LZP3控制接口，遵循rx323串口协议，控制命令遵循小墨科技MT22控制板命令
        :param args:
        '''

        self.comm = comm
        self.safe = motor_config['safe']
        self.name = motor_config['Name']
        self.obj = motor_config['obj']

        # print("Check %s: " % self.name + str(self.check()))
        self.info("检查电机[%s]端口id[%d]: " % (self.name, self.obj) + str(self.check()))

        self.motType = motor_config['motType']
        self.MStep = motor_config['MStep']
        self.driveRatio = motor_config['DriveRatio']
        self.angle_reverse = angle_reverse

        # 角度脉冲数，和细分、步进角、转动比有关
        self.angle_step = int((360 / self.motType * self.MStep * self.driveRatio) / 360)

        self.debug("初始化电机[%s]: 步进角[%f], 细分[%d], 传动比[1:%d], 是否反向[%r], 角度脉冲数[%d]" % (
                self.name,
                self.motType,
                self.MStep,
                self.driveRatio,
                self.angle_reverse,
                self.angle_step)
            )

    def _init_without_adc(self):
        print("设置当前位置为零点 " + str(self._set_zero()) + ", now: " + str(self.get_p()))

        print("设置定位运动模式 " + str(self._set_mode_p()))

    def _init(self, acc=1.0, dec=1.0, v=1.0):
        print("设置当前位置为零点 " + str(self._set_zero()) + ", now: " + str(self.get_p()))

        print("设置定位运动模式 " + str(self._set_mode_p()))

        print(
            "当前电机acc dec v " + str(acc) + ", " + str(dec) + ", " + str(v) + ", " + str(self.set_acc_dec_v(acc, dec, v)))

    def _set_mode_p(self):
        '''
        设置定位运动模式
        :return:
        '''
        cmd = "MODE_P " + str(self.obj) + " 0"
        self.comm.send(cmd)
        self.info("电机[%s]" % self.name + " set model p: " + cmd)

        return self.comm.wait_receive()

    def _set_acc_dec_v(self, acc, dec, v):
        '''
        设置三个参数
        :param acc:
        :param dec:
        :param v:
        :return:
        '''
        cmd = "P_ACC_DEC_V " + str(self.obj)
        if self.safe['acc'] >= acc > 0:
            cmd += " " + str(int(acc * self.angle_step))
        else:
            print("[ERROR] acc illegal")
            msg = "电机[%s]端口id[%d]" % (self.name, self.obj) + "加速加速度 acc[%f]不在安全范围内(< %f)" % (acc, self.safe['acc'])
            self.error(msg)
            return msg

        if self.safe['dec'] >= dec > 0:
            cmd += " " + str(int(dec * self.angle_step))
        else:
            msg = "电机[%s]端口id[%d]" % (self.name, self.obj) + "减速加速度 dec[%f]不在安全范围内(< %f)" % (dec, self.safe['dec'])
            self.error(msg)
            return msg

        if self.safe['v'] >= v > 0:
            cmd += " " + str(int(v * self.angle_step))
        else:
            msg = "电机[%s]端口id[%d]" % (self.name, self.obj) + "最大速度 v[%f]不在安全范围内(< %f)" % (v, self.safe['v'])
            self.error(msg)
            return msg

        self.info("电机[%s]端口id[%d]" % (self.name, self.obj) + "设置运动参数： 加速加速度[%f], 减速加速度[%f], 最大速度[%f]" % (acc, dec, v))
        self.comm.send(cmd)

        res = self.comm.wait_receive()

        print(cmd, res)

        return res

    def _p_rel(self, angle):
        '''
        相对定位运动
        :param angle:
        :return:
        '''
        if self.angle_reverse:
            angle = -angle
        cmd = "P_REL " + str(self.obj) + " " + str(angle * self.angle_step)
        self.comm.send(cmd)
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "相对定位运动：" + cmd)
        return self.comm.wait_receive()

    def _p_abs(self, angle):
        '''
        绝对定位运动
        :param angle:
        :return:
        '''
        if self.angle_reverse:
            angle = -angle
        cmd = "P_ABS " + str(self.obj) + " " + str(angle * self.angle_step)
        self.comm.send(cmd)
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "绝对定位运动：" + cmd)
        return self.comm.wait_receive()

    def _p_stop(self):
        '''
        停止
        :return:
        '''
        cmd = "P_STOP " + str(self.obj)
        self.comm.send(cmd)
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "停止：" + cmd)
        return self.comm.wait_receive()

    def _set_zero(self):
        '''
        设置当前位置为坐标系零点
        :return:
        '''
        cmd = "SET_P " + str(self.obj) + " 0"
        self.comm.send(cmd)
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "置当前为零位：" + cmd)
        return self.comm.wait_receive()

    def _check(self):
        '''
        握手检查
        :return:
        '''
        self.comm.send("CHECK")
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "链接检查")
        return self.comm.wait_receive()

    def _get_p(self):
        '''
        查询转盘当前位置，角度以最近一次设置零点坐标系为主
        :return:
        '''
        cmd = "GET_P " + str(self.obj)
        self.comm.send(cmd)
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "查询当前位置：" + cmd)
        return int(self.comm.wait_receive()) / self.angle_step

    def _get_v(self):
        cmd = "GET_V " + str(self.obj)
        self.comm.send(cmd)
        self.debug("电机[%s]端口id[%d]" % (self.name, self.obj) + "查询当前速度：" + cmd)
        return int(self.comm.wait_receive()) / self.angle_step
