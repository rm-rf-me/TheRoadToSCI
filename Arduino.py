import serial
import time
from config import Config


class Arduino:
    def __init__(self, args):
        # self.port = serial.tools.list_ports.comports()[args.port].device
        self.port = args.port
        self.comm = serial.Serial(self.port, baudrate=args.baud, timeout=args.commTimeout)
        time.sleep(1)       # wait serial
        print(self.comm)
        if 'open' == self._wait_receive():
            print("serial open")

        self.motType = args.motType
        self.MStep = args.MStep
        self.round_step = int(360 / self.motType * self.MStep)


    def _send(self, text):
        return self.comm.write(text.encode())

    def _receive(self):
        return self.comm.readline()[:-2]

    def _wait_receive(self):
        while 1:
            if (self.comm.inWaiting() > 0):
                return self.comm.readline()[:-2]

    def _close(self):
        self.comm.close()
        print(self.comm.name + " closed.")

    def _isAvailable(self):
        while 1:
            self._send('q')
            haha = self._receive()
            # print(haha)
            if haha == b'y':
                return
            time.sleep(0.05)

    def _open(self):
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

    def Round(self, dirr, angle, speed):
        self._isAvailable()
        cmd = 'a'
        if dirr == 'CW':
            cmd += '0'
        elif dirr == 'CCW':
            cmd += '1'
        if angle > 999 or angle < 0:
            return 0
        cmd += str(angle).zfill(3)
        if speed > 999 or speed < 0:
            return 0
        cmd += str(speed).zfill(3)
        print("round cmd:", cmd)
        self._send(cmd)

        return self._wait_receive()

    def goback(self, dirr, angle, speed, mid_delay):
        self._isAvailable()
        cmd = 'b'
        if dirr == 'CW':
            cmd += '0'
        elif dirr == 'CCW':
            cmd += '1'
        if angle > 999 or angle < 0:
            return 0
        cmd += str(angle).zfill(3)
        if speed > 999 or speed < 0:
            return 0
        cmd += str(speed).zfill(3)
        if mid_delay > 999 or mid_delay < 0:
            return 0
        cmd += str(mid_delay).zfill(3)
        print("goback cmd:", cmd)
        self._send(cmd)

        return self._wait_receive()

    def turnAround(self, dirr, speed):
        self._isAvailable()
        cmd = 'c'
        if dirr == 'CW':
            cmd += '0'
        elif dirr == 'CCW':
            cmd += '1'

        if speed > 999 or speed < 0:
            return 0
        cmd += str(speed).zfill(3)

        print("turnAround cmd:", cmd)
        self._send(cmd)

        return self._wait_receive()



if __name__ == '__main__':
    config = Config()
    args = config.getArgs()
    haha = Arduino(args)
    # haha = serial.Serial("COM3", baudrate=57600)


    print(haha.Round('CW', 720, 20))
    time.sleep(1)
    print(haha.Round('CCW', 720, 40))
    time.sleep(1)
    print(haha.goback('CW', 720, 20, 50))
    time.sleep(1)
    print(haha.turnAround('CW', 100))

    # print(haha.write('b0180090'.encode()))
