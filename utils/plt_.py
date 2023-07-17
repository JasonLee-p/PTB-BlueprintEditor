import copy

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import patheffects, patches

BG_COLOUR = 'Beige'
BG_COLOUR2 = 'ivory'


class Plot:
    Pie = 0

    def __init__(self, master, title: str, type_="pie"):
        self.fig = plt.Figure(facecolor=BG_COLOUR, dpi=100) if type_ == "pie" else plt.Figure(
            facecolor=BG_COLOUR, dpi=100, figsize=(3.7, 4.2))
        # 设置边距
        self.fig.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.1)
        self.subp = self.fig.add_subplot(1, 1, 1)  # 添加子图:1行1列第1个
        self.title = title
        self.subp.set_title(self.title, fontsize=20)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=225, y=0, anchor='n')
        self.subp.set_facecolor(BG_COLOUR2)  # 设置子图背景色
        # 去掉所有边框
        self.subp.spines['top'].set_visible(False)
        self.subp.spines['right'].set_visible(False)
        self.subp.spines['bottom'].set_visible(False)
        self.subp.spines['left'].set_visible(False)
        # 子图
        if type_ == "bar":
            self.subp2 = self.subp.twinx()
        # 显示暂无数据
        self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='black', ha='center', va='center',
                       transform=self.subp.transAxes)

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
        # 清空子图内原有的图表
        self.subp.clear()
        self.subp.set_title(self.title, fontsize=20)
        if not data:
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='black', ha='center', va='center',
                           transform=self.subp.transAxes)
            return
        # 如果比例小于3%，则在饼图外侧显示比例和标签，不在图内，防止标签重叠
        _data = []
        _labels = []
        if sum(data.values()) == 0:
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='black', ha='center', va='center',
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
        wedges, texts = self.subp.pie(
            data,
            labels=_labels,
            # 在扇形图内部绘制labels
            colors=colors,
            startangle=90,
            textprops={'fontsize': 12, 'color': '#000000', 'rotation_mode': 'anchor'},
            pctdistance=0.8,  # 调整标签位置
        )
        # 调整标签文本的布局
        plt.setp(texts, ha='center', va='center')
        # 环绕显示标签
        plt.setp(texts, path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR)])
        if show_legend:
            # 在左下边绘制图例
            self.subp.legend(
                labels,
                loc='upper right',
                fontsize=10,
                bbox_to_anchor=(0.25, 0.7, 0.2, 0.2),  # (x, y, width, height)
                borderaxespad=0.4,
                # 无边框
                frameon=False,
            )
        # 调整文本的位置
        for text in texts:
            x, y = text.get_position()
            # 缩放比例
            show_value_map = {True: 0.4, False: 0.65}
            text.set_position((x * show_value_map[show_value], y * show_value_map[show_value]))  # 调整位置，根据需要调整缩放比例
        self.canvas.draw()

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
        self.subp.set_title(self.title, fontsize=20)
        if not xs or not ys[0]:
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='black', ha='center', va='center',
                           transform=self.subp.transAxes)
            self.canvas.draw()
            return
        # 绘制单位弹药库耗弹量柱状图------------------------------------------------------------------------- #
        # 设置左边y轴范围，耗弹量
        self.subp.set_ylim(y_range)
        self.subp.set_ylabel('（Kg/min*弹药）', fontsize=10, rotation=-90, color='#6600bb')
        self.subp.yaxis.set_label_coords(0, 0.5)
        self.subp.tick_params(axis='y', colors='#6600bb')
        # 设置右边y轴范围
        self.subp2.set_ylim(y_range2)
        self.subp2.set_ylabel('（Kg/min）', fontsize=10, rotation=-90, color='#0066bb')
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
            self.subp.text(x, y_1, y0, ha='center', va='bottom', fontsize=11,
                           path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR2)])
            self.subp2.text(x, y_2, y1, ha='center', va='bottom', fontsize=11,
                            path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR2)])
            # 让标签呈一定角度，防止重叠
            if len(xs) >= 4:
                self.subp.text(x, -0.2, x, ha='center', va='top', fontsize=9, rotation=-20,
                               path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR)])
            else:
                self.subp.text(x, -0.2, x, ha='center', va='top', fontsize=11, rotation=0,
                               path_effects=[patheffects.withStroke(linewidth=3, foreground=BG_COLOUR)])
        self.canvas.draw()


