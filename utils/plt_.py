import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import patheffects

BG_COLOUR = 'Beige'
BG_COLOUR2 = 'ivory'


class Plot:
    def __init__(self, master, title: str):
        self.fig = plt.Figure(facecolor=BG_COLOUR, dpi=100)
        self.subp = self.fig.add_subplot(1, 1, 1)  # 添加子图:1行1列第1个
        self.title = title
        self.subp.set_title(self.title, fontsize=20)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=220, y=0, anchor='n')
        self.subp.set_facecolor(BG_COLOUR)  # 设置子图背景色
        self.subp.spines['top'].set_visible(False)  # 去掉上边框
        # 显示暂无数据
        self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='gray', ha='center', va='center',
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
            self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='gray', ha='center', va='center',
                           transform=self.subp.transAxes)
            return
        # 如果比例小于3%，则在饼图外侧显示比例和标签，不在图内，防止标签重叠
        _data = []
        _labels = []
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
            #
            text.set_position((x * show_value_map[show_value], y * show_value_map[show_value]))  # 调整位置，根据需要调整缩放比例
        self.canvas.draw()

    # def pie2(self, data: dict, labels: list, colors: list):
    #     """
    #     无百分比显示，饼图内显示标签
    #     :param data:
    #     :param labels:
    #     :param colors:
    #     :return:
    #     """
    #     self.subp.clear()
    #     self.subp.set_title(self.title, fontsize=20)
    #     if not data:
    #         self.subp.text(0.5, 0.5, "暂无数据", fontsize=20, color='gray', ha='center', va='center',
    #                        transform=self.subp.transAxes)
    #         return
    #     # 如果比例小于1%，则在饼图外侧显示比例和标签，不在图内，防止标签重叠
    #     _data = []
    #     _labels = []
    #     for key in labels:
    #         # 检查data中是否存在该栏数据
    #         if key in data.keys():
    #             _data.append(data[key])
    #             if data[key] / sum(data.values()) < 0.01:
    #                 _labels.append('')
    #             else:
    #                 _labels.append(key)
    #         else:
    #             _data.append(0)
    #             _labels.append('')
    #     data = _data
    #     # 按顺序绘制饼图
    #     wedges, texts = self.subp.pie(
    #         data,
    #         labels=_labels,
    #         # 在扇形图内部绘制labels
    #         colors=colors,
    #         startangle=90,
    #         textprops={'fontsize': 12, 'color': '#000000', 'rotation_mode': 'anchor'},
    #         pctdistance=0.8,  # 调整标签位置
    #     )
    #     # 调整标签文本的布局
    #     plt.setp(texts, ha='center', va='center')
    #     # 环绕显示标签
    #     plt.setp(texts, path_effects=[patheffects.withStroke(linewidth=3, foreground="Beige")])
    #     # 调整文本的位置
    #     for text in texts:
    #         x, y = text.get_position()
    #         text.set_position((x * 0.65, y * 0.65))  # 调整位置，根据需要调整缩放比例
    #     self.canvas.draw()

    @staticmethod
    def func(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def bar1(self, xs, ys, colors: list):
        """
        柱状图
        :param xs:
        :param ys:
        :param colors:
        :return:
        """
        self.subp.clear()
        self.subp.set_title(self.title, fontsize=20)
        # 按照颜色显示柱状图
        self.subp.bar(xs, ys, color=colors)
        self.canvas.draw()
        # 显示数值
        for x, y in zip(xs, ys):
            # 用环绕的方式显示数值
            self.subp.text(x, y+0.1, y, ha='center', va='bottom', fontsize=12, path_effects=[patheffects.withStroke(linewidth=3, foreground="Beige")])
