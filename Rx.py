import pyvisa as visa
import time

class Rx2438:
    def __init__(self, args):
        self.args = args
        rm = visa.ResourceManager()
        res = rm.list_resources()
        print('find resources: ', res)
        self.haha = rm.open_resource(args.rxPath, read_termination=args.termination, timeout=args.rxTimeout)
        self.setFreq(self.args.freq)

    def setFreq(self, freq):
        return self._write('FREQ ' + freq + '\n')

    def getPower(self):
        return self._query('FETCH?\n')

    def _query(self, cmd):
        return self.haha.query(cmd), time.time()

    def _write(self, cmd):
        return self.haha.write(cmd), time.time()
