from utils.config.base_config import BaseConfig


class StepConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        # 加速加速度，度/秒^2
        self.parser.add_argument('--acc', type=float, default=8)

        # 减速加速度，度/秒^2
        self.parser.add_argument('--dec', type=float, default=6)

        # 最大速度阈值，度/秒
        self.parser.add_argument('--v', type=float, default=8)

        # 步内等待时间，从转盘完全停止开始计时，秒
        self.parser.add_argument('--delay', type=float, default=1)

        # 步长，单位是度
        self.parser.add_argument('--stride', type=float, default=1)

        # 从当前位置开始的最远转动角度，一定要小心不要打到东西
        self.parser.add_argument('--max_angle', type=float, default=-90)


        # 单条数据测量结束后是否展示曲线
        self.parser.add_argument('--show_pic', type=bool, default=True)

        # 单条数据测量结束后是否保存曲线
        self.parser.add_argument('--save_pic', type=bool, default=True)

        # 每步测量后是否阻塞等待
        self.parser.add_argument('--step_block', type=bool, default=False)

        # 数据保存格式，支持txt、xlsx、csv
        self.parser.add_argument('--data_type', type=str, default='xlsx')

        # 是否为命令行执行模式
        self.parser.add_argument('--cmd', type=bool, default=True)

        self.args = self.parser.parse_args()
