# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import pyvisa as visa
import time




def haha():
    # 在下面的代码行中使用断点来调试脚本。
    rm = visa.ResourceManager()
    res = rm.list_resources()
    print(res)
    lala = rm.open_resource('TCPIP0::169.254.216.79::6666::SOCKET', read_termination='\n')
    # lala.timeout = 10000
    # lala.write('FETC:ARR:AWE:POW?')
    for i in range(10):
        print(time.time(), lala.query('FETC?\n'), time.time())



# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    haha()

