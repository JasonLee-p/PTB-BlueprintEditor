# -*- coding: utf-8 -*-
"""
Created on 2023/6/24 15:00
Project: 工艺战舰图纸阅读器
File: main.py
Description:
    This file is the main file of PTB-BlueprintReader,
    which is a program that can read blueprint files of From the Depths.
    本文件是工艺战舰图纸阅读器的主文件，该程序可以读取来自深渊的工艺战舰图纸文件。
"""
import base64
import os
# 项目文件
from IMGS import *
from utils_TkGUI import *
from xml_reader import ReadDesign
from utils_plot import *

LOCAL_ADDRESS = os.getcwd()


class MainHandler:
    def __init__(self):
        self.tree1 = GUI.Left.tree
        self.combox = GUI.Left.combox
        self.combox.bind('<Return>', self.combox_update)
        self.combox.bind('<Button-1>', self.combox_update)
        self.combox.bind('<MouseWheel>', self.combox_update)
        self.last_design = None
        self.DesignReader = None
        self.ReadingDesign = False

    def combox_update(self, event=None):
        """
        更新所有信息
        :return:
        """
        if self.last_design == self.combox.get():
            return
        if self.ReadingDesign:
            return
        self.ReadingDesign = True
        file_name = self.combox.get() + '.xml'
        # 在同目录下寻找有Design字样的文件夹:
        for root, dirs, files in os.walk(LOCAL_ADDRESS):
            for _dir in dirs:
                if 'Design' in _dir:
                    path = os.path.join(root, _dir, file_name)
                    if os.path.exists(path):
                        # 重新读取图纸
                        # 创建临时窗口
                        _win = TempTransparentWin('white')\
                            if GUI.current_Frame == GUI.ShowFrame else TempTransparentWin("black")
                        del self.DesignReader
                        # try:
                        self.DesignReader = ReadDesign(path)
                        self.DesignReader.read_parts()
                        self.DesignReader.read_armors()
                        self.DesignReader.read_rebars()
                        # 更新所有数据
                        GUI.Left.update_treeview()
                        GUI.ShowFrame.update_messages()
                        GUI.AnalFrame.update_plots()
                        self.last_design = self.combox.get()
                        # 删除临时窗口
                        _win.destroy()
                        self.ReadingDesign = False
                        return
                        # except Exception as e:
                        #     # 删除临时窗口
                        #     _win.destroy()
                        #     show_text(f'读取图纸失败！\n{e}\n', 'stderr')
                        #     self.ReadingDesign = False


class TkinterGUI:
    def __init__(self):
        self.root = tk.Tk()
        set_window(self.root, "PTB Blueprint Reader")
        self.ICO = tk.PhotoImage(data=base64.b64decode(ICO))
        self.root.iconphoto(True, self.ICO)
        # notebook
        self.notebook_main = ttk.Notebook(self.root)
        self.Bottom = BottomFrame(self.root, redirect=True)
        self.Left = LeftFrame(self.root)
        # 初始化标签页Frame
        self.Frame_BP = tk.Frame(bg=BG_COLOUR)
        self.Frame_AN = tk.Frame(bg=BG_COLOUR)
        self.Frame_CP = tk.Frame(bg=BG_COLOUR)
        self.Frame_CA = tk.Frame(bg=BG_COLOUR)
        self.Frame_3D = tk.Frame(bg=BG_COLOUR)
        self.notebook_main.add(self.Frame_BP, text='   图纸信息预览   ')
        self.notebook_main.add(self.Frame_AN, text='   图纸数据分析   ')
        self.notebook_main.add(self.Frame_CP, text='        对比器        ')
        self.notebook_main.add(self.Frame_CA, text='        计算器        ')
        self.notebook_main.add(self.Frame_3D, text='       3D预览       ')
        # 绑定标签被选中事件
        self.notebook_main.bind('<<NotebookTabChanged>>', self.tab_changed)
        self.notebook_main.pack(fill='both', side='right', expand=True)
        # 初始化标签页内容
        self.ShowFrame = None
        self.AnalFrame = None
        self.CompFrame = None
        self.CalFrame = None
        self.ThDFrame = None
        self.all_frames = []
        # 初始化标签状态
        self.current_Frame = None

    def init(self):
        self.ShowFrame = ShowShipFrame(self.Frame_BP)
        self.AnalFrame = AnalyseFrame(self.Frame_AN)
        self.CompFrame = CompareFrame(self.Frame_CP)
        self.CalFrame = CalculatorFrame(self.Frame_CA)
        self.all_frames = [self.ShowFrame, self.AnalFrame, self.CompFrame, self.CalFrame, self.ThDFrame]
        self.current_Frame = self.all_frames[0]  # 初始化标签状态

    def tab_changed(self, event):
        if not LOADING:
            self.current_Frame = self.all_frames[event.widget.index('current')]

    def AnalFrame_animation(self):
        # 渐入，颜色加深
        ...


