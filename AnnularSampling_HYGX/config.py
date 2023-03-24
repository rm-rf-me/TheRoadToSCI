import argparse

from AnnularSampling_HYGX.util.base_config import BaseConfig

class Config(BaseConfig):
    def __init__(self):
        super().__init__()

        # 当前使用的频率，字符串形式，用于记录
        self.parser.add_argument('--freq', type=str, default="None")

        # 当前使用的功率，浮点数形式，用于记录，单位为dbm
        self.parser.add_argument('--power', type=float, default=0)

        # 加速加速度，米/秒^2
        self.parser.add_argument('--acc', type=float, default=8)

        # 减速加速度，米/秒^2
        self.parser.add_argument('--dec', type=float, default=6)

        # 最大速度阈值，米/秒，超过15会丢步
        self.parser.add_argument('--v', type=float, default=8)

        # 步内等待时间，从转盘完全停止开始计时，秒
        self.parser.add_argument('--delay', type=float, default=0.2)

        # 步长，可以是小数
        self.parser.add_argument('--stride', type=float, default=2)

        # 从当前位置开始的最远转动角度，一定要小心不要打到东西；正数为顺时针，负数为逆时针
        self.parser.add_argument('--max_angle', type=float, default=-6)

        # 单条数据测量结束后是否展示曲线
        self.parser.add_argument('--show_pic', type=bool, default=True)

        # 单条数据测量结束后是否保存曲线
        self.parser.add_argument('--save_pic', type=bool, default=False)

        # 每步测量后是否阻塞等待
        self.parser.add_argument('--step_block', type=bool, default=False)

        # 数据保存格式，支持txt、xlsx、csv
        self.parser.add_argument('--data_type', type=str, default='xlsx')



        self.args = self.parser.parse_args()