class Plot3D:
    def __init__(
            self, master, title: str,
            figsize=(7, 7), dpi=100, top=0, bottom=0, left=0, right=0,
            place=(300, 0), place_anchor='n'
    ):
        self.fig = plt.Figure(facecolor=BG_COLOUR, dpi=dpi, figsize=figsize)
        # 让self.fig占满整个画布
        # 绘图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams['agg.path.chunksize'] = 100000  # 解决绘图时出现的内存溢出问题
        # 设置边距
        self.fig.subplots_adjust(left=left, right=1 - right, top=1 - top, bottom=bottom)
        self.subp = self.fig.add_subplot(111, projection='3d')
        # 设置标题
        self.title = title
        if title:
            self.subp.set_title(self.title, fontsize=20)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().place(x=place[0], y=place[1], anchor=place_anchor)
        # 设置背景色
        self.subp.set_facecolor(BG_COLOUR2)
        self.subp.dist = 30
        # 去掉所有边框
        self.subp.spines['top'].set_visible(False)
        self.subp.spines['right'].set_visible(False)
        self.subp.spines['left'].set_visible(False)
        # self.subp.spines['bottom'].set_visible(False)
        self.plot_map = {
            "船体": [], "装甲舱": [],
            "弹药库": [], "机库": [],
            "主武器": [], "防空炮": [],
            "动力组": [],
            "装饰": [],
            "进阶船壳": [],
        }

        # 将鼠标滚轮时间绑定到缩放
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        # # 绑定右键为平移
        # self.canvas.mpl_connect('button_press_event', self.on_press)
        # self.canvas.mpl_connect('button_release_event', self.on_release)
        # 事件绑定
        self.press_position = None
        self.release_position = None

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
            self.subp.set_title(self.title, fontsize=20)
        if xs is None or ys is None or zs is None:
            self.subp.text(0.5, 0.5, '无数据', ha='center', va='center', fontsize=20, color='#6600bb')
            return

        self.set_axes_preset(x_range, y_range, z_range, show_ticks, show_label, show_grid)
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
        # 将box的底面设置为透明
        self.subp.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # 将box的坐标轴设置为透明
        self.subp.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.subp.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
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
            self.subp.set_xlabel('X', fontsize=10, color='#6600bb')
            self.subp.set_ylabel('Y', fontsize=10, color='#6600bb')
            self.subp.set_zlabel('Z', fontsize=10, color='#6600bb')
        else:
            self.subp.set_xticklabels([])
            self.subp.set_yticklabels([])
            self.subp.set_zticklabels([])
        # 设置网格
        if show_grid:
            self.subp.grid(True)
        else:
            self.subp.grid(False)

    def on_scroll(self, event):
        """
        鼠标滚轮事件
        :param event:
        :return:
        """
        # print(event.button, event.step)
        if event.button == 'up':
            self.subp.dist -= 0.5
        elif event.button == 'down':
            self.subp.dist += 0.5
        self.canvas.draw()

    def draw_ship(self, hull_data, hull_pos, rebar_data, airfix_data, part_data, ship_size):
        self.subp.clear()
        if self.title:
            self.subp.set_title(self.title, fontsize=20)
        # 设置视角距离
        self.subp.dist = 13
        self.plot_advanced_hull(hull_data, hull_pos)
        self.plot_rebar(rebar_data)
        self.plot_airfix(airfix_data)
        self.plot_part_dots(part_data, ship_size)

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
            self.plot_map["进阶船壳"].append(
                self.subp.plot(segment_data[0][:Len1], segment_data[1][:Len1], segment_data[2][:Len1],
                               c='black', linewidth=0.6)
            )
            self.plot_map["进阶船壳"].append(
                self.subp.plot(segment_data[0][Len1:], segment_data[1][Len1:], segment_data[2][Len1:],
                               c='black', linewidth=0.6)
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
                    for iii in range(Len2 // 2 - 1):
                        dots = np.array(
                            [deck_plot[iii:iii + 2], deck_plot[Len2 // 2 + iii:Len2 // 2 + iii + 2]]
                        ) + np.array(hull_pos)
                        dots = dots.T
                        self.plot_map["进阶船壳"].append(self.subp.plot_surface(
                            dots[0], dots[1], dots[2],
                            color='tan', alpha=0.95
                        )
                        )
                    # 绘制线条
                    self.plot_map["进阶船壳"].append(
                        self.subp.plot(deck_data[i][0], deck_data[i][1], deck_data[i][2],
                                       c='black', label='Deck', linewidth=1.5)
                    )
                    self.plot_map["进阶船壳"].append(
                        self.subp.plot(bottom_data[i][0], bottom_data[i][1], bottom_data[i][2],
                                       c='black', label='Bottom', linewidth=1.5)
                    )
                    continue
                self.plot_map["进阶船壳"].append(
                    self.subp.plot(deck_data[i][0], deck_data[i][1], deck_data[i][2],
                                   c='black', linewidth=0.6)
                )
                self.plot_map["进阶船壳"].append(
                    self.subp.plot(bottom_data[i][0], bottom_data[i][1], bottom_data[i][2],
                                   c='black', linewidth=0.6)
                )
        except IndexError and ValueError:
            pass
        self.canvas.draw()
        hull_range = [x_range, y_range, z_range]
        return hull_range

    def plot_rebar(self, rebar_data):
        self.canvas.draw()

    def plot_airfix(self, airfix_data):
        self.canvas.draw()

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
            "船体": "#888888", "装甲舱": "#ffff00", "火炮": "#ff0000", "鱼雷": "#0000ff", "防空炮": "#00ffff",
            "火控": "#ee00ff", "测距仪": "#ee00ff", "排烟器": "#00ff00", "传动": "#00ff00", "弹射器": "#ee00ff",
            "装饰": "#ee00ff"
        }
        size_map = {
            "船体": 4, "装甲舱": 50, "火炮": 300, "鱼雷": 300, "防空炮": 50,
            "火控": 4, "测距仪": 4, "排烟器": 500, "传动": 4, "弹射器": 4,
            "装饰": 4
        }
        for part_class, parts in part_data.items():
            if not parts:
                continue
            if part_class in "船体":
                dots0 = []
                dots_magazine = []
                dots_plane = []
                for part in parts:
                    if part.ID in "弹药库":
                        dots_magazine.append((part.PosX, part.PosZ, part.PosY))
                    elif part.ID in "机库":
                        dots_plane.append((part.PosX, part.PosZ, part.PosY))
                    else:
                        dots0.append((part.PosX, part.PosZ, part.PosY))
                self.plot_map["船体"].append(self.subp.scatter(
                    np.array(dots0).T[0], np.array(dots0).T[1], np.array(dots0).T[2],
                    c=color_map[part_class], s=size_map[part_class], linewidths=0
                )) if dots0 else None
                self.plot_map["弹药库"].append(self.subp.scatter(
                    np.array(dots_magazine).T[0], np.array(dots_magazine).T[1], np.array(dots_magazine).T[2],
                    c='red', s=size_map[part_class], linewidths=0
                )) if dots_magazine else None
                self.plot_map["机库"].append(self.subp.scatter(
                    np.array(dots_plane).T[0], np.array(dots_plane).T[1], np.array(dots_plane).T[2],
                    c='orange', s=300, linewidths=0
                )) if dots_plane else None
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
                            part.PosX, part.PosZ, part.PosY, part.ID[1:4], fontsize=8, ha='center', va='center',
                            color='red'))
                elif part_class in "鱼雷":
                    for part in parts:
                        # 设置偏移标签
                        self.plot_map[plot_map_name].append(self.subp.text(
                            part.PosX, part.PosZ, part.PosY, part.ID[:3], fontsize=8, ha='center', va='center',
                            color='blue'))
                elif part_class in "动力组":
                    for part in parts:
                        if "烟" in part.ID:
                            # 设置偏移标签
                            self.plot_map[plot_map_name].append(self.subp.text(
                                part.PosX, part.PosZ, part.PosY, part.ID[:3], fontsize=8, ha='center', va='center',
                                color='green'))
        self.canvas.draw()
        self.canvas.flush_events()

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
        self.canvas.draw()

    def clear(self):
        self.subp.clear()
