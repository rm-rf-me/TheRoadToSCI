import pyvisa as visa
from AnnularSampling_HYGX.StepConfig import StepConfig


class Rx2438:
    def __init__(self, args):
        self.args = args
        rm = visa.ResourceManager()
        # res = rm.list_resources()
        # print('find resources: ', res)
        self.haha = rm.open_resource(args.rxPath, read_termination='\n')
        print("Rx连接成功: " + str(self.haha))
        # self.setFreq(self.args.freq)
        # print("Rx2438 freq :", self.args.freq)

    def setFreq(self, freq):
        '''
        设置功率计测量频率，需携带单位
        :param freq:
        :return:
        '''
        print("rx set freq: %sGHz" % freq)
        return self._write('FREQ ' + freq + 'GHz\n')

    def getPower(self):
        '''
        使用fetch命令，立即读取屏幕数值，不保证完整完成一次测量，io开销在ms级别
        :return:
        '''
        return self._query('FETC?\n')

    def _query(self, cmd):
        return self.haha.query(cmd)

    def _write(self, cmd):
        return self.haha.write(cmd)


if __name__ == '__main__':
    config = StepConfig()
    args = config.getArgs()
    rx = Rx2438(args)
    print(rx.getPower())
