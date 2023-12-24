import serial
from baseLogger import BaseLogger

xiaomo_config = {
    "Baud": 115200,
    "Timeout": None,
}


class Serial(BaseLogger):
    def __init__(self, args):
        super(Serial, self).__init__()
        self.port = args.port
        self.baud = xiaomo_config['Baud']
        self.timeout = xiaomo_config['Timeout']
        self.comm = serial.Serial(self.port, baudrate=self.baud, timeout=self.timeout)

    def send(self, text):
        '''
        统一发送函数
        :param text:
        :return:
        '''
        # self.comm.write(text.encode())
        # now = time.time()
        cmd = text + '\r\n'
        self.debug("Serial message to port %s" % self.comm.name, cmd.encode())
        return self.comm.write(cmd.encode())

    def receive(self):
        '''
        统一接受函数
        :return:
        '''
        msg = self.comm.readline()
        self.debug("Serial message from port %s" % self.comm.name, msg)
        return msg[:-2]

    def wait_receive(self):
        '''
        阻塞等待，由于电机是异步控制的，所以阻塞市场很短
        :return:
        '''
        while 1:
            if self.comm.inWaiting() > 0:
                res = self.comm.readline()
                self.debug("Serial message from port %s" % self.comm.name, res)
                return res[:-2]

    def close(self):
        '''
        关闭连接
        :return:
        '''
        self.comm.close()
        # print(self.comm.name + " closed.")
        self.info(self.comm.name + " 端口成功关闭")

    def open(self):
        '''
        打开连接
        :return:
        '''
        if self.comm.isOpen():
            # print(self.port, "open success")
            self.info(self.comm.name, "端口成功打开")
            return True
        else:
            self.comm.open()
            res = self.receive()
            # print(res)
            if self.comm.isOpen():
                # print(self.port, "open success")
                self.info(self.comm.name, "端口成功打开")
                return True
            else:
                self.info(self.port, "端口打开失败")
                return False
