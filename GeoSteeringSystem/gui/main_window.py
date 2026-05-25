#!/usr/bin/python
# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from gui.plot_canvas import TrajectoryPlot
from gui.log_handler import LogHandler
from core.models import SurveyPoint, FormationLayer
from agents.orchestrator import Orchestrator


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("地质导向多Agent协作系统 v2.0")
        self.root.geometry("1200x750")
        self.orchestrator = Orchestrator()
        self.survey = []
        self.formations = []
        self.create_widgets()

    def create_widgets(self):
        # 菜单栏
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="加载测点数据(CSV)", command=self.load_survey)
        file_menu.add_command(label="加载地层数据(CSV)", command=self.load_formations)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        self.root.config(menu=menubar)

        # 主框架
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧控制面板
        left_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="5")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        ttk.Button(left_frame, text="运行多Agent流水线", command=self.run_pipeline).pack(pady=5, fill=tk.X)
        ttk.Button(left_frame, text="显示轨迹3D图", command=self.show_trajectory).pack(pady=5, fill=tk.X)
        ttk.Button(left_frame, text="显示厚度柱状图", command=self.show_thickness).pack(pady=5, fill=tk.X)
        ttk.Button(left_frame, text="导出报告", command=self.export_report).pack(pady=5, fill=tk.X)

        # 参数区
        param_frame = ttk.LabelFrame(left_frame, text="敏感性参数", padding="5")
        param_frame.pack(pady=10, fill=tk.X)
        ttk.Label(param_frame, text="井斜角增量(度):").pack(anchor=tk.W)
        self.delta_var = tk.StringVar(value="5")
        ttk.Entry(param_frame, textvariable=self.delta_var, width=10).pack(fill=tk.X)

        # 右侧显示区域
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 笔记本选项卡
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.traj_frame = ttk.Frame(notebook)
        self.thick_frame = ttk.Frame(notebook)
        self.log_frame = ttk.Frame(notebook)
        notebook.add(self.traj_frame, text="轨迹与厚度图")
        notebook.add(self.thick_frame, text="数据表格")
        notebook.add(self.log_frame, text="运行日志")

        self.plot_canvas = TrajectoryPlot(self.traj_frame)

        # 表格
        self.tree = ttk.Treeview(self.thick_frame, columns=("地层", "真厚度", "视厚度"), show="headings")
        self.tree.heading("地层", text="地层名称")
        self.tree.heading("真厚度", text="真厚度(米)")
        self.tree.heading("视厚度", text="视厚度(米)")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 日志
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_handler = LogHandler(self.log_text)

    def load_survey(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            df = pd.read_csv(filepath)
            self.survey = []
            for _, row in df.iterrows():
                self.survey.append(SurveyPoint(row["MD"], row["Incl"], row["Azi"]))
            self.log_handler.log(f"已加载测点数据: {len(self.survey)} 个点")

    def load_formations(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            df = pd.read_csv(filepath)
            self.formations = []
            for _, row in df.iterrows():
                self.formations.append(
                    FormationLayer(row["Name"], row["TopMD"], row["BaseMD"], row["Dip"], row["DipAzimuth"]))
            self.log_handler.log(f"已加载地层数据: {len(self.formations)} 层")

    def run_pipeline(self):
        if not self.survey or not self.formations:
            messagebox.showerror("错误", "请先加载测点数据和地层数据")
            return
        try:
            delta = float(self.delta_var.get())
        except:
            delta = 5
        self.log_handler.log("启动多Agent协作流水线...")
        self.log_handler.log("  → 计算Agent: 执行轨迹解算与厚度计算")
        self.log_handler.log("  → 敏感性Agent: 执行参数变化分析")
        self.log_handler.log("  → 报告Agent: 生成智能分析报告")
        context = self.orchestrator.run_pipeline(self.survey, self.formations, do_sensitivity=True, delta=delta)
        self.context = context
        self.log_handler.log("流水线执行完成！")
        self.log_handler.log("报告摘要:\n" + context["report"][:200] + "...")
        self.update_table(context["thickness"])
        self.plot_canvas.plot_trajectory_3d(context["trajectory"])
        self.plot_canvas.plot_thickness_bar(context["thickness"], title="原始地层真厚度")

    def update_table(self, thickness):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in thickness:
            self.tree.insert("", tk.END, values=(t["地层名称"], t["真厚度(米)"], t["视厚度(米)"]))

    def show_trajectory(self):
        if hasattr(self, 'context') and 'trajectory' in self.context:
            self.plot_canvas.plot_trajectory_3d(self.context["trajectory"])
        else:
            messagebox.showinfo("提示", "请先运行流水线")

    def show_thickness(self):
        if hasattr(self, 'context') and 'thickness' in self.context:
            self.plot_canvas.plot_thickness_bar(self.context["thickness"], title="地层真厚度")
        else:
            messagebox.showinfo("提示", "请先运行流水线")

    def export_report(self):
        if not hasattr(self, 'context') or 'report' not in self.context:
            messagebox.showerror("错误", "没有可导出的报告，请先运行流水线")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.context["report"])
            self.log_handler.log(f"报告已导出到: {filepath}")

    def show_about(self):
        messagebox.showinfo("关于", "地质导向多Agent协作系统\n版本 2.0\n基于最小曲率法与矢量点积\n支持多Agent长链推理")