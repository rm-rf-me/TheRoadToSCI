import serial
import time

class Arduino:
    def __init__(self, args):
        self.port = serial.tools.list_ports.comports()[args.port].device
        self.comm = serial.Serial(self.port, baudrate=args.baudrate, timeout=args.commTimeout)
        self.motType = args.motType
        self.MStep = args.MStep
        self.round_step = int(360 / self.motType * self.MStep)

    def _send(self, text):
        return self.comm.write(text.encode('gbk'))

    def _receive(self):
        return self.comm.read_all()

    def _close(self):
        self.comm.close()
        print(self.comm.name + " closed.")

    def _open(self):
        self.comm.open()
        if self.comm.isOpen():
            print(self.port, "open success")
            return True
        else:
            print("open failed")
            return False
