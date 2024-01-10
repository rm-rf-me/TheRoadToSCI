from Serial import Serial
from XiaoMo import XiaoMo
from baseLogger import BaseLogger


class BaseXiaoMoDevice(XiaoMo):
    def __init__(self):
        super(BaseXiaoMoDevice, self).__init__()
        pass

    def set_zero(self):
        pass

    def set_acc_dec_v(self, acc, dec, v):
        pass

    def move_relative(self):
        pass

    def move_absolute(self):
        pass

    def async_move_relative(self):
        pass

    def async_move_absolute(self):
        pass

    def get_position(self):
        pass

    def get_v(self):
        pass