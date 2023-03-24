import time

def io_rx_test(args, rx):
    if args.cmd is True:
        print("test rx: " + rx.getPower())

def io_set_adv(args):
    a = args.acc
    d = args.dec
    v = args.v
    if args.cmd is True:
        qq = input("Config文件中当前电机参数adv为：%f %f %f，若正确请敲回车，若不正确请输入n：" % (a, d, v))
        if qq == 'n' or qq == 'N':
            return input("输入电机参数acc dev v，中间用空格隔开：").split()

    return a, d, v

def io_set_tx(args):
    freq = args.freq
    power = args.power
    if args.cmd is True:
        qq = input("Config文件中配置当前频率为%s，当前功率为%f，若正确请敲回车，若不正确请输n：" % (
            args.freq, args.power))
        if qq == 'n' or qq == 'N':
            freq = input("当前使用的频率是：")
            power = input("当前使用的功率是：")
        else:
            freq = args.freq
            power = args.power

    return freq, power

def io_get_note(args):
    if args.cmd is True:
        note = input("描述这组数据，这段话将写入数据文件中：")
        return note

def io_block(args, block):
    if args.cmd is True and block is True:
        input("回车继续：")

def io_get_file_name(args):
    if args.cmd is True:
        return input("需要保存请起名，不保存输n:")