class BottomFrame(CodeEditor):
    """
    The bottom frame of the main window.
    """

    def __init__(self, frame, redirect=True):
        self.basic = tk.Frame(master=frame, bg='ivory', height=270, pady=10)
        self.basic.pack(side='bottom', fill='x', expand=False)
        self.basic.propagate(0)
        tk.Frame(master=self.basic, bg='ivory', width=15).pack(side='left', fill='y', expand=False)
        self.left_r_f = tk.Frame(master=self.basic, bg='ivory', width=50)
        self.left_r_f.pack(side='left', fill='y', expand=False)
        tk.Frame(master=self.basic, bg='ivory', width=10).pack(side='left', fill='y', expand=False)
        super().__init__(self.basic, redirect=redirect)
        # 右键菜单栏：
        self.menu.add_command(label='F1', command=self.F1)
        # -----------------------------------------重新绘制-----------------------------------------
        self.result.pack_forget()
        self.scroll2.pack_forget()
        self.scroll2.pack(side='right', fill='y', expand=False)
        self.result.pack(side='left', fill='both', expand=False)
        # 设置字体样式
        self.result.tag_config('_time', foreground='blue', font=("Source Code Pro", 9))
        self.result.tag_config('init', foreground='green', font=("Source Code Pro", 9))
        self.result.tag_config('receive', foreground='black', font=("Source Code Pro", 12))

    def F1(self):
        ...


class CompareFrame:
    def __init__(self, frm):
        self.basic = frm
        self.canvas = tk.Canvas(self.basic, width=800, height=600, bg=BG_COLOUR)
        self.available_designs = []
        # 检索同级目录所有头为Design的文件夹，比如Design31099等
        self.all_folders = [f for f in os.listdir(
            '.') if os.path.isdir(os.path.join('.', f)) and f.startswith('Design')]
        # 检索文件夹下的所有xml文件
        for folder in self.all_folders:
            for f in os.listdir(folder):
                if os.path.isfile(os.path.join(folder, f)) and f.endswith('.xml'):
                    self.available_designs.append(f[:-4])
        # 创建下拉框
        tk.Frame(master=self.basic, bg=BG_COLOUR, height=5).pack(side='top', fill='x', expand=False)
        self.top1 = tk.Frame(master=self.basic, bg=BG_COLOUR)
        self.top1.pack(side='top', fill='x', expand=False, pady=3)
        tk.Frame(master=self.top1, bg=BG_COLOUR, width=50).pack(side='left', fill='y', expand=False)
        self.combox = text_with_combox(
            self.top1, '选择要对比的设计:', (FONT0, FONT_SIZE), 16, 15, self.available_designs, False)
        # 添加按钮
        ttk.Style().configure("3.TButton", padding=5, relief="flat",
                              background=BG_COLOUR, foreground='firebrick', font=(FONT0, FONT_SIZE))
        self.CompareBt = ttk.Button(
            style="3.TButton", master=self.top1, text='开始对比', width=10, command=self.start)
        self.CompareBt.pack(side='right', fill='y', expand=False, padx=100)
        tk.Frame(master=self.basic, bg=BG_COLOUR2, height=3).pack(side='top', fill='x', expand=False)
        # 添加右键菜单
        self.menu = MyMenu(self.basic, {'F1': self.F1})

    def F1(self):
        ...

    def start(self):
        if self.combox.get() == '':
            messagebox.showerror('错误', '请选择要对比的设计！')
            return
        # 判断是否选择了两个不同的设计
        if self.combox.get() == GUI.Left.combox.get():
            messagebox.showerror('错误', '请选择两个不同的设计！')
            return
        # 开始对比


