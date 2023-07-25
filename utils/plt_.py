import base64
import copy
import time
from tkinter import Label

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import patheffects
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from utils.TkGUI import ScaleFactor, FONT_SIZE9, FONT_SIZE10, FONT_SIZE12, \
    FONT_SIZE14, FONT_SIZE16, FONT_SIZE18, FONT_SIZE20, FONT_SIZE22, width_, RATE
from Data import WeightRelationMap

BG_COLOUR = 'Beige'
BG_COLOUR2 = 'ivory'
DPI = int(100 * 125 * width_ / (ScaleFactor * 1920))


class Plot:
    Pie = 0
    pop_box = None  # 用于存储弹出框
    pop_wedge = None  # 用于存储上一个弹出的wedge
    animating = False  # 用于判断是否正在动画
    ALL_PIE = []  # 用于存储所有的饼图

    def __init__(self, master, title: str, type_="pie"):
        self.data = None
        self.wedges = None
        self.animating = False
        # 主窗口
        self.master = master
        self.fig = plt.Figure(facecolor=BG_COLOUR2, dpi=DPI) if type_ == "pie" else plt.Figure(
            facecolor=BG_COLOUR2, dpi=DPI, figsize=(3.7, 4.2))
        # 设置边距
        self.fig.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.1)
        self.subp = self.fig.add_subplot(1, 1, 1)  # 添加子图:1行1列第1个
        self.title = title
        self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=int(225 * RATE), y=0, anchor='n')
        self.subp.set_facecolor("white")  # 设置子图背景色
        # 去掉所有边框
        self.subp.spines['top'].set_visible(False)
        self.subp.spines['right'].set_visible(False)
        self.subp.spines['bottom'].set_visible(False)
        self.subp.spines['left'].set_visible(False)
        # 子图
        if type_ == "bar":
            self.subp2 = self.subp.twinx()
        # 显示暂无数据
        self.subp.text(0.5, 0.5, "暂无数据", fontsize=FONT_SIZE16, color='black', ha='center', va='center',
                       transform=self.subp.transAxes)
        # 绑定鼠标悬停事件
        # 鼠标停止不动时间2s后，显示当前行数：
        self.line_label = Label(master=master, text=' 行数：', bg='white', font=('微软雅黑', FONT_SIZE12))
        self.line_label.config(bd=1, relief='solid', anchor='w')
        self.canvas.mpl_connect('motion_notify_event', self._show_line)
        self.timer = time.time()
        Plot.ALL_PIE.append(self)

    def _show_line(self, event=None):
        self.timer = time.time()
        self.line_label.place_forget()  # 隐藏行数
        # 非阻塞式检测时间，如果鼠标停止不动1s后，显示当前行数：
        self.master.after(1000, self._show_line2)

    def _show_line2(self, event=None):
        if time.time() - self.timer < 1:
            return
        # 获取鼠标的坐标：
        x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        y = self.master.winfo_pointery() - self.master.winfo_rooty()
        self.line_label.config(text=f'单击查看详细信息', state='normal')
        self.line_label.place(x=x, y=y)

    def pie1(
            self,
            data: dict, labels: list, colors: list, show_threshold=0.03, show_legend=True, show_value=False):
        """
        无百分比显示，饼图内显示标签
        :param data:
        :param labels:
        :param colors:
        :param show_threshold: 显示比例的阈值
        :param show_legend: 是否显示图例
        :param show_value: 是否显示数值
        :return:
        """
        self.data = data
        # 清空子图内原有的图表
        self.subp.clear()
        self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        if not data:
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=FONT_SIZE16, color='black', ha='center', va='center',
                           transform=self.subp.transAxes)
            return
        # 如果比例小于3%，则在饼图外侧显示比例和标签，不在图内，防止标签重叠
        _data = []
        _labels = []
        if sum(data.values()) == 0:
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=FONT_SIZE16, color='black', ha='center', va='center',
                           transform=self.subp.transAxes)
            self.canvas.draw()
            return
        if not show_value:
            for key in labels:
                # 检查data中是否存在该栏数据
                if key in data.keys():
                    _data.append(data[key])
                    if data[key] / sum(data.values()) < show_threshold or key == "船体":
                        _labels.append('')
                    else:
                        _labels.append(key)
                else:
                    _data.append(0)
                    _labels.append('')
        else:  # 显示数值
            for key in labels:
                # 检查data中是否存在该栏数据
                if key in data.keys():
                    _data.append(data[key])
                    if data[key] / sum(data.values()) < show_threshold or key == "船体":
                        _labels.append('')
                    else:
                        _labels.append(round(data[key], 1))  # 显示数值
                else:
                    _data.append(0)
                    _labels.append('')
        data = _data
        # 按顺序绘制饼图
        self.wedges, texts = self.subp.pie(
            data,
            labels=_labels,
            # 在扇形图内部绘制labels
            colors=colors,
            startangle=90,
            textprops={'fontsize': FONT_SIZE12, 'color': '#000000', 'rotation_mode': 'anchor'},
            pctdistance=0.8,  # 调整标签位置
        )
        for wedge in self.wedges:
            wedge.set_edgecolor(BG_COLOUR2)
            wedge.set_linewidth(0.6)
            wedge.set_alpha(0.6)
            wedge.set_picker(True)

        # 调整标签文本的布局
        plt.setp(texts, ha='center', va='center')
        # 环绕显示标签
        plt.setp(texts, path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR2)])
        if show_legend:
            # 在左下边绘制图例
            self.subp.legend(
                labels,
                loc='upper right',
                fontsize=FONT_SIZE10,
                bbox_to_anchor=(0.25, 0.7, 0.2, 0.2),  # (x, y, width, height)
                borderaxespad=0.4,
                frameon=True,
                edgecolor=BG_COLOUR2,
            )
        # 调整文本的位置
        for text in texts:
            x, y = text.get_position()
            # 缩放比例
            show_value_map = {True: 0.4, False: 0.65}
            text.set_position((x * show_value_map[show_value], y * show_value_map[show_value]))  # 调整位置，根据需要调整缩放比例

        self.canvas.draw()
        # 绑定鼠标点击事件
        self.canvas.mpl_connect('pick_event', self.on_pick)

    def on_pick(self, event=None):
        if Plot.animating:
            return
        # 获取鼠标点击的扇形图和扇形区域
        active_wedge = event.artist
        Plot.animating = True
        # 扇形图动画
        if Plot.pop_wedge:
            Plot.pop_wedge.set_alpha(0.6)
            Plot.pop_wedge.set_edgecolor(BG_COLOUR2)
            theta0 = (Plot.pop_wedge.theta1 + Plot.pop_wedge.theta2) / 2  # 计算扇形的中心角度
            x0 = np.cos(np.deg2rad(theta0))
            y0 = np.sin(np.deg2rad(theta0))
            for i in range(2):
                # 缩小
                Plot.pop_wedge.set_radius(1.04 - i * 0.04)
                _x = x0 * (0.05 - i * 0.05)
                _y = y0 * (0.05 - i * 0.05)
                Plot.pop_wedge.set_center((_x, _y))
        Plot.pop_wedge = active_wedge
        # 信息处理
        w_color = active_wedge.get_facecolor()
        w_color = '#%02x%02x%02x' % (int(w_color[0] * 255), int(w_color[1] * 255), int(w_color[2] * 255))
        _text = active_wedge.get_label()
        # 展示具体信息
        pos_x = event.mouseevent.xdata
        pos_y = event.mouseevent.ydata
        try:
            if w_color == '#ffffff':
                _text = '船体'
            elif w_color == '#ffd6d0':
                _text = '装甲舱增重'
            elif w_color == '#ffaa99':
                _text = '装甲板'
            elif w_color == '#99ff99':
                _text = '动力系统'
            elif w_color == '#ffaaaa':
                _text = '火炮'
            elif w_color == '#aaaaff':
                _text = '鱼雷'
            elif w_color == '#aaffff':
                _text = '防空炮'
            elif w_color == '#eeccff':
                _text = '舰载机增重'
            elif w_color == '#ee00ff':
                _text = '装饰'
            value = round(self.data[_text], 1)
            unit = 't'
            report = get_weight_report(_text, value, sum(self.data.values()))
        except KeyError:
            unit = ''
            if w_color == '#ffaaaa':
                _text = "主炮耗弹"
            elif w_color == '#ffd6d0':
                _text = "副炮耗弹"
            elif w_color == '#aaaaff':
                _text = "鱼雷耗弹"
            elif w_color == '#aaffff':
                _text = "防空耗弹"
            value = round(self.data[_text], 1)
            report = get_ammo_report(_text, value, sum(self.data.values()))
        pct = value / sum(self.data.values()) * 100
        # 弹出框
        Plot.pop_box.remove() if Plot.pop_box else None
        Plot.pop_box = self.subp.annotate(
            # 显示具体数值和百分比
            f"  {value} / {round(sum(self.data.values()), 1)} {unit}  \n  {pct:.2f}%  {report}",
            xy=(pos_x, pos_y),
            xycoords='data',
            xytext=(pos_x, pos_y),
            textcoords='data',
            size=FONT_SIZE10,
            va="center",
            ha="center",
            bbox=dict(boxstyle="round4", fc="w", ec=BG_COLOUR2, lw=0.5, alpha=0.9),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.5", color=BG_COLOUR2),
            alpha=0.8,
            zorder=10
        )
        active_wedge.set_alpha(1)
        # 设置扇形偏离位置
        # 获取扇形的中心位置
        theta = (active_wedge.theta1 + active_wedge.theta2) / 2  # 计算扇形的中心角度
        x = np.cos(np.deg2rad(theta))
        y = np.sin(np.deg2rad(theta))
        for plot in Plot.ALL_PIE:
            if self != plot:
                plot.canvas.draw()
                break
        # 设置扇形动画
        for i in range(4):
            active_wedge.set_radius(1.02 + i * 0.02)
            _x = x * (0.01 + i * 0.01)
            _y = y * (0.01 + i * 0.01)
            active_wedge.set_center((_x, _y))
            self.canvas.flush_events()
            self.canvas.draw()
        Plot.animating = False

    @staticmethod
    def func(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def bar1(self, xs, ys, colors: list, y_range=(0, 1200), y_range2=(0, 12000)):
        """
        柱状图
        :param xs:
        :param ys:
        :param colors:
        :param y_range:
        :param y_range2:
        :return:
        """
        self.subp.clear()
        self.subp2.clear()
        self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        if not xs or not ys[0]:
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=FONT_SIZE16, color='black', ha='center', va='center',
                           transform=self.subp.transAxes)
            self.canvas.draw()
            return
        # 绘制单位弹药库耗弹量柱状图------------------------------------------------------------------------- #
        # 设置左边y轴范围，耗弹量
        self.subp.set_ylim(y_range)
        self.subp.set_ylabel('（Kg/min*弹药）', fontsize=FONT_SIZE10, rotation=-90, color='#6600bb')
        self.subp.yaxis.set_label_coords(0, 0.5)
        self.subp.tick_params(axis='y', colors='#6600bb')
        # 设置右边y轴范围
        self.subp2.set_ylim(y_range2)
        self.subp2.set_ylabel('（Kg/min）', fontsize=FONT_SIZE10, rotation=-90, color='#0066bb')
        self.subp2.yaxis.set_label_coords(0.9, 0.5)
        self.subp2.tick_params(axis='y', colors='#0066bb')
        # 按照颜色显示柱状图
        if colors:
            self.subp.bar(xs, ys, color=colors)
            # 隐藏标签
            self.subp.set_xticklabels([])
            self.subp2.set_xticklabels([])
        else:
            # 以投射量大小排序为渐变色
            colors = []
            colors2 = []
            for y in ys[0]:
                # print(y)
                colors.append((0.5, 0.3, 1, 0.19 + 0.8 * y / y_range[1]))
            for y in ys[1]:
                colors2.append((0.3, 0.5, 1, 0.19 + 0.8 * y / y_range2[1]))
            self.subp.bar(xs, ys[0], color=colors)
            self.subp2.bar(xs, ys[1], color=colors2)
            # 隐藏标签
            self.subp.set_xticklabels([])
            self.subp2.set_xticklabels([])
        # 设置半透明
        for patch in self.subp.patches:
            patch.set_alpha(0.8)
        for patch in self.subp2.patches:
            patch.set_alpha(0.8)
        # 显示数值和标签
        for x, y0, y1 in zip(xs, ys[0], ys[1]):
            # 用环绕的方式显示数值
            y_1 = y0 / y_range[1]
            y_2 = y1 / y_range2[1]
            if y_1 > y_2 and y_1 - y_2 < 0.03:
                y_2 -= 0.035
            elif y_1 < y_2 and y_2 - y_1 < 0.03:
                y_1 -= 0.035
            y_1 *= y_range[1]
            y_2 *= y_range2[1]
            self.subp.text(x, y_1, y0, ha='center', va='bottom', fontsize=FONT_SIZE10,
                           path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR2)])
            self.subp2.text(x, y_2, y1, ha='center', va='bottom', fontsize=FONT_SIZE10,
                            path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR2)])
            # 让标签呈一定角度，防止重叠
            if len(xs) >= 4:
                self.subp.text(x, -0.2, x, ha='center', va='top', fontsize=FONT_SIZE10, rotation=-20,
                               path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR)])
            else:
                self.subp.text(x, -0.2, x, ha='center', va='top', fontsize=FONT_SIZE10, rotation=0,
                               path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR)])
        self.canvas.draw()


