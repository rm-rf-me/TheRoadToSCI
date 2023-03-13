import pyvisa as visa
import time
from config import Config

class Rx2438:
    def __init__(self, args):
        self.args = args
        rm = visa.ResourceManager()
        res = rm.list_resources()
        print('find resources: ', res)
        self.haha = rm.open_resource(args.rxPath, read_termination='\n')
        print(self.haha)
        # self.setFreq(self.args.freq)
        # print("Rx2438 freq :", self.args.freq)


    def setFreq(self, freq):
        return self._write('FREQ ' + freq + '\n')

    def getPower(self):
        return self._query('FETC?\n')

    def _query(self, cmd):
        return self.haha.query(cmd)

    def _write(self, cmd):
        return self.haha.write(cmd)


if __name__ == '__main__':
    config = Config()
    args = config.getArgs()
    rx = Rx2438(args)
    print(rx.getPower())