class AnalyseFrame:
    def __init__(self, frm):
        self.basic = frm
        # 添加右键菜单
        self.menu = MyMenu(self.basic, {'F1': self.F1})
        # 绘图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 重量分布图
        self.pltCv1 = tk.Canvas(self.basic, bg=BG_COLOUR, highlightthickness=0, width=460, height=500)
        self.pltCv1.pack(side='left', expand=True)
        self.pie1 = Plot(self.pltCv1, "重量分布图")
        # 重量分布图
        self.pltCv2 = tk.Canvas(self.basic, bg="black", highlightthickness=0, width=460, height=500)
        self.pltCv2.pack(side='left', expand=True)
        self.pie2 = Plot(self.pltCv2, "火力结构图")

    def F1(self):
        ...

    def update_plots(self):
        DR = Handler.DesignReader
        self.pie1.pie1(
            DR.WeightRelation,
            ["船体", "装甲舱增重", "装甲板", "动力系统", "火炮", "鱼雷", "防空炮", "舰载机增重", "装饰"],
            ['#ffffff', '#ffd6d0', '#ffaa99', '#99ff99', '#ffaaaa', '#aaaaff', '#aaffff', '#eeccff', '#ee00ff']
        )
        # self.pie2.pie1(
        #     DR.WeightRelation
        #
        # )


