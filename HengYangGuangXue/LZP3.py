import serial
import time
import eventlet

base_config = {
    "MStep" : 20,
    "DriveRatio" : 180,
    "Baud" : 115200,
    "Port" : "COM5",
    "Timeout" : None,
    "motType" : 1.8,
    "obj" : 0,
    "safe" : {
        "acc" : 5,
        "dec" : 5,
        "v" : 10
    }
}


class LZP3:
    def __init__(self):
        # self.port = serial.tools.list_ports.comports()[args.port].device
        self.port = base_config['Port']
        self.baud = base_config['Baud']
        self.timeout = base_config['Timeout']
        self.obj = base_config['obj']
        self.safe = base_config['safe']

        self.comm = serial.Serial(self.port, baudrate=self.baud, timeout=self.timeout)
        time.sleep(1)       # wait serial
        print("Check: " + str(self.check()))

        self.motType = base_config['motType']
        self.MStep = base_config['MStep']
        self.driveRatio = base_config['DriveRatio']


        self.angle_step = int((360 / self.motType * self.MStep * self.driveRatio) / 360)


    def init(self, acc=1, dec=1, v=1):
        print("Set zero " + str(self.set_zero()) + ", now: " + str(self.get_p()))

        print("Set mode P " + str(self.set_mode_p()))

        print("Set default adv " + str(acc) + ", " + str(dec) + ", " + str(v) + ", " + str(self.set_acc_dec_v(acc, dec, v)))

    def set_mode_p(self):
        cmd = "MODE_P " + str(self.obj) + " 0"
        self._send(cmd)

        return self._wait_receive()

    def set_acc_dec_v(self, acc=1, dec=1, v=1):
        cmd = "P_ACC_DEC_V " + str(self.obj)
        if self.safe['acc'] > acc > 0:
            cmd += " " + str(acc * self.angle_step)
        else:
            return "acc illegal"

        if self.safe['dec'] > dec > 0:
            cmd += " " + str(dec * self.angle_step)
        else:
            return "dec illegal"

        if self.safe['v'] > v > 0:
            cmd += " " + str(v * self.angle_step)
        else:
            return "v illegal"

        self._send(cmd)

        return self._wait_receive()

    def p_rel(self, angle):
        cmd = "P_REL " + str(self.obj) + " " + str(angle * self.angle_step)
        self._send(cmd)
        return self._wait_receive()

    def p_abs(self, angle):
        cmd = "P_ABS " + str(self.obj) + " " + str(angle * self.angle_step)
        self._send(cmd)
        return self._wait_receive()

    def p_stop(self):
        cmd = "P_STOP " + str(self.obj)
        self._send(cmd)
        return self._wait_receive()

    def set_zero(self):
        cmd = "SET_P " + str(self.obj) + " 0"
        self._send(cmd)
        return self._wait_receive()

    def check(self):
        self._send("CHECK")
        return self._wait_receive()

    def get_p(self):
        cmd = "GET_P " + str(self.obj)
        self._send(cmd)
        return int(self._wait_receive()) / self.angle_step

    def _send(self, text):
        # self.comm.write(text.encode())
        # now = time.time()
        cmd = text + '\r\n'
        return self.comm.write(cmd.encode())

    def _receive(self):
        return self.comm.readline()[:-2]

    def _event_receive(self):
        eventlet.monkey_patch()

        with eventlet.Timeout(5, False):
            res = self._wait_receive()
            return str(res)
        return 0

    def _wait_receive(self):
        while 1:
            if (self.comm.inWaiting() > 0):
                res = self.comm.readline()[:-2]
                return res

    def _close(self):
        self.comm.close()
        print(self.comm.name + " closed.")

    # 暂时废弃掉，靠wait receive阻塞就行
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




if __name__ == '__main__':
    haha = LZP3()
    print("start: " + haha.get_p())
    haha.p_rel(1)
    time.sleep(2)
    print("end: " + haha.get_p())
