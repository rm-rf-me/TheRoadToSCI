import argparse


class BaseConfig:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')

        # 串口通信配置
        self.parser.add_argument('--baud', type=int, default=115200)
        self.parser.add_argument('--port', type=str, default='COM3')
        self.parser.add_argument('--commTimeout', type=int, default=None)

        # visa通信配置
        self.parser.add_argument('--rxPath', type=str, default='TCPIP0::169.254.216.79::6666::SOCKET')
        self.parser.add_argument('--rxTimeout', type=int, default=None)
        self.parser.add_argument('--termination', type=str, default='\n')
        # self.parser.add_argument('--freq', type=str, default='100GHz')

        # 电机参数
        self.parser.add_argument('--motType', type=float, default=1.8)
        self.parser.add_argument('--MStep', type=int, default=20)

        self.parser.add_argument('--debugPan', type=bool, default=0)

        self.args = None

    def getArgs(self):
        return self.args