class ShowShipFrame:
    def __init__(self, frm):
        self.basic = frm
        # 读取图片，把base64编码的图片解码成可用格式
        self.bg_base64 = base64.b64decode(BG)
        self.BG1 = tk.PhotoImage(data=self.bg_base64)
        # 显示图片
        self.canvas = tk.Canvas(self.basic, width=self.BG1.width(), height=self.BG1.height(), bg=BG_COLOUR)
        self.canvas.pack(side='top', fill='both', expand=True)
        self.canvas.create_image(-215, -130, image=self.BG1, anchor='nw')
        self.menu = MyMenu(self.canvas, {'F1': self.F1})  # 添加右键菜单
        # -----------------------------------------文字-----------------------------------------
        # 覆盖图片显示文字
        self.LineH = 55
        self.StartH = 185
        self.text_dict = {
            "left": ["排水", "水线长度", "水上高度", "推进功率", "视野范围", "主炮口径", "主装厚度", "弹药供给", "实际价格"],
            "right": ["体积", "水线宽度", "吃水深度", "阻力系数", "隐蔽能力", "火力射程", "防空能力", "载机数量", "建造时间"]
        }
        for i in range(len(self.text_dict["left"])):
            _H = self.StartH + self.LineH * i
            self.canvas.create_text(
                170, _H, text=self.text_dict["left"][i], anchor='sw', font=(FONT0, 18), fill='white', tags="values")
            self.canvas.create_text(
                820, _H, text=self.text_dict["right"][i], anchor='sw', font=(FONT0, 18), fill='white', tags="values")
        # 按钮
        self.BtPos = [775, 657]
        self.Button = self.canvas.create_rectangle(
            self.BtPos[0] - 130, self.BtPos[1] - 20, self.BtPos[0] + 130, self.BtPos[1] + 20,
            outline='white', width=2)
        # 文字
        self.ButtonText = self.canvas.create_text(
            self.BtPos[0], self.BtPos[1], text="船只介绍", anchor='center', font=(FONT0, 12), fill='white')
        # 绑定事件
        self.canvas.tag_bind(self.Button, '<Button-1>', self.button_down)
        self.canvas.tag_bind(self.ButtonText, '<Button-1>', self.button_down)
        # 简介界面
        self.IntroCv = tk.Canvas(self.canvas, width=1300, height=500)
        self.IntroCv.config(scrollregion=(0, 0, 1300, 500))  # Canvas显示大小
        self.IntroCv.config(bg='white', highlightthickness=0)
        self.IntroCv.bind('<MouseWheel>', self.on_mousewheel)  # 鼠标滚轮
        # 插入图片
        self.ImgX = -340
        self.ImgY = -265
        self.IntroCv.create_image(self.ImgX, self.ImgY, image=self.BG1, anchor='nw',
                                  tags=('introduction', 'image'))

    def F1(self):
        ...

    def button_down(self, event=None):
        if self.canvas.itemcget(self.ButtonText, 'text') == '船只介绍':
            self.canvas.itemconfig(self.ButtonText, text='性能参数')
            self.canvas.itemconfig('values', state='hidden')
            self.IntroCv.place(x=775, y=135, anchor='n')
        else:
            self.canvas.itemconfig(self.ButtonText, text='船只介绍')
            self.canvas.itemconfig('values', state='normal')
            self.IntroCv.place_forget()

    def move_image(self, event=None):
        # 获取目前画布移动的位置：
        y = self.IntroCv.canvasy(1)
        # 修改图片的位置
        self.IntroCv.coords('image', self.ImgX, self.ImgY + y)

    def on_mousewheel(self, event):
        self.IntroCv.yview_scroll(-1 * int(event.delta / 120), 'units')
        self.move_image()

    @staticmethod
    def text_wrap(text, length=50):
        # 对文字进行换行处理
        text = text.split('\n')
        for i in range(len(text)):
            full = 0
            half = 0
            # 检测全角半角字符，分别计数：
            for ii in range(len(text[i])):
                if ord(text[i][ii]) > 127:
                    full += 1
                else:
                    half += 1
                if full + half > length:
                    full = 0
                    half = 0
                    # 插入换行符
                    text[i] = text[i][:ii] + '\n' + text[i][ii:]
        text = '\n'.join(text)  # 重新组合
        return text

    def update_messages(self):
        """
        更新信息
        :return:
        """
        DR = Handler.DesignReader
        # 清空信息
        self.canvas.delete('content')
        # 插入信息
        # 顶部
        try:
            self.canvas.create_text(
                self.BtPos[0], 60, text=f"{DR.ShipName}", anchor='center', font=(FONT0, 23), fill='white',
                tags=('content',))
            self.canvas.create_text(
                self.BtPos[0], 115, text=f"设计者:{DR.Designer}", anchor='center', font=(FONT0, 18), fill='white',
                tags=('content',))
        except AttributeError:
            return
        # 中间
        insert = {
            "left": [
                f"{DR.Displacement_in_t} 吨",
                f"{DR.Length_in_m} 米",
                f"{DR.Height_in_m} 米",
                f"{DR.Power} 米制马力",
                f"{DR.ViewRange} 米",
                f"{DR.MainWeapon} 毫米",
                f"{DR.MainArmor} 毫米",
                DR.Ammo,
                f"{DR.Price} 资源点"
            ],
            "right": [
                f"{DR.Volume_in_m} 立方米",
                f"{DR.Width_in_m} 米",
                f"{DR.Draft_in_m} 米",
                DR.Drag,
                f"{DR.Concealment} %",
                f"{DR.Range} 米",
                DR.AA,
                DR.Aircraft,
                f"{round(DR.SpendTime / 3600, 1)} 小时"
            ]
        }
        _W = 570
        for i in range(len(insert["left"])):  # 左边
            _H = self.StartH + self.LineH * i
            self.canvas.create_text(
                150 + _W, _H, text=insert["left"][i], anchor='se', font=(FONT0, 15), fill='white',
                tags=("content", "values"))
            self.canvas.create_text(
                800 + _W, _H, text=insert["right"][i], anchor='se', font=(FONT0, 15), fill='white',
                tags=("content", "values"))
        # 插入介绍
        text = DR.Introduction
        text = self.text_wrap(text)
        # 获取行数
        lines = text.count('\n') + 1
        if lines > 13:
            self.IntroCv.config(scrollregion=(0, 0, 1300, 500 + lines * 15))
        else:
            self.IntroCv.config(scrollregion=(0, 0, 1300, 500))
        self.move_image()
        # 删除原有的文字
        self.IntroCv.delete('content')
        self.IntroCv.create_text(
            0, 0, text=text, anchor='nw', font=(FONT0, 16), fill='white',
            tags=('content', 'introduction'))


