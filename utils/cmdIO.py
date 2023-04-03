import time


def io_rx_test(args, rx):
    if args.cmd is True:
        print("test rx: " + rx.getPower())


def io_set_adv(args):
    a = args.acc
    d = args.dec
    v = args.v

    qq = input("Config文件中当前电机参数adv为：%f %f %f，若正确请敲回车，若不正确请输入n：" % (a, d, v))
    if qq == 'n' or qq == 'N':
        return input("输入电机参数acc dev v，中间用空格隔开：").split()

    return a, d, v


def io_set_rx(args):

    qq = input("Config文件中配置当前频率为%sGHz，当前功率为%sdBm, 倍频为%s，若正确请敲回车，若不正确请输n：" % (
        args.freq, args.power, args.multi))
    if qq == 'n' or qq == 'N':
        freq, power, multi = input("设置当前的频率和功率，只写数字，默认单位为GHz和dBm，空格隔开：").split()
    else:
        freq = args.freq
        power = args.power
        multi = args.multi

    return freq, power, multi


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
