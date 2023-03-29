import serial
import time

xiaomo_config = {
    "Baud": 115200,
    "Timeout": None,
}


class XiaoMo:
    def __init__(self, args, motor_config):
        '''
        LZP3控制接口，遵循rx323串口协议，控制命令遵循小墨科技MT22控制板命令
        :param args:
        '''
        # self.port = serial.tools.list_ports.comports()[args.port].device
        self.port = args.port
        self.baud = xiaomo_config['Baud']
        self.timeout = xiaomo_config['Timeout']
        self.obj = motor_config['obj']
        self.safe = motor_config['safe']

        self.comm = serial.Serial(self.port, baudrate=self.baud, timeout=self.timeout)
        time.sleep(1)  # wait serial
        print("Check LZP3: " + str(self.check()))

        self.motType = motor_config['motType']
        self.MStep = motor_config['MStep']
        self.driveRatio = motor_config['DriveRatio']

        # 角度脉冲数，和细分、步进角、转动比有关
        self.angle_step = int((360 / self.motType * self.MStep * self.driveRatio) / 360)

    def init_without_adc(self):
        print("设置当前位置为零点 " + str(self.set_zero()) + ", now: " + str(self.get_p()))

        print("设置定位运动模式 " + str(self.set_mode_p()))

    def init(self, acc=1, dec=1, v=1):
        print("设置当前位置为零点 " + str(self.set_zero()) + ", now: " + str(self.get_p()))

        print("设置定位运动模式 " + str(self.set_mode_p()))

        print(
            "当前电机acc dec v " + str(acc) + ", " + str(dec) + ", " + str(v) + ", " + str(self.set_acc_dec_v(acc, dec, v)))

    def set_mode_p(self):
        '''
        设置定位运动模式
        :return:
        '''
        cmd = "MODE_P " + str(self.obj) + " 0"
        self._send(cmd)

        return self._wait_receive()

    def set_acc_dec_v(self, acc, dec, v):
        '''
        设置三个参数
        :param acc:
        :param dec:
        :param v:
        :return:
        '''
        cmd = "P_ACC_DEC_V " + str(self.obj)
        if self.safe['acc'] > acc > 0:
            cmd += " " + str(int(acc * self.angle_step))
        else:
            return "[ERROR] acc illegal"

        if self.safe['dec'] > dec > 0:
            cmd += " " + str(int(dec * self.angle_step))
        else:
            return "[ERROR] dec illegal"

        if self.safe['v'] > v > 0:
            cmd += " " + str(int(v * self.angle_step))
        else:
            return "[ERROR] v illegal"

        self._send(cmd)

        res = self._wait_receive()

        print(cmd, res)

        return res

    def p_rel(self, angle):
        '''
        相对定位运动
        :param angle:
        :return:
        '''
        cmd = "P_REL " + str(self.obj) + " " + str(angle * self.angle_step)
        self._send(cmd)
        return self._wait_receive()

    def p_abs(self, angle):
        '''
        绝对定位运动
        :param angle:
        :return:
        '''
        cmd = "P_ABS " + str(self.obj) + " " + str(angle * self.angle_step)
        self._send(cmd)
        return self._wait_receive()

    def p_stop(self):
        '''
        停止
        :return:
        '''
        cmd = "P_STOP " + str(self.obj)
        self._send(cmd)
        return self._wait_receive()

    def set_zero(self):
        '''
        设置当前位置为坐标系零点
        :return:
        '''
        cmd = "SET_P " + str(self.obj) + " 0"
        self._send(cmd)
        return self._wait_receive()

    def check(self):
        '''
        握手检查
        :return:
        '''
        self._send("CHECK")
        return self._wait_receive()

    def get_p(self):
        '''
        查询转盘当前位置，角度以最近一次设置零点坐标系为主
        :return:
        '''
        cmd = "GET_P " + str(self.obj)
        self._send(cmd)
        return int(self._wait_receive()) / self.angle_step

    def get_v(self):
        cmd = "GET_V " + str(self.obj)
        self._send(cmd)
        return int(self._wait_receive()) / self.angle_step

    def _send(self, text):
        '''
        统一发送函数
        :param text:
        :return:
        '''
        # self.comm.write(text.encode())
        # now = time.time()
        cmd = text + '\r\n'
        return self.comm.write(cmd.encode())

    def _receive(self):
        '''
        统一接受函数
        :return:
        '''
        return self.comm.readline()[:-2]

    # def _event_receive(self):
    #     '''
    #     超时等待，暂时废弃
    #     :return:
    #     '''
    #     eventlet.monkey_patch()
    #
    #     with eventlet.Timeout(5, False):
    #         res = self._wait_receive()
    #         return str(res)
    #     return 0

    def _wait_receive(self):
        '''
        阻塞等待，由于电机是异步控制的，所以阻塞市场很短
        :return:
        '''
        while 1:
            if (self.comm.inWaiting() > 0):
                res = self.comm.readline()[:-2]
                return res

    def _close(self):
        '''
        关闭连接
        :return:
        '''
        self.comm.close()
        print(self.comm.name + " closed.")

    def _isAvailable(self):
        '''
        暂时废弃
        :return:
        '''
        while 1:
            self._send('q')
            haha = self._receive()
            # print(haha)
            if haha == b'y':
                return
            time.sleep(0.05)

    def _open(self):
        '''
        打开连接
        :return:
        '''
        if self.comm.isOpen():
            print(self.port, "open success")
            return True
        else:
            self.comm.open()
            res = self._receive()
            print(res)
            if self.comm.isOpen():
                print(self.port, "open success")
                return True
            else:
                print("open failed")
                return False