class CalculatorFrame:
    def __init__(self, frm):
        self.basic = frm
        self.canvas = tk.Canvas(master=self.basic, bg=BG_COLOUR, width=1300, height=700, highlightthickness=0)
        self.menu = MyMenu(self.canvas, {'F1': self.F1})  # 添加右键菜单

    def F1(self):
        ...


class LeftFrame:
    """
    The left frame of the main window, which contains the entry box, the start button and the play button.
    """

    def __init__(self, frm):
        self.basic = tk.Frame(master=frm, bg=BG_COLOUR, width=320)
        self.basic.propagate(0)
        self.basic.pack(side='left', padx=15, pady=5, fill='y', expand=False)
        tk.Frame(master=self.basic, bg=BG_COLOUR, height=12).pack(side='top', fill='y', expand=False)
        self.LOGO = LOGO
        self.LOGO = tk.PhotoImage(data=self.LOGO)
        self.logo_label = tk.Label(master=self.basic, image=self.LOGO, bg=BG_COLOUR)
        self.logo_label.pack(side='top', fill='x', expand=False)
        # 检索同级目录所有头为Design的文件夹，比如Design31099等
        self.available_designs = []
        self.all_folders = [f for f in os.listdir(
            '.') if os.path.isdir(os.path.join('.', f)) and f.startswith('Design')]
        for folder in self.all_folders:  # 检索文件夹下的所有xml文件
            for f in os.listdir(folder):
                if os.path.isfile(os.path.join(folder, f)) and f.endswith('.xml'):
                    self.available_designs.append(f[:-4])
        # 创建下拉框
        self.top1 = tk.Frame(master=self.basic, bg=BG_COLOUR)
        self.top1.pack(side='top', fill='x', expand=False, pady=0)
        self.combox = text_with_combox(
            self.top1, '选择设计:', (FONT1, FONT_SIZE), 9, 15, self.available_designs, False)
        # 添加按钮
        style = ttk.Style()
        style.configure(
            "Treeview", rowheight=36, font=(FONT0, FONT_SIZE), foreground=FG_COLOUR, background=BG_COLOUR)
        style.configure("1.TButton", font=(FONT0, FONT_SIZE), foreground=FG_COLOUR, background=BG_COLOUR)
        self.button = ttk.Button(
            master=self.basic, text='读取图纸', style='1.TButton')
        self.button.pack(side='top', fill='x', expand=False, padx=15)
        # 创建2列的treeview，但是要隐藏第一行表头
        self.tree = ttk.Treeview(
            self.basic, columns=('key', 'value'), show="headings", height=13, style="Treeview")
        self.tree['show'] = ''
        self.tree.column('key', width=125, anchor='e')
        self.tree.column('value', width=165, anchor='center')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.pack(side='top', expand=False, pady=6)
        # 初始化左边栏的内容
        # 定义初始化数据
        data = [
            ('设计者ID', ''),
            ('战舰类型', ''),
            ('排水体积比', ''),
            ('长宽吃水比', ''),
            ('方形系数', ''),
            ('装甲板重量', ''),
            ('装甲舱加重', ''),
            ('火炮重量', ''),
            ('排烟器种类', ''),
            ('轮机数量', ''),
            ('轮机重量', ''),
            ('推重比', '')
        ]
        # 批量插入数据
        for item in data:
            self.tree.insert('', 'end', values=item)
        # 添加右键菜单
        self.tree_menu = MyMenu(self.tree, {
            '刷新': self.update_treeview,
            '详细信息': self.show_detail,
        })
        self.menu = MyMenu(self.basic, {'刷新': self.update_treeview})

    def show_detail(self):
        # 获取当前被选中的treeview的item
        item = self.tree.focus()
        # 如果没有选中任何item，就提示未选择
        if not item:
            messagebox.showinfo('提示', '未选择任何条目，请先单击条目至选中状态')
            return
        # 显示消息框
        item = self.tree.item(item)['values']
        text = {
            "设计者ID": "设计者ID：\n工艺战舰设计者的标识符，由注册时系统自动生成。\nID越小，说明该设计者越早注册。",
            "战舰类型": "战舰类型：\n这里的战舰类型包括特化类型。",
            "排水体积比": "排水体积比：\n战舰的排水体积与总体积的比值。该值越大，说明该设计的浮力储备越小。\n浮力储备不足时，战舰更容易被击沉。",
            "长宽吃水比": "长宽吃水比：\n战舰的长度与宽度的比值.前值越大，说明该设计的船体越细长，战舰越容易获得高速，但转向性能越差。",
            "方形系数": "方形系数：\n战舰的排水体积与水线下战舰方形体积的比值。该值越小，说明该设计的船体越扁平，战舰越容易获得高速，但稳定性越差。",
            "装甲板重量": "装甲板重量：\n战舰的装甲板总重量(吨)",
            "装甲舱加重": "装甲舱重量(皮重)：\n战舰的装甲舱总重量(吨)减相等体积的船体重量。",
            "火炮重量": "火炮重量：\n战舰的火炮总重量(吨)\n这里的火炮不包括防空炮和鱼雷发射器。",
        }
        messagebox.showinfo('详细信息', text[item[0]])

    def update_treeview(self):
        """
        更新treeview
        :return:
        """
        DR = Handler.DesignReader
        turbine_names = ''
        turbine_num = 0
        turbine_weight = 0
        # 初步处理部分数据
        if len(DR.Turbines) == 0:
            pass
        elif len(DR.Turbines) == 1:
            turbine_names = DR.Turbines[0][0]
            turbine_num = int(
                DR.Turbines[0][1]["单烟轮机数量"].split(' × ')[0]
            ) * int(
                DR.Turbines[0][1]["单烟轮机数量"].split(' × ')[1]
            )
            turbine_weight = DR.Turbines[0][1]["单烟轮机重量"]
        else:
            for i in DR.Turbines:
                turbine_names += i[0] + ' '
                turbine_num += int(
                    i[1]["单烟轮机数量"].split(' × ')[0]
                ) * int(
                    i[1]["单烟轮机数量"].split(' × ')[1]
                )
                turbine_weight += i[1]["单烟轮机重量"]
        if not DR:
            return
        # 直接修改treeview的值
        datas = [
            DR.DesignerID,
            DR.Type,
            str(DR.weight_ratio),
            str(DR.Len_Wid_Dra),
            str(DR.SquareCoefficient),
            f"{DR.armorboards_weight} t",
            f"{DR.parts_weight['装甲舱增重']} t",
            f"{DR.parts_weight['火炮']} t",
            turbine_names,
            turbine_num,
            f"{turbine_weight} t",
            f"{round(DR.HP / DR.Displacement_in_t, 3)}"
        ]
        try:
            for i in range(len(datas)):
                self.tree.set(f'I00{self.index2sixteen(i)}', 'value', datas[i])
        except AttributeError:
            pass

    @staticmethod
    def index2sixteen(index):
        """
        将索引转换为16进制
        :param index:
        :return:
        """
        index += 1
        if index < 10:
            return str(index)
        elif index == 10:
            return 'A'
        elif index == 11:
            return 'B'
        elif index == 12:
            return 'C'
        elif index == 13:
            return 'D'
        elif index == 14:
            return 'E'
        elif index == 15:
            return 'F'
        else:
            return '0'


def show_text(text, mode):
    GUI.Bottom.result.config(state='normal')
    GUI.Bottom.result.insert('end', text + '\n', mode)
    GUI.Bottom.result.config(state='disabled')


if __name__ == '__main__':
    # 初始化GUI
    LOADING = True
    GUI = TkinterGUI()
    GUI.init()
    Handler = MainHandler()
    GUI.Left.button.config(command=Handler.combox_update)
    Handler.combox_update()
    LOADING = False
    # 启动主循环
    GUI.root.mainloop()
