import argparse

class Config:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')

        self.parser.add_argument('--baud', type=int, default=57600)
        self.parser.add_argument('--port', type=str, default='COM3')
        self.parser.add_argument('--commTimeout', type=int, default=None)

        self.parser.add_argument('--rxPath', type=str, default='TCPIP0::169.254.216.79::6666::SOCKET')
        self.parser.add_argument('--rxTimeout', type=int, default=1000)
        self.parser.add_argument('--termination', type=str, default='\n')
        self.parser.add_argument('--freq', type=str, default='1GHz')

        self.parser.add_argument('--motType', type=float, default=0.9)
        self.parser.add_argument('--MStep', type=int, default=16)

        self.args = self.parser.parse_args()

    def getArgs(self):
        return self.args



