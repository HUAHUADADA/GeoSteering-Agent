import matplotlib

matplotlib.use('TkAgg')  # 确保在 Tkinter 中正常显示
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常
class TrajectoryPlot:
    def __init__(self, parent_frame):
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_trajectory_3d(self, trajectory):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        if trajectory:
            xs = [p.x for p in trajectory]
            ys = [p.y for p in trajectory]
            zs = [p.z for p in trajectory]
            ax.plot(xs, ys, zs, 'b-', linewidth=2, marker='o', markersize=4)
            ax.set_xlabel("北坐标 (m)")
            ax.set_ylabel("东坐标 (m)")
            ax.set_zlabel("垂深 (m)")
            ax.set_title("三维井轨迹")
        self.canvas.draw()

    def plot_thickness_bar(self, thickness_list, title="地层真厚度对比"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if thickness_list:
            names = [t["地层名称"] for t in thickness_list]
            values = [t["真厚度(米)"] for t in thickness_list]
            ax.bar(names, values, color='green')
            ax.set_ylabel("真厚度 (米)")
            ax.set_title(title)
            for i, v in enumerate(values):
                ax.text(i, v + 0.2, str(v), ha='center')
        self.canvas.draw()