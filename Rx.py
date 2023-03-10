import pyvisa as visa
import time

class Rx2438:
    def __init__(self, args):
        rm = visa.ResourceManager()
        res = rm.list_resources()
        print('find resources: ', res)
        self.haha = rm.open_resource(args.rxPath, read_termination=args.termination, timeout=args.rxTimeout)

    def setFreq(self, fre):
        pass

    def getPower(self):
        pass

    def query(self, cmd):
        pass

    def write(self, cmd):
        pass
