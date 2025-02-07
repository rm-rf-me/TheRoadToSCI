import numpy as np
import matplotlib as mpl
from config import TrackingConfig
from utils.sampling.base_sampling import Sample200and300PanBase
from utils.cmdIO import *

mpl.use('TkAgg')


class SignalTracker(Sample200and300PanBase):
    def __init__(self, args):
        super(SignalTracker, self).__init__(args)

    def usage_example(self):
        # 通过self.args[name]获取命令行参数的值，这个参数根据自己的需要在config.py中定义
        pan200_position = self.args['pan200_position']
        pan300_position = self.args['pan300_position']
        print(f"Pan200 position: {pan200_position}, Pan300 position: {pan300_position}")

        # 使用self.pan200.get_p()获取当前Pan200的位置，self.pan300.get_p()获取当前Pan300的位置，self.rx.getPower()获取当前接收机的功率
        pan200_position = self.pan200.get_p()
        pan300_position = self.pan300.get_p()
        power_value = self.rx.getPower()
        print(f"Pan200 position: {pan200_position}, Pan300 position: {pan300_position}, Power value: {power_value}")

        # 使用self.pan200.p_rel(angle)和self.pan300.p_rel(angle)来控制Pan200和Pan300的位置
        pan200_step_angle = 10
        self.pan200.p_rel(pan200_step_angle)
        pan300_step_angle = -10
        self.pan300.p_rel(pan300_step_angle)

    def run(self):
        peak_angles, peak_values = self.scan_and_find_peaks()

        print("Top 3 peak angles and their signal strengths:")
        for i in range(3):
            print(f"Angle: {peak_angles[i]}°, Signal Strength: {peak_values[i]}")

        # 从最强的信号角度开始进行极值跟踪
        initial_angle = peak_angles[np.argmax(peak_values)]
        final_angle, final_signal = self.track_max_signal(initial_angle)

        print(f"Final angle: {final_angle}° with signal strength {final_signal}")

    # 扫描一周，找出信号最大的三个角度
    def scan_and_find_peaks(self, step_size=1.0):
        """
        扫描一周（0° 到 360°），找出信号值最大的三个角度
        step_size: 扫描的步长（度）
        """
        signal_values = []
        angles = np.arange(0, 360, step_size)  # 扫描的角度
        step_count = int(360 // step_size)  # 扫描的步数
        for angle in range(step_count):
            self.pan200.p_rel(step_size)
            time.sleep(1)
            signal_values.append(self.rx.getPower())

        # 找到信号值最大的三个角度
        peak_indices = np.argsort(signal_values)[-3:]  # 找到前三个最大信号值的索引
        peak_angles = angles[peak_indices]  # 对应的角度
        peak_values = np.array(signal_values)[peak_indices]  # 对应的信号值

        return peak_angles, peak_values

    def step200_and_sacn(self, step_angle, sleep_time=1):
        self.pan200.p_rel(step_angle)
        time.sleep(sleep_time)
        return self.rx.getPower()

    def step300_and_sacn(self, step_angle, sleep_time=1):
        self.pan300.p_rel(step_angle)
        time.sleep(sleep_time)
        return self.rx.getPower()

    # 极值跟踪功能
    def track_max_signal(self, initial_angle, threshold=0.1, step_size=0.1):
        """
        从最强的角度开始，按照步长 0.1° 进行极值跟踪
        initial_angle: 初始角度（从扫描阶段得到的最强信号角度）
        threshold: 信号强度阈值，当信号强度小于该值时切换到其他角度
        step_size: 每次旋转的步长（度）
        """
        angle = initial_angle
        current_signal = self.rx.getPower()

        # 保存之前扫描的3个角度和信号值
        peak_angles, peak_values = self.scan_and_find_peaks()

        # 输出初始信息
        print(f"Starting at angle {angle}° with signal strength {current_signal}")

        while True:
            # 小幅度旋转：尝试顺时针和逆时针
            clockwise_angle = angle + step_size
            counterclockwise_angle = angle - step_size

            # 保证角度在 0° 到 360° 范围内
            clockwise_angle = clockwise_angle % 360
            counterclockwise_angle = counterclockwise_angle % 360

            clockwise_signal = self.step200_and_sacn(step_size)
            self.pan200.p_rel(-step_size)
            counterclockwise_signal = self.step200_and_sacn(-step_size)

            # 比较哪个方向的信号更强
            if clockwise_signal > current_signal:
                angle = clockwise_angle
                current_signal = clockwise_signal
            elif counterclockwise_signal > current_signal:
                angle = counterclockwise_angle
                current_signal = counterclockwise_signal
            else:
                # 如果信号强度小于阈值，则切换到其他角度
                if current_signal < threshold:
                    # 切换到信号值更大的另一个存储的角度
                    print("Signal below threshold, switching to another stored angle...")
                    # 选择一个信号较大的角度
                    new_angle = peak_angles[np.argmax(peak_values)]
                    angle = new_angle
                    current_signal = self.rx.getPower()
                    print(f"Switching to angle {angle}° with signal strength {current_signal}")

                # 如果已经达到极值（没有更高信号了），则退出
                break

        return angle, current_signal


# 运行主程序
if __name__ == '__main__':
    config = TrackingConfig()
    args = config.getArgs()
    code = SignalTracker(args)

    code.run()