class Plot3D:
    def __init__(
            self, master, title: str,
            figsize=(7, 7), dpi=DPI, top=0, bottom=0, left=0, right=0,
            place=(int(300 * RATE), 0), place_anchor='n'
    ):
        self.fig = plt.Figure(facecolor=BG_COLOUR, dpi=DPI, figsize=figsize)
        # 让self.fig占满整个画布
        # 绘图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams['agg.path.chunksize'] = 500000  # 解决绘图时出现的内存溢出问题
        # 清晰度
        plt.rcParams['figure.dpi'] = dpi
        # 设置边距
        self.fig.subplots_adjust(left=left, right=1 - right, top=1 - top, bottom=bottom)
        self.subp = self.fig.add_subplot(111, projection='3d', facecolor=BG_COLOUR2)
        # 设置标题
        self.title = title
        if title:
            self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().place(x=place[0], y=place[1], anchor=place_anchor)
        # 将box的底面设置为透明
        self.subp.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # 将box的坐标轴设置为透明
        self.subp.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.set_axes_preset([-1, 1], [-1, 1], [-1, 1], False, False, False)
        # 去掉所有边框
        self.subp.spines['top'].set_visible(False)
        self.subp.spines['right'].set_visible(False)
        self.subp.spines['left'].set_visible(False)
        self.subp.spines['bottom'].set_visible(False)
        self.plot_map = {
            "船体": [], "装甲舱": [],
            "弹药库": [], "机库": [],
            "主武器": [], "防空炮": [],
            "动力组": [],
            "装饰": [],
            "截面": [], "纵向": [], "甲板": []
        }
        # 将鼠标滚轮时间绑定到缩放
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        # 事件绑定
        self.press_position = None
        self.release_position = None
        self.control_dot = None
        self.canvas.draw()

    def plot(self, xs, ys, zs,
             x_range=(0, 10), y_range=(0, 10), z_range=(0, 10),
             colors=None,
             show_ticks=False,
             show_label=False,
             show_grid=False,
             ):
        """
        绘制3D图
        :param xs:
        :param ys:
        :param zs:
        :param x_range:
        :param y_range:
        :param z_range:
        :param colors:
        :param show_ticks:
        :param show_label:
        :param show_grid:
        :return:
        """
        self.subp.clear()
        if self.title:
            self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        if xs is None or ys is None or zs is None:
            self.subp.text(0.5, 0.5, '无数据', ha='center', va='center', fontsize=FONT_SIZE16, color='#6600bb')
            return
        self.set_axes_preset(x_range, y_range, z_range, show_ticks, show_label, show_grid)

    def add_dot(self, x, y, z, color=None, size=50):
        if color is None:
            color = 'black'
        # 绘制单个点
        self.control_dot = self.subp.scatter(x, y, z, c=color, s=size, linewidths=0, alpha=0.7)

    def move_dot(self, x, y, z):
        if self.control_dot is not None:
            self.control_dot._offsets3d = ([x], [y], [z])
            self.canvas.flush_events()
            self.canvas.draw()

    def set_axes_preset(self, x_range, y_range, z_range, show_ticks, show_label, show_grid):
        """
        设置图像预设
        :param x_range:
        :param y_range:
        :param z_range:
        :param show_ticks:
        :param show_label:
        :param show_grid:
        :return:
        """
        # 根据范围设置盒子的长宽比
        self.subp.set_box_aspect((x_range[1] - x_range[0], y_range[1] - y_range[0], z_range[1] - z_range[0]))
        # 设置坐标轴范围
        if x_range is not None:
            self.subp.set_xlim(*x_range)
        if y_range is not None:
            self.subp.set_ylim(*y_range)
        if z_range is not None:
            self.subp.set_zlim(*z_range)
        if show_ticks:
            self.subp.set_xticks([])
            self.subp.set_yticks([])
            self.subp.set_zticks([])
        else:
            self.subp.set_xticks([])
            self.subp.set_yticks([])
            self.subp.set_zticks([])
        # 设置坐标轴标签
        if show_label:
            self.subp.set_xlabel('X', fontsize=FONT_SIZE10, color='#6600bb')
            self.subp.set_ylabel('Y', fontsize=FONT_SIZE10, color='#6600bb')
            self.subp.set_zlabel('Z', fontsize=FONT_SIZE10, color='#6600bb')
        else:
            self.subp.set_xticklabels([])
            self.subp.set_yticklabels([])
            self.subp.set_zticklabels([])
        # 设置网格
        if show_grid:
            self.subp.grid(True)
        else:
            self.subp.grid(False)

    def plot_obj(self, data_base64, new_plot=True):
        """
        绘制obj文件
        :param data_base64:
        :param new_plot:
        :return:
        """
        if new_plot:
            # 清空画布
            self.subp.clear()
            if self.title:
                self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        # 设置视角距离
        self.subp.dist = 14
        # 读取文件编码
        f = base64.b64decode(data_base64)
        # 将文件编码转换为字符串
        f = f.decode()
        # 将字符串按行分割
        lines = f.splitlines()

        vertices = []
        faces = []

        # 解析.obj文件
        for line in lines:
            elements = line.strip().split()
            if elements[0] == 'v':
                vertex = [float(elements[1]), float(elements[2]), float(elements[3])]
                vertices.append(vertex)
            elif elements[0] == 'f':
                face = [int(elements[1].split('/')[0]), int(elements[2].split('/')[0]), int(elements[3].split('/')[0])]
                faces.append(face)
        # 交换y轴和z轴
        for i in range(len(vertices)):
            vertices[i][1], vertices[i][2] = vertices[i][2], vertices[i][1]
        # 获取x，y，z轴的范围
        x_range = [min([v[0] for v in vertices]), max([v[0] for v in vertices])]
        y_range = [min([v[1] for v in vertices]), max([v[1] for v in vertices])]
        z_range = [min([v[2] for v in vertices]), max([v[2] for v in vertices])]
        # 设置坐标轴范围
        self.set_axes_preset(x_range, y_range, z_range, show_ticks=False, show_label=False, show_grid=False)
        # # 绘制三维模型
        # for face in faces:
        #     x = [vertices[face[0] - 1][0], vertices[face[1] - 1][0], vertices[face[2] - 1][0]]
        #     y = [vertices[face[0] - 1][1], vertices[face[1] - 1][1], vertices[face[2] - 1][1]]
        #     z = [vertices[face[0] - 1][2], vertices[face[1] - 1][2], vertices[face[2] - 1][2]]
        #     self.subp.plot3D(x, y, z, color='#000000', alpha=0.5, linewidth=0.5)
        lines = []
        for face in faces:  # 把线段的两个端点加入lines
            xs = [vertices[face[0] - 1][0], vertices[face[1] - 1][0], vertices[face[2] - 1][0]]
            ys = [vertices[face[0] - 1][1], vertices[face[1] - 1][1], vertices[face[2] - 1][1]]
            zs = [vertices[face[0] - 1][2], vertices[face[1] - 1][2], vertices[face[2] - 1][2]]
            pc0 = Poly3DCollection([list(zip(xs, ys, zs))], alpha=0.5, linewidth=0.08,
                                   facecolors='#999999', edgecolors='#000000')

            self.subp.add_collection3d(pc0)
        #     dot1 = (vertices[face[0] - 1][0], vertices[face[0] - 1][1], vertices[face[0] - 1][2])
        #     dot2 = (vertices[face[1] - 1][0], vertices[face[1] - 1][1], vertices[face[1] - 1][2])
        #     dot3 = (vertices[face[2] - 1][0], vertices[face[2] - 1][1], vertices[face[2] - 1][2])
        #     lines.append([dot1, dot2])
        #     lines.append([dot2, dot3])
        #     lines.append([dot3, dot1])
        # pc = Poly3DCollection(lines, color="#000000", alpha=1, linewidth=0.05)
        # pc.set_facecolor('#999999')
        # self.subp.add_collection3d(pc)
        # 绘制
        self.canvas.draw()
        self.canvas.flush_events()

    def on_scroll(self, event):
        """
        鼠标滚轮事件
        :param event:
        :return:
        """
        # print(event.button, event.step)
        if self.subp.dist < 1 and event.button == 'up':
            self.subp.dist = 0.5
        elif event.button == 'up':
            self.subp.dist -= 0.5
        elif event.button == 'down':
            self.subp.dist += 0.5
        self.canvas.draw()

    def draw_ship(self, hull_data, hull_pos, rebar_data, airfix_data, part_data, ship_size):
        self.subp.clear()
        if self.title:
            self.subp.set_title(self.title, fontsize=FONT_SIZE16)
        # 设置视角距离
        self.subp.dist = 13
        self.plot_advanced_hull(hull_data, hull_pos)
        self.plot_rebar(rebar_data)
        self.plot_airfix(airfix_data)
        self.plot_part_dots(part_data, ship_size)
        self.add_dot(0, 0, 0)
        self.canvas.flush_events()
        self.canvas.draw()

    def plot_advanced_hull(self, hull_data, hull_pos):
        """
        绘制船体外壳
        :param hull_data: {"segment_name": [dot1, dot2, ...], ...}
        :param hull_pos: 船体位置
        :return:
        """

        if hull_data is None:
            return
        hull_pos = np.array([hull_pos[0], hull_pos[2], hull_pos[1]])
        deck_data = []
        deck_plot = []
        bottom_data = []
        x_range = [0, 0]
        y_range = [0, 0]
        z_range = [0, 0]

        for segment_name, segment_data in hull_data.items():
            segment_data = np.array(segment_data)
            segment_data = segment_data.T
            Len0 = len(segment_data[0])
            # 先添加甲板点集
            d_plot = [
                segment_data[0][0],
                segment_data[1][0],
                segment_data[2][0]
            ]
            deck_plot.append(d_plot)
            # 在segment_data 中分别获得最大坐标和最小坐标，设置为图表的范围
            for i in range(Len0):
                x_range[0] = min(x_range[0], segment_data[0][i])
                x_range[1] = max(x_range[1], segment_data[0][i])
                y_range[0] = min(y_range[0], segment_data[1][i])
                y_range[1] = max(y_range[1], segment_data[1][i])
                z_range[0] = min(z_range[0], segment_data[2][i])
                z_range[1] = max(z_range[1], segment_data[2][i])
            # deck_data 和 bottom_data 分别存储甲板和底部的点
            for ii in range(Len0 // 2):
                deck_data.append([])
                bottom_data.append([])
                # 再添加底部点集
                try:
                    deck_data[ii].append((segment_data[0][ii], segment_data[1][ii], segment_data[2][ii]))
                    bottom_data[ii].append((segment_data[0][Len0 - ii - 1], segment_data[1][Len0 - ii - 1],
                                            segment_data[2][Len0 - ii - 1]))
                except IndexError:
                    deck_data[ii].append(deck_data[ii][-1])
                    bottom_data[ii].append(bottom_data[ii][-1])
        # deck_d 和 bottom_d 的内容复制，再经过对称，再取一次反向，再加到原来的list中
        deck_d = copy.deepcopy(deck_data)
        bottom_d = copy.deepcopy(bottom_data)
        add_deck_plot = []
        for _i in range(len(deck_plot)):
            add_deck_plot.append([deck_plot[_i][0], -deck_plot[_i][1], deck_plot[_i][2]])
        deck_plot += add_deck_plot
        try:
            for i in range(10):
                deck_d[i] = [(x, -y, z) for x, y, z in deck_d[i]]
                bottom_d[i] = [(x, -y, z) for x, y, z in bottom_d[i]]
                deck_data[i] += deck_d[i][::-1]
                bottom_data[i] += bottom_d[i][::-1]
        except IndexError:
            pass
        # ------------------------------------------------------------------------------------------ 开始绘制
        for segment_name, segment_data in hull_data.items():
            segment_data = np.array(segment_data) + np.array(hull_pos)
            segment_data = segment_data.T
            Len1 = len(segment_data[0]) // 2
            # 绘制船体外壳点
            # self.plot_map["进阶船壳"].append(
            #    self.subp.scatter(segment_data[0], segment_data[1], segment_data[2], c='black', s=0.01)
            # )
            # 绘制船体外壳线
            self.plot_map["截面"].append(
                self.subp.plot(segment_data[0][:Len1], segment_data[1][:Len1], segment_data[2][:Len1],
                               c='black', linewidth=0.2)
            )
            self.plot_map["截面"].append(
                self.subp.plot(segment_data[0][Len1:], segment_data[1][Len1:], segment_data[2][Len1:],
                               c='black', linewidth=0.2)
            )
        # 绘制甲板和底部
        try:
            for i in range(6):
                deck_data[i] = np.array(deck_data[i]) + np.array(hull_pos)
                bottom_data[i] = np.array(bottom_data[i]) + np.array(hull_pos)
                deck_data[i] = deck_data[i].T
                bottom_data[i] = bottom_data[i].T
                if i == 0:
                    # 绘制甲板
                    Len2 = len(deck_plot)
                    dock_dots_ = []
                    for iii in range(Len2 // 2 - 1):
                        dots = np.array(
                            [
                                deck_plot[iii],
                                deck_plot[iii + 1],
                                deck_plot[Len2 // 2 + iii + 1],
                                deck_plot[Len2 // 2 + iii]
                            ]
                        ) + np.array(hull_pos)
                        dock_dots_.append(dots)
                    pc = Poly3DCollection(dock_dots_, facecolors='tan', edgecolors='black',
                                          # 置于底层
                                          zorder=10, linewidths=0.1, alpha=0.5)
                    self.plot_map["甲板"].append(self.subp.add_collection3d(pc))
                    # 绘制线条
                    self.plot_map["纵向"].append(
                        self.subp.plot(deck_data[i][0], deck_data[i][1], deck_data[i][2],
                                       c='#000000', linewidth=0.1)
                    )
                    self.plot_map["纵向"].append(
                        self.subp.plot(bottom_data[i][0], bottom_data[i][1], bottom_data[i][2],
                                       c='#000000', linewidth=0.8)
                    )
                    continue
                self.plot_map["纵向"].append(
                    self.subp.plot(deck_data[i][0], deck_data[i][1], deck_data[i][2],
                                   c='#000000', linewidth=1.5 * 0.6 ** (1.2 * (i + 1))
                                   ))
                self.plot_map["纵向"].append(
                    self.subp.plot(bottom_data[i][0], bottom_data[i][1], bottom_data[i][2],
                                   c='#000000', linewidth=1.5 * 0.6 ** (1.2 * i)
                                   ))
        except IndexError and ValueError as e:
            print(e)
        hull_range = [x_range, y_range, z_range]
        return hull_range

    def split_hull_x(self, hull, x):
        """
        :param hull: SplitAdHull 对象
        :param x: 要切割的 x 坐标
        :return:
        """

    def plot_rebar(self, rebar_data):
        ...

    def plot_airfix(self, airfix_data):
        ...

    def plot_part_dots(self, part_data, size):
        """
        :param part_data: {'船体': [Part对象列表], '火炮': [Part对象列表], ...}
        :param size: [x_range, y_range, z_range]
        :return:
        """
        if not part_data:
            return
        self.set_axes_preset(size[0], size[1], size[2], show_label=False, show_ticks=True, show_grid=True)
        color_map = {
            "船体": "#888888", "装甲舱": "#ffaa00", "火炮": "#ff0000", "鱼雷": "#0000ff", "防空炮": "#00ffff",
            "火控": "#ee00ff", "测距仪": "#ee00ff", "排烟器": "#00ff00", "传动": "#00ff00", "弹射器": "#ee00ff",
            "装饰": "#ee00ff"
        }
        size_map = {
            "船体": 4, "装甲舱": 25, "火炮": 300, "鱼雷": 300, "防空炮": 50,
            "火控": 4, "测距仪": 4, "排烟器": 300, "传动": 4, "弹射器": 4,
            "装饰": 4
        }
        for part_class, parts in part_data.items():
            if not parts:
                continue
            if part_class in "船体":
                dots0 = []
                for part in parts:
                    _x = part.PosX
                    _y = part.PosY
                    _z = part.PosZ
                    _rx = part.RotX
                    _ry = part.RotY
                    _rz = part.RotZ
                    if part.ID in "弹药库":
                        # 绘制面，正负 0.5
                        plc = Poly3DCollection([
                            [[_x - 0.5, _z + 0.5, _y - 0.5], [_x - 0.5, _z + 0.5, _y + 0.5],
                             [_x + 0.5, _z + 0.5, _y + 0.5], [_x + 0.5, _z + 0.5, _y - 0.5]],
                            [[_x - 0.5, _z - 0.5, _y - 0.5], [_x - 0.5, _z - 0.5, _y + 0.5],
                             [_x + 0.5, _z - 0.5, _y + 0.5], [_x + 0.5, _z - 0.5, _y - 0.5]],
                            [[_x - 0.5, _z - 0.5, _y - 0.5], [_x - 0.5, _z - 0.5, _y + 0.5],
                             [_x - 0.5, _z + 0.5, _y + 0.5], [_x - 0.5, _z + 0.5, _y - 0.5]],
                            [[_x + 0.5, _z - 0.5, _y - 0.5], [_x + 0.5, _z - 0.5, _y + 0.5],
                             [_x + 0.5, _z + 0.5, _y + 0.5], [_x + 0.5, _z + 0.5, _y - 0.5]],
                            [[_x - 0.5, _z - 0.5, _y - 0.5], [_x - 0.5, _z + 0.5, _y - 0.5],
                             [_x + 0.5, _z + 0.5, _y - 0.5], [_x + 0.5, _z - 0.5, _y - 0.5]],
                            [[_x - 0.5, _z - 0.5, _y + 0.5], [_x - 0.5, _z + 0.5, _y + 0.5],
                             [_x + 0.5, _z + 0.5, _y + 0.5], [_x + 0.5, _z - 0.5, _y + 0.5]]],
                            facecolors='red', linewidths=0, edgecolors='red', alpha=0.15, zsort='max')
                        self.plot_map["弹药库"].append(plc)
                        self.subp.add_collection3d(plc)

                    elif part.ID in "机库":
                        x_l = 1.5
                        y_l = 1
                        z_l = 1
                        if _rx in [0, 180] and _ry in [0, 180] and _rz in [0, 180]:
                            pass
                        elif _rx in [90, 270] and _ry in [0, 180] and _rz in [0, 180]:
                            x_l, y_l, z_l = x_l, z_l, y_l
                        elif _rx in [0, 180] and _ry in [90, 270] and _rz in [0, 180]:
                            x_l, y_l, z_l = z_l, y_l, x_l
                        elif _rx in [0, 180] and _ry in [0, 180] and _rz in [90, 270]:
                            x_l, y_l, z_l = y_l, x_l, z_l
                        elif _rx in [90, 270] and _ry in [90, 270] and _rz in [0, 180]:
                            x_l, y_l, z_l = z_l, x_l, y_l
                        elif _rx in [0, 180] and _ry in [90, 270] and _rz in [90, 270]:
                            x_l, y_l, z_l = y_l, z_l, x_l
                        elif _rx in [90, 270] and _ry in [0, 180] and _rz in [90, 270]:
                            x_l, y_l, z_l = x_l, z_l, y_l
                        elif _rx in [90, 270] and _ry in [90, 270] and _rz in [90, 270]:
                            x_l, y_l, z_l = z_l, y_l, x_l

                        plc = Poly3DCollection([
                            [[_x - x_l, _z + z_l, _y - y_l], [_x - x_l, _z + z_l, _y + y_l],
                             [_x + x_l, _z + z_l, _y + y_l], [_x + x_l, _z + z_l, _y - y_l]],
                            [[_x - x_l, _z - z_l, _y - y_l], [_x - x_l, _z - z_l, _y + y_l],
                             [_x + x_l, _z - z_l, _y + y_l], [_x + x_l, _z - z_l, _y - y_l]],
                            [[_x - x_l, _z - z_l, _y - y_l], [_x - x_l, _z - z_l, _y + y_l],
                             [_x - x_l, _z + z_l, _y + y_l], [_x - x_l, _z + z_l, _y - y_l]],
                            [[_x + x_l, _z - z_l, _y - y_l], [_x + x_l, _z - z_l, _y + y_l],
                             [_x + x_l, _z + z_l, _y + y_l], [_x + x_l, _z + z_l, _y - y_l]],
                            [[_x - x_l, _z - z_l, _y - y_l], [_x - x_l, _z + z_l, _y - y_l],
                             [_x + x_l, _z + z_l, _y - y_l], [_x + x_l, _z - z_l, _y - y_l]],
                            [[_x - x_l, _z - z_l, _y + y_l], [_x - x_l, _z + z_l, _y + y_l],
                             [_x + x_l, _z + z_l, _y + y_l], [_x + x_l, _z - z_l, _y + y_l]]],
                            facecolors='#ff5500', linewidths=0.5, edgecolors='#ff0000', alpha=0.25)
                        self.plot_map["机库"].append(plc)
                        self.subp.add_collection3d(plc)
                    else:
                        dots0.append((part.PosX, part.PosZ, part.PosY))
                self.plot_map["船体"].append(self.subp.scatter(
                    np.array(dots0).T[0], np.array(dots0).T[1], np.array(dots0).T[2],
                    c=color_map[part_class], s=size_map[part_class], linewidths=0,
                )) if dots0 else None
            else:
                dots = []
                for part in parts:
                    dots.append((part.PosX, part.PosZ, part.PosY))
                color = color_map[part_class]
                plot_map_name = part_class
                if part_class in "火炮鱼雷":
                    plot_map_name = "主武器"
                elif part_class in "排烟器传动":
                    plot_map_name = "动力组"
                elif part_class in "装饰弹射器测距仪火控":
                    plot_map_name = "装饰"
                self.plot_map[plot_map_name].append(self.subp.scatter(
                    np.array(dots).T[0], np.array(dots).T[1], np.array(dots).T[2],
                    c=color, s=size_map[part_class], alpha=0.5, linewidths=0
                ))
                # 显示标签
                if part_class in "火炮":
                    for part in parts:
                        # 设置居中标签
                        self.plot_map[plot_map_name].append(self.subp.text(
                            part.PosX, part.PosZ, part.PosY, part.ID[1:4], fontsize=FONT_SIZE9, ha='center',
                            va='center',
                            color='red'))
                elif "雷" in part_class:
                    for part in parts:
                        # 设置偏移标签
                        self.plot_map[plot_map_name].append(self.subp.text(
                            part.PosX, part.PosZ, part.PosY, part.ID[:3], fontsize=FONT_SIZE9, ha='center', va='center',
                            color='blue'))
                elif plot_map_name in "动力组":
                    for part in parts:
                        if "烟" in part.ID:
                            # 设置偏移标签
                            self.plot_map[plot_map_name].append(self.subp.text(
                                part.PosX, part.PosZ, part.PosY, part.ID[:3], fontsize=FONT_SIZE9, ha='center',
                                va='center',
                                color='green'))

    def hide_part(self, part_name):
        if self.plot_map[part_name]:
            for plot in self.plot_map[part_name]:
                try:
                    plot.set_visible(False)
                except AttributeError:
                    for p in plot:
                        try:
                            p.set_visible(False)
                        except ValueError:
                            pass
                except ValueError:
                    pass
        self.canvas.draw()

    def show_part(self, part_name):
        if self.plot_map[part_name]:
            for plot in self.plot_map[part_name]:
                try:
                    plot.set_visible(True)
                except AttributeError:
                    for p in plot:
                        try:
                            p.set_visible(True)
                        except ValueError:
                            pass
                except ValueError:
                    pass
        try:
            self.canvas.draw()
        except TypeError:
            pass

    def clear(self):
        self.subp.clear()


def get_weight_report(key, value, summary):
    WR_map = {
        "船体0": "\n浮储偏多\n可以尝试加入更多的装甲和武器；",
        "船体1": "\n浮储偏少\n可以尝试减少装甲，武器或动力；",
        "动力0": "\n轮机较重",
        "动力1": "\n轮机较轻\n如果浮储充足，可以尝试增加轮机；",
        "火炮0": "\n火炮较重",
        "火炮1": "\n火炮较轻",
        "鱼雷0": "\n鱼雷较重",
        "鱼雷1": "\n鱼雷较轻",
        "防空0": "\n防空较重",
        "防空1": "\n防空较轻",
        "装饰0": "\n装饰较重\n可以考虑用进阶装饰物替换部分装饰；",
        "装饰1": "\n装饰较轻",
        "装甲板0": "\n装甲板较重",
        "装甲板1": "\n装甲板较轻",
        "装甲舱增重0": "\n装甲舱较重",
        "装甲舱增重1": "\n装甲舱较轻",
        "适中": "\n适中",
    }
    result = ""
    rate = value / summary
    range_hull = [np.polyval(WeightRelationMap["船体"], summary), np.polyval(WeightRelationMap["船体标准差"], summary)]
    range_armor = [np.polyval(WeightRelationMap["装甲舱增重"], summary), np.polyval(WeightRelationMap["装甲舱增重标准差"], summary)]
    range_armor_board = [np.polyval(WeightRelationMap["装甲板"], summary),
                         np.polyval(WeightRelationMap["装甲板标准差"], summary)]
    range_engine = [np.polyval(WeightRelationMap["动力系统"], summary), np.polyval(WeightRelationMap["动力系统标准差"], summary)]
    range_gun = [np.polyval(WeightRelationMap["火炮"], summary), np.polyval(WeightRelationMap["火炮标准差"], summary)]
    range_torpedo = [np.polyval(WeightRelationMap["鱼雷"], summary), np.polyval(WeightRelationMap["鱼雷标准差"], summary)]
    range_AA = [np.polyval(WeightRelationMap["防空炮"], summary), np.polyval(WeightRelationMap["防空炮标准差"], summary)]
    range_aircraft = [np.polyval(WeightRelationMap["舰载机增重"], summary),
                      np.polyval(WeightRelationMap["舰载机增重标准差"], summary)]
    range_decoration = [np.polyval(WeightRelationMap["装饰"], summary), np.polyval(WeightRelationMap["装饰标准差"], summary)]
    if key == "船体":
        if rate > range_hull[0] + range_hull[1] * 3 / 2:
            result += WR_map["船体0"]
        elif rate < range_hull[0] - range_hull[1] * 1 / 3:
            result += WR_map["船体1"]
        else:
            result += WR_map["适中"]
    elif key == "装甲舱增重":
        if rate > range_armor[0] + range_armor[1]:
            result += WR_map["装甲舱增重0"]
        elif rate < range_armor[0] - range_armor[1]:
            result += WR_map["装甲舱增重1"]
        else:
            result += WR_map["适中"]
    elif key == "装甲板":
        if rate > range_armor_board[0] + range_armor_board[1]:
            result += WR_map["装甲板0"]
        elif rate < range_armor_board[0] - range_armor_board[1]:
            result += WR_map["装甲板1"]
        else:
            result += WR_map["适中"]
    elif key == "动力系统":
        if rate > range_engine[0] + range_engine[1]:
            result += WR_map["动力0"]
        elif rate < range_engine[0] - range_engine[1]:
            result += WR_map["动力1"]
        else:
            result += WR_map["适中"]
    elif key == "火炮":
        if rate > range_gun[0] + range_gun[1]:
            result += WR_map["火炮0"]
        elif rate < range_gun[0] - range_gun[1]:
            result += WR_map["火炮1"]
        else:
            result += WR_map["适中"]
    elif key == "鱼雷":
        if rate > range_torpedo[0] + range_torpedo[1]:
            result += WR_map["鱼雷0"]
        elif rate < range_torpedo[0] - range_torpedo[1]:
            result += WR_map["鱼雷1"]
    elif key == "防空":
        if rate > range_AA[0] + range_AA[1]:
            result += WR_map["防空0"]
        elif rate < range_AA[0] - range_AA[1]:
            result += WR_map["防空1"]
    elif key == "装饰":
        if rate > range_decoration[0] + range_decoration[1]:
            result += WR_map["装饰0"]
        elif rate < range_decoration[0] - range_decoration[1]:
            result += WR_map["装饰1"]
        else:
            result += WR_map["适中"]
    elif key == "舰载机增重":
        if rate > range_aircraft[0] + range_aircraft[1]:
            result += WR_map["舰载机0"]
        elif rate < range_aircraft[0] - range_aircraft[1]:
            result += WR_map["舰载机1"]
        else:
            result += WR_map["适中"]
    return result


def get_ammo_report(key, value, summary):
    AM_map = {
        "鱼雷0": "\n雷击能力很弱",
        "鱼雷1": "\n雷击能力很强",
        "防空0": "\n防空能力很弱",
        "防空1": "\n防空能力很强",
        "防空2": "\n防空能力适中",
    }
    result = ""
    range_torpedo = [4, 15]
    range_aa = [6, 19]
    if key == "鱼雷耗弹":
        if value < range_torpedo[0]:
            result += AM_map["鱼雷0"]
        elif value > range_torpedo[1]:
            result += AM_map["鱼雷1"]
    if key == "防空耗弹":
        if value < range_aa[0]:
            result += AM_map["防空0"]
        elif value > range_aa[1]:
            result += AM_map["防空1"]
        else:
            result += AM_map["防空2"]

    return result
