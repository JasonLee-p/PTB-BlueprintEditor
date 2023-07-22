# -*- coding: utf-8 -*-
"""
Created on 2023/6/24 15:00
Last Edit: 2023/7/18 15:00
Project: 工艺战舰图纸阅读器
File: main.py
Description:
    This file is the main file of PTB-BlueprintReader,
    which is a program that can read blueprint files of From the Depths.
    本文件是工艺战舰图纸阅读器的主文件，该程序可以读取来自深渊的工艺战舰图纸文件。
"""
import os
from tkinter import Tk, PhotoImage, BooleanVar, PanedWindow
from tkinter.ttk import Checkbutton as ttkCheckbutton
# 项目文件
from Data.PartAttrMaps import MainWeaponsData, PartType11
from images.Img_main import *
from images.Img_shipType import *
from images.Img_special import *
import objs.OBJS as OBJS
from utils.TkGUI import *
from utils.plt_ import *
from utils.weapon_selector import WeaponSelector
from design_reader import DesignAnalyser, ReadXML, Part, ArmorBoard, Rebar, AdvancedHull

LOCAL_ADDRESS = os.getcwd()
REDIRECT = True
VERSION = '0.0.4'


class MainHandler:
    def __init__(self):
        self.tree1 = GUI.Left.tree
        self.combox = GUI.Left.combox
        self.combox.bind('<Return>', self.combox_update)
        self.combox.bind('<Button-1>', self.combox_update)
        self.combox.bind('<MouseWheel>', self.combox_update)
        self.last_design = None
        self.DesignReader = None
        self.Analyser = None
        self.ReadingDesign = False

    def combox_update(self, event=None):
        """
        更新所有信息
        :return:
        """
        # 获取combobox的可用内容
        all_values = self.combox.cget('values')
        next_index = list(all_values).index(self.combox.get())
        # 如果是鼠标事件
        if event is not None and event.delta < 0:
            next_index -= event.delta // 120
            if next_index >= len(all_values):
                next_index = len(all_values) - 1
        elif event is not None and event.delta > 0:
            next_index -= event.delta // 120
            if next_index < 0:
                next_index = 0
        if self.last_design == all_values[next_index]:
            return
        if self.ReadingDesign:
            return
        self.ReadingDesign = True
        file_name = all_values[next_index] + '.xml'
        # 只在当前文件夹下搜索
        for folder in os.listdir(LOCAL_ADDRESS):
            if 'Design' in folder:
                path = os.path.join(LOCAL_ADDRESS, folder, file_name)
                if os.path.exists(path):
                    # 重新读取图纸
                    # 创建临时窗口
                    _win = TempTransparentWin('black')
                    # 删除上一艘图纸的所有信息
                    if self.DesignReader is not None:
                        self.DesignReader.change_ship()
                    del self.DesignReader
                    del self.Analyser
                    # 读取图纸
                    show_time()
                    show_text(f" {file_name} ", "stdout", False)
                    self.DesignReader = ReadXML(path)
                    # 获取其他信息
                    Part.get_all_information()
                    ArmorBoard.get_all_information()
                    Rebar.get_all_information()
                    # 分析部分数据
                    self.Analyser = DesignAnalyser(self.DesignReader.design)
                    # 更新所有数据
                    GUI.Left.update_treeview()
                    GUI.ShowFrame.update_messages()
                    GUI.AnalFrame.update_plots()
                    GUI.ThDFrame.update_3d()
                    self.last_design = all_values[next_index]
                    # 删除临时窗口
                    _win.destroy()
                    self.ReadingDesign = False
                    show_text(f"读取完成！", "purple", False)
                    return
        self.ReadingDesign = False
        return

    def save_data(self):
        # 打开选择器
        file_name = filedialog.asksaveasfilename(title='保存数据', filetypes=[
            ('Text', '*.txt'), ('Excel', '*.xlsx'), ('XML', '*.xml'), ('JSON', '*.json')
        ])
        if file_name == '':
            return
        # 保存数据
        self.Analyser.save_data(file_name)
        show_time()
        show_text(f" {self.Analyser.ShipName} ", "stdout", False)
        show_text(f"已保存至{file_name}！", "purple", False)


class TkinterGUI:
    def __init__(self):
        # 初始化窗口，设置透明
        self.root = Tk()
        self.root.withdraw()
        set_window(self.root, "PTB Blueprint Reader")
        # 非阻塞式渐变显示
        self.ICO = PhotoImage(data=base64.b64decode(ICO))
        self.root.iconphoto(True, self.ICO)
        # ttk水平分割条
        ttkStyle().configure('vertical.TSeparator', background=BG_COLOUR, foreground=BG_COLOUR)
        self.main_panedwindow = PanedWindow(self.root, orient='vertical', bg=BG_COLOUR2, relief='flat',
                                            sashrelief='flat', sashwidth=int(3 * RATE), sashpad=int(3 * RATE))
        self.main_panedwindow.pack(fill='both', expand=True)
        self.top_panedwindow = PanedWindow(self.main_panedwindow, orient='horizontal', bg=BG_COLOUR2, relief='flat',
                                           sashrelief='flat', sashwidth=int(3 * RATE), sashpad=int(3 * RATE))
        self.main_panedwindow.pack(fill='both', expand=True)
        self.main_panedwindow.add(self.top_panedwindow)
        # 设置panedwindow拖动范围
        # 初始化标签页
        self.Left = LeftFrame(self.top_panedwindow)
        self.top_panedwindow.add(self.Left.basic)
        self.notebook_frame = Frame(self.top_panedwindow, bg=BG_COLOUR)
        self.notebook_main = Notebook(self.notebook_frame)
        self.top_panedwindow.add(self.notebook_frame)
        self.Bottom = BottomFrame(self.main_panedwindow, redirect=REDIRECT)
        self.main_panedwindow.add(self.Bottom.basic)
        # 初始化标签页Frame
        self.Frame_BP = Frame(bg=BG_COLOUR)
        self.Frame_AN = Frame(bg=BG_COLOUR)
        self.Frame_WP = Frame(bg=BG_COLOUR)
        self.Frame_CP = Frame(bg=BG_COLOUR)
        self.Frame_CA = Frame(bg=BG_COLOUR)
        self.notebook_main.add(self.Frame_BP, text='       图纸预览       ')
        self.notebook_main.add(self.Frame_AN, text='   图纸数据分析   ')
        self.notebook_main.add(self.Frame_WP, text='   武器数据一览   ')
        self.notebook_main.add(self.Frame_CP, text='        对比器        ')
        self.notebook_main.add(self.Frame_CA, text='        计算器        ')
        # 绑定标签被选中事件
        self.notebook_main.bind('<<NotebookTabChanged>>', self.tab_changed)
        self.notebook_main.pack(fill='both', side='right', expand=True)
        # 初始化标签页内容
        self.ShowFrame = None
        self.AnalFrame = None
        self.WeaponFrame = None
        self.CompFrame = None
        self.CalFrame = None
        self.ThDFrame = None
        self.all_frames = []
        # 初始化标签状态
        self.current_Frame = None
        # 获取分辨率

    def fade_in(self):
        """
        非阻塞式渐变显示
        :return:
        """
        self.root.deiconify()
        alpha = self.root.attributes("-alpha")
        while alpha < 1:
            alpha += 0.05
            self.root.attributes("-alpha", alpha)
            time.sleep(0.01)
            self.root.update()

    def init(self):
        self.ShowFrame = ShowShipFrame(self.Frame_BP)
        self.ThDFrame = ThreeDFrame(self.ShowFrame.F1)
        self.AnalFrame = AnalyseFrame(self.Frame_AN)
        self.WeaponFrame = WeaponFrame(self.Frame_WP)
        self.CompFrame = CompareFrame(self.Frame_CP)
        self.CalFrame = CalculatorFrame(self.Frame_CA)

        self.all_frames = [
            self.ThDFrame, self.ShowFrame, self.AnalFrame, self.WeaponFrame, self.CompFrame, self.CalFrame]
        self.current_Frame = self.all_frames[0]  # 初始化标签状态
        self.root.after(100, self.fade_in)

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
        self.basic = Frame(master=frame, bg='ivory', height=int(230 * RATE), pady=int(10 * RATE))
        self.basic.pack(side='bottom', fill='x', expand=False)
        self.basic.propagate(0)
        Frame(master=self.basic, bg='ivory', width=int(15 * RATE)).pack(side='left', fill='y', expand=False)
        self.left_r_f = Frame(master=self.basic, bg='ivory', width=int(50 * RATE))
        self.left_r_f.pack(side='left', fill='y', expand=False)
        Frame(master=self.basic, bg='ivory', width=int(10 * RATE)).pack(side='left', fill='y', expand=False)
        super().__init__(self.basic, redirect=redirect)
        # 右键菜单栏：
        self.menu.add_command(label='check', command=self.check)
        # -----------------------------------------重新绘制-----------------------------------------
        self.result.pack_forget()
        self.scroll2.pack_forget()
        self.scroll2.pack(side='right', fill='y', expand=False)
        self.result.pack(side='left', fill='both', expand=False)
        # 设置字体样式
        self.result.tag_config('time', foreground='blue', font=("Source Code Pro", FONT_SIZE9))
        self.result.tag_config('init', foreground='green', font=("Source Code Pro", FONT_SIZE9))
        self.result.tag_config('blue', foreground='blue', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('red', foreground='red', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('green', foreground='green', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('yellow', foreground='yellow', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('purple', foreground='purple', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('gold', foreground='gold', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('gray', foreground='#aaaaaa', font=("Source Code Pro", FONT_SIZE12))

    def check(self):
        ...


class CompareFrame:
    def __init__(self, frm):
        self.basic = frm
        self.canvas = Canvas(self.basic, width=int(800 * RATE), height=int(600 * RATE), bg=BG_COLOUR)
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
        Frame(master=self.basic, bg=BG_COLOUR, height=int(5 * RATE)).pack(side='top', fill='x', expand=False)
        self.top1 = Frame(master=self.basic, bg=BG_COLOUR)
        self.top1.pack(side='top', fill='x', expand=False, pady=3)
        Frame(master=self.top1, bg=BG_COLOUR, width=int(50 * RATE)).pack(side='left', fill='y', expand=False)
        self.combox = text_with_combox(
            self.top1, '选择要对比的设计:', (FONT0, FONT_SIZE12), 16, 15, self.available_designs, False)
        # 添加按钮
        ttkStyle().configure("3.TButton", padding=int(5 * RATE), relief="flat",
                             background=BG_COLOUR, foreground='firebrick', font=(FONT0, FONT_SIZE12))
        self.CompareBt = ttkButton(
            style="3.TButton", master=self.top1, text='开始对比', width=int(10 * RATE), command=self.start)
        self.CompareBt.pack(side='right', fill='y', expand=False, padx=int(100 * RATE))
        Frame(master=self.basic, bg=BG_COLOUR2, height=3).pack(side='top', fill='x', expand=False)
        # 添加右键菜单
        self.menu = MyMenu(self.basic, {'show_weight_relation': self.F1})

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
        # 添加顶部船只名称显示
        self.top = Frame(master=self.basic, bg=BG_COLOUR, height=int(50 * RATE))

        self.shipName_var = StringVar()
        self.shipName_f = Label(master=self.top, textvariable=self.shipName_var, bg=BG_COLOUR,
                                font=(FONT0, FONT_SIZE18))
        self.show_img_button = ttkButton(
            style="3.TButton", master=self.top, text='查看吨位比关系图', width=14, command=self.show_weight_relation)
        # 可拖动分割线
        self.p_window = PanedWindow(self.basic, orient='vertical', bg=BG_COLOUR, relief='flat',
                                    showhandle=True, sashrelief='raised', sashwidth=int(5 * RATE))
        # 重量分布图
        self.top2 = Frame(master=self.p_window, bg=BG_COLOUR2)
        self.pltCv1 = Canvas(self.top2, bg=BG_COLOUR2, highlightthickness=0, width=int(470 * RATE),
                             height=int(520 * RATE))
        self.pie1 = Plot(self.pltCv1, "重量分布图")
        # 重量分布图
        self.pltCv2 = Canvas(self.top2, bg=BG_COLOUR2, highlightthickness=0, width=int(470 * RATE),
                             height=int(520 * RATE))
        self.pie2 = Plot(self.pltCv2, "火力结构图")
        # 火炮投射量
        self.pltCv3 = Canvas(self.top2, bg=BG_COLOUR2, highlightthickness=0, width=int(470 * RATE),
                             height=int(520 * RATE))
        self.bar1 = Plot(self.pltCv3, "火炮投射量", type_='bar')
        self.pop_wedge = None
        # 底部
        self.bottom = Frame(master=self.p_window, bg=BG_COLOUR)
        self.analyseReport = StringVar()
        self.analyseReportS = Label(master=self.bottom, textvariable=self.analyseReport, bg=BG_COLOUR,
                                    font=(FONT0, 8))
        # 添加右键菜单
        self.menu0 = MyMenu(self.top2, {'查看吨位比例关系图': self.show_weight_relation})
        self.menu1 = MyMenu(self.pltCv1, {'查看吨位比例关系图': self.show_weight_relation})
        self.weight_img = WEIGHT
        self.weight_img = PhotoImage(data=base64.b64decode(self.weight_img))
        # 创建顶级窗口
        self.top2_top = Toplevel()
        self.top2_top.withdraw()
        self.top2_top.title('吨位比例关系图')
        self.top2_top.geometry('1000x660')
        self.top2_top.resizable(False, False)
        self.top2_top.protocol("WM_DELETE_WINDOW", self.top2_top.withdraw)
        Label(master=self.top2_top, image=self.weight_img, bg=BG_COLOUR2).pack(side='top', fill='both', expand=True)
        self.init_frame()

    def init_frame(self):
        self.top.pack(side='top', fill='x', expand=False, pady=3)
        self.top.propagate(0)
        Frame(master=self.top, bg=BG_COLOUR, width=int(130 * RATE)).pack(side='left', fill='y', expand=False)
        self.show_img_button.pack(side='right', fill='y', expand=False)
        self.shipName_f.pack(side='left', fill='y', expand=True, padx=int(10 * RATE), pady=int(5 * RATE))
        self.p_window.pack(side='left', fill='both', expand=True)
        # 添加中间的分割线
        Frame(master=self.basic, bg=BG_COLOUR2, height=int(5 * RATE)).pack(side='top', fill='x', expand=False)
        # 绘图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.top2.pack(side='top', fill='x', expand=False, pady=0)
        Frame(master=self.top2, bg=BG_COLOUR2, width=int(30 * RATE)).pack(side='right', fill='y', expand=False)
        self.pltCv1.pack(side='left', expand=True)
        self.pltCv2.pack(side='left', expand=True)
        self.pltCv3.pack(side='left', expand=True)
        self.p_window.add(self.top2)
        self.p_window.add(self.bottom)
        # 分析报告
        Label(master=self.bottom, text=' 分析简报 ', bg=BG_COLOUR, font=(FONT0, FONT_SIZE12)).pack(
            side='top', fill='x', expand=False, padx=int(30 * RATE), pady=0)
        self.analyseReportS.pack(side='top', fill='x', expand=False, padx=int(30 * RATE), pady=0)
        self.analyseReport.set(
            '（~敬请期待~）\n'
        )
        self.basic.update()

    def show_weight_relation(self):
        self.top2_top.deiconify()

    def update_plots(self):
        ANLS = Handler.Analyser
        if Handler.DesignReader.design['ShipCard'] == {}:
            ANLS.ShipName = '未知'
            ANLS.weight_relation_data = {"船体": 1, "装甲舱增重": 0, "装甲板": 0, "动力系统": 0, "火炮": 0, "鱼雷": 0, "防空炮": 0,
                                         "舰载机增重": 0, "装饰": 0}
            ANLS.right_frame0_data1 = {"主炮耗弹": 1, "副炮耗弹": 0, "鱼雷耗弹": 0, "防空炮耗弹": 0}
            ANLS.right_frame0_data2 = {'无': 0}
            ANLS.right_frame0_data3 = {'无': 0}
        self.shipName_var.set(ANLS.ShipName)
        self.pie1.pie1(
            ANLS.weight_relation_data,
            ["船体", "装甲舱增重", "装甲板", "动力系统", "火炮", "鱼雷", "防空炮", "舰载机增重", "装饰"],
            ['#ffffff', '#ffd6d0', '#ffaa99', '#99ff99', '#ffaaaa', '#aaaaff', '#aaffff', '#eeccff', '#ee00ff']
        )
        self.pie2.pie1(
            ANLS.right_frame0_data1,
            ["主炮耗弹", "副炮耗弹", "鱼雷耗弹", "防空耗弹"],
            ['#ffaaaa', '#ffd6d0', '#aaaaff', '#aaffff'],
            show_threshold=0.01,
            show_value=True
        )
        self.bar1.bar1(
            ANLS.right_frame0_data2.keys(),
            [ANLS.right_frame0_data2.values(), ANLS.right_frame0_data3.values()],
            colors=[]
        )


class WeaponFrame:
    def __init__(self, frm):
        self.basic = frm
        self.notebook = Notebook(self.basic)
        self.notebook.pack(side='top', fill='both', expand=True)
        self.F1 = Frame(bg=BG_COLOUR)
        self.F2 = Frame(bg=BG_COLOUR)
        self.notebook.add(self.F1, text='                单武器性能                ')
        self.notebook.add(self.F2, text='              武器数据对比              ')
        # --------------------------------------------------------------------------- 单武器性能 show_weight_relation
        self.right = Frame(master=self.F1, bg=BG_COLOUR, width=int(460 * RATE))
        self.Selector = WeaponSelector(self.right, side='top', fill='x', expand=False, padx=5, pady=8)
        self.tree = Treeview(
            self.right, columns=('key', 'value', 'unit'), show="headings", height=12, style="Treeview")
        # 添加右键菜单
        self.tree_menu = MyMenu(self.tree, {'刷新': self.update_treeview})
        self.menu = MyMenu(self.basic, {'刷新': self.update_treeview})
        # 初始化右侧的Frame
        self.init_right_frame()
        self.left = Frame(master=self.F1, bg=BG_COLOUR)
        self.left.pack(side='left', fill='both', expand=True)
        self.plt3dFrame = Canvas(self.left, bg=BG_COLOUR, highlightthickness=0, width=int(1000 * RATE),
                                 height=int(685 * RATE))
        self.plt3dFrame.pack(side='top', expand=False)
        self.plt3d = Plot3D(self.plt3dFrame, None, figsize=(10, 10), place=(int(500 * RATE), int(-300 * RATE)), dpi=100)
        self.plt3d.plot_obj(eval("OBJS.O111000300_LOD"))
        # --------------------------------------------------------------------------- 武器数据对比 F2

    def init_right_frame(self):
        self.right.pack(side='right', fill='y', expand=False)
        self.Selector.tree.bind('<ButtonRelease-1>', self.update_treeview)
        self.tree['show'] = ''
        self.tree.column('key', width=int(210 * RATE), anchor='e')  # e 是右对齐
        self.tree.column('value', width=int(240 * RATE), anchor='center')
        self.tree.column('unit', width=int(80 * RATE), anchor='w')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.heading('unit', text="", anchor="e")
        self.tree.pack(side='top', expand=False, pady=int(6 * RATE))
        data = [
            ('装填', '0', 's'),
            ('射程', '0', 'km'),
            ('炮塔转速', '0', 'r/m'),
            ('出膛速度', '0', 'm/s'),
            ('最长炮弹飞行时间', '0', 's'),
            ('最大仰角', '0', 'deg'),
            ('武器散布', '0', 'm/km'),
            ('炮弹重量', '0', 'kg'),
            ('弹药用量', '0', '个'),
            ('5-15-25-35km穿深', '0 / 0 / 0 / 0', 'mm'),
            ('推荐数量', '0', '个'),
        ]
        # 批量插入数据
        for item in data:
            self.tree.insert('', 'end', values=item)

    def update_treeview(self, event=None):
        """
        更新treeview
        :return:
        """
        if self.Selector.selectedName == '':
            return
        try:
            _data = MainWeaponsData[self.Selector.selectedName]
        except KeyError:
            show_time()
            show_text(f' 未找到{self.Selector.selectedName}的数据', 'stderr', False)
            return
        # 把13到16合并为一个字符串
        _data = [
            _data[2], _data[3], _data[4], _data[5], _data[6], _data[7], _data[8], _data[10], _data[12],
            f"{int(_data[13])} / {int(_data[14])} / {int(_data[15])} / {int(_data[16])}", int(_data[17])
        ]
        for i in range(len(_data)):
            self.tree.set(f'I00{LeftFrame.index2sixteen(i)}', 'value', _data[i])
        # 更新3D图
        # 获取PartType11的值键字典
        part_type11_dict = {v: k for k, v in PartType11.items()}
        _id = part_type11_dict[self.Selector.selectedName]
        # 在文件夹下寻找含有该字样的文件
        smallest = None
        # 在OBJS包下面寻找其所有变量名：
        for obj in OBJS.ALL:
            if _id in obj:
                if _id[2] in "0":
                    if not smallest:
                        smallest = obj
                    elif len(eval(f"OBJS.{smallest}")) > len(eval(f"OBJS.{obj}")):
                        smallest = obj
                elif _id[2] in "2":  # 鱼雷武器
                    pass
        if not smallest:
            show_time()
            show_text(f' 找不到3D文件位置', 'stderr', False)
            return
        self.plt3d.plot_obj(eval(f"OBJS.{smallest}"))


class ShowShipFrame:
    def __init__(self, frm):
        self.basic = frm
        self.notebook = Notebook(self.basic, height=int(680 * RATE))
        self.notebook.pack(side='top', fill='x', expand=False)
        self.F1 = Frame(self.notebook, bg=BG_COLOUR2)
        self.F2 = Frame(self.notebook, bg=BG_COLOUR)
        self.notebook.add(self.F1, text='                   3D预览                   ')
        self.notebook.add(self.F2, text='                   信息查看                   ')
        # 读取图片，把base64编码的图片解码成可用格式
        self.bg_base64 = base64.b64decode(BG)
        self.BG1 = PhotoImage(data=self.bg_base64)
        # 显示图片
        self.canvas = Canvas(self.F2, width=int(1600 * RATE), height=int(700 * RATE), bg=BG_COLOUR)
        self.canvas.pack(anchor='nw')
        self.canvas.create_image(int(-215 * RATE), int(-130 * RATE), image=self.BG1, anchor='nw')
        self.menu = MyMenu(self.canvas, {'show_weight_relation': self.F1})  # 添加右键菜单
        # -----------------------------------------文字-----------------------------------------
        # 覆盖图片显示文字
        self.LineH = int(55 * RATE)
        self.StartH = int(182 * RATE)
        self.text_dict = {
            "left": ["排水", "水线长度", "水上高度", "推进功率", "视野范围", "主炮口径", "主装厚度", "弹药供给", "实际价格"],
            "right": ["体积", "水线宽度", "吃水深度", "阻力系数", "隐蔽能力", "火力射程", "防空能力", "载机数量", "建造时间"]
        }
        for i in range(len(self.text_dict["left"])):
            _H = self.StartH + self.LineH * i
            self.canvas.create_text(
                int(170 * RATE), _H, text=self.text_dict["left"][i], anchor='sw', font=(FONT0, FONT_SIZE18),
                fill='white', tags="values")
            self.canvas.create_text(
                int(820 * RATE), _H, text=self.text_dict["right"][i], anchor='sw', font=(FONT0, FONT_SIZE18),
                fill='white', tags="values")
        # 按钮
        self.BtPos = [int(775 * RATE), int(647 * RATE)]
        self.Button = self.canvas.create_rectangle(
            self.BtPos[0] - int(130 * RATE), self.BtPos[1] - int(20 * RATE), self.BtPos[0] + int(130 * RATE),
            self.BtPos[1] + int(20 * RATE),
            outline='white', width=2)
        # 文字
        self.ButtonText = self.canvas.create_text(
            self.BtPos[0], self.BtPos[1], text="船只介绍", anchor='center', font=(FONT0, FONT_SIZE12), fill='white')
        # 绑定事件
        self.canvas.tag_bind(self.Button, '<Button-1>', self.button_down)
        self.canvas.tag_bind(self.ButtonText, '<Button-1>', self.button_down)
        # 简介界面
        self.intro_cv_width = int(1300 * RATE)
        self.intro_cv_height = int(490 * RATE)
        self.IntroCv = Canvas(self.canvas, width=self.intro_cv_width, height=self.intro_cv_height)
        self.IntroCv.config(scrollregion=(0, 0, self.intro_cv_width, self.intro_cv_height))  # Canvas显示大小
        self.IntroCv.config(bg='white', highlightthickness=0)
        self.IntroCv.bind('<MouseWheel>', self.on_mousewheel)  # 鼠标滚轮
        # 插入图片
        self.ImgX = int(-340 * RATE)
        self.ImgY = int(-265 * RATE)
        self.IntroCv.create_image(self.ImgX, self.ImgY, image=self.BG1, anchor='nw',
                                  tags=('introduction', 'image'))

    def F1(self):
        ...

    def button_down(self, event=None):
        if self.canvas.itemcget(self.ButtonText, 'text') == '船只介绍':
            self.canvas.itemconfig(self.ButtonText, text='性能参数')
            self.canvas.itemconfig('values', state='hidden')
            self.IntroCv.place(x=int(775 * RATE), y=int(135 * RATE), anchor='n')
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
    def text_wrap(text, length=48):
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
        ANLS = Handler.Analyser
        DR = Handler.DesignReader
        # 清空信息
        self.canvas.delete('content')
        # 插入信息
        # 顶部
        try:
            self.canvas.create_text(
                self.BtPos[0], int(57 * RATE), text=f"{ANLS.ShipName}", anchor='center', font=(FONT0, FONT_SIZE22),
                fill='white',
                tags=('content',))
            self.canvas.create_text(
                self.BtPos[0], int(112 * RATE), text=f"设计者:{ANLS.Designer}", anchor='center', font=(FONT0, FONT_SIZE18),
                fill='white',
                tags=('content',))
        except AttributeError:
            return
        # 中间
        insert = ANLS.right_frame0_data
        _W = int(570 * RATE)
        for i in range(len(insert["left"])):  # 左边
            _H = self.StartH + self.LineH * i
            self.canvas.create_text(
                int(150 * RATE) + _W, _H, text=insert["left"][i], anchor='se', font=(FONT0, FONT_SIZE14), fill='white',
                tags=("content", "values"))
            self.canvas.create_text(
                int(800 * RATE) + _W, _H, text=insert["right"][i], anchor='se', font=(FONT0, FONT_SIZE14), fill='white',
                tags=("content", "values"))
        # 插入介绍
        text = DR.design["CopyWriting"]
        text = self.text_wrap(text)
        # 获取行数
        lines = text.count('\n') + 1
        if lines > 13:
            self.IntroCv.config(scrollregion=(0, 0, self.intro_cv_width, self.intro_cv_height + lines * 15))
        else:
            self.IntroCv.config(scrollregion=(0, 0, self.intro_cv_width, self.intro_cv_height))
        self.move_image()
        # 删除原有的文字
        self.IntroCv.delete('content')
        self.IntroCv.create_text(
            0, 0, text=text, anchor='nw', font=(FONT0, FONT_SIZE16), fill='white',
            tags=('content', 'introduction'))


class CalculatorFrame:
    def __init__(self, frm):
        self.basic = frm
        self.canvas = Canvas(master=self.basic, bg=BG_COLOUR, width=int(1300 * RATE), height=int(700 * RATE),
                             highlightthickness=0)
        self.menu = MyMenu(self.canvas, {'show_weight_relation': self.F1})  # 添加右键菜单

    def F1(self):
        ...


class ThreeDFrame:
    def __init__(self, frm):
        self.basic = frm
        # 3D预览右侧
        self.right = Frame(self.basic, bg=BG_COLOUR, highlightthickness=0, width=int(260 * RATE))
        self.right.pack(side='right', fill='y', expand=False, padx=0)
        self.right.propagate(False)
        # 3D预览
        self.plt3dFrame = Canvas(self.basic, bg=BG_COLOUR2, highlightthickness=0, width=int(1300 * RATE),
                                 height=int(700 * RATE))
        self.plt3dFrame.pack(side='left', expand=False)
        self.plt3dFrame.propagate(False)
        self.plt3d = Plot3D(self.plt3dFrame, None, figsize=(12, 12), place=(int(650 * RATE), int(-350 * RATE)), dpi=DPI)
        self.plt3d.set_axes_preset([-10, 10], [-10, 10], [-10, 10], False, False, False)
        """
        -------------------------------------------------筛选框------------------------------------------------
        """
        self.filter = Frame(self.right, bg=BG_COLOUR)
        self.all_hull = BooleanVar()
        self.all_hull.set(True)
        self.all_add_hull = BooleanVar()
        self.all_add_hull.set(True)
        self.add_hull_filter = Frame(self.filter, bg=BG_COLOUR, highlightthickness=0)
        self.filter_left = Frame(self.filter, bg=BG_COLOUR, highlightthickness=0)
        self.filter_right = Frame(self.filter, bg=BG_COLOUR, highlightthickness=0)
        # 绘制筛选栏
        self.vars = {"船体": BooleanVar(), "装甲舱": BooleanVar(),
                     "弹药库": BooleanVar(), "机库": BooleanVar(),
                     "主武器": BooleanVar(), "防空炮": BooleanVar(),
                     "动力组": BooleanVar(),
                     "装饰": BooleanVar(),
                     "进阶船壳": BooleanVar()}
        for part_type, bool_ in self.vars.items():
            bool_.set(True)
        self.last_bool = dict([(part_type, True) for part_type in self.vars.keys()])
        self.last_ship = None
        self.filter_frame()
        """
        -------------------------------------------------操作栏------------------------------------------------
        """
        self.operation_frame()
        """
        -------------------------------------------------信息------------------------------------------------
        """
        self.menu = MyMenu(self.plt3dFrame, {'查看图例': self.show_legend})  # 添加右键菜单
        self.update_3d()

    def filter_frame(self):
        self.filter.pack(side='top', fill='both', expand=False)
        Frame(self.filter, bg=BG_COLOUR2, height=int(10 * RATE)).pack(side='top', fill='x', expand=False)
        Frame(self.filter, bg=BG_COLOUR2, height=int(10 * RATE)).pack(side='bottom', fill='x', expand=False)
        Label(self.filter, text='筛选栏', bg=BG_COLOUR, fg='black', font=(FONT0, FONT_SIZE16)
              ).pack(side='top', expand=False, fill='x', pady=0)
        # 所有船体筛选（顶部）
        Frame(self.filter, bg=BG_COLOUR2, height=4).pack(side='top', fill='x', expand=False)
        ttkStyle().configure("TCheckbutton", background=BG_COLOUR, foreground='black', font=(FONT0, FONT_SIZE12))
        ttkCheckbutton(self.filter, text='所有普通零件', variable=self.all_hull, onvalue=True, offvalue=False,
                       command=lambda: self.update_all(), style='TCheckbutton'
                       ).pack(side='top', expand=True, pady=0)
        Frame(self.filter, bg=BG_COLOUR2, height=2).pack(side='top', fill='x', expand=False)
        # 进阶船壳筛选（底部）
        self.add_hull_filter.pack(side='bottom', fill='x', expand=False)
        Frame(self.add_hull_filter, bg=BG_COLOUR2, height=4).pack(side='top', fill='x', expand=False)
        ttkCheckbutton(self.add_hull_filter, text='所有进阶船壳', variable=self.all_add_hull, onvalue=True, offvalue=False,
                       command=lambda: self.update_all(), style='TCheckbutton'
                       ).pack(side='top', expand=True, pady=0)
        Frame(self.add_hull_filter, bg=BG_COLOUR2, height=2).pack(side='top', fill='x', expand=False)
        # 普通零件筛选（顶部）
        self.filter_left.pack(side='left', fill='y', expand=True)
        self.filter_right.pack(side='left', fill='y', expand=True)
        # 创建多选框并绑定函数
        for part_type, bool_ in self.vars.items():
            if part_type in ["进阶船壳"]:
                checkbox = ttkCheckbutton(self.add_hull_filter, text=part_type, variable=bool_,
                                          command=lambda: self.update_3d())
                checkbox.pack()
                break
            elif part_type in ["船体", "装甲舱", "弹药库", "机库"]:
                checkbox = ttkCheckbutton(self.filter_left, text=part_type, variable=bool_,
                                          command=lambda: self.update_3d())
            else:
                checkbox = ttkCheckbutton(self.filter_right, text=part_type, variable=bool_,
                                          command=lambda: self.update_3d())
            checkbox.pack(anchor='w', expand=False)

    def operation_frame(self):
        ...

    def update_all(self):
        show_time()
        show_text(" 预览  ", "blue", False)
        if self.all_hull.get():
            for part_type, bool_ in self.vars.items():
                bool_.set(True)
            show_text("所有零件—", "stdout", False)
        else:
            for part_type, bool_ in self.vars.items():
                bool_.set(False)
            show_text("所有零件—", "gray", False)
        if self.all_add_hull.get():
            self.vars["进阶船壳"].set(True)
            show_text("进阶船壳", "stdout", False)
        else:
            self.vars["进阶船壳"].set(False)
            show_text("进阶船壳", "gray", False)
        self.update_3d()

    def update_3d(self, event=None):
        try:
            if self.last_ship == Handler.DesignReader.design['ShipCard']:
                for part_type, bool_ in self.vars.items():
                    if not bool_.get():
                        self.plt3d.hide_part(part_type)
                    else:
                        self.plt3d.show_part(part_type)
                return
            self.last_ship = Handler.DesignReader.design['ShipCard']
            part_data = Handler.DesignReader.design["Parts"]
            shipCard = Handler.DesignReader.design['ShipCard']
            try:
                length = shipCard["Length"]
                width = shipCard["Width"]
                height = shipCard["Height"]
            except KeyError:
                length = 10
                width = 10
                height = 10
            ship_size = (
                [-length / 2, length / 2],
                [-width / 2, width / 2],
                [-height / 2, height / 2]
            )
        except AttributeError and NameError:
            part_data = None
            ship_size = [10, 10, 10]
        try:
            hull_data = AdvancedHull.currentHull.SlicesPoints
            hull_pos = AdvancedHull.currentHull.Position
        except AttributeError:
            hull_data = None
            hull_pos = None
        # 永久清空所有图像：
        self.plt3d.clear()
        self.plt3d.draw_ship(
            hull_data, hull_pos,
            None,
            None,
            part_data, ship_size
        )
        for part_type, bool_ in self.vars.items():
            if not bool_.get():
                self.plt3d.hide_part(part_type)
            else:
                self.plt3d.show_part(part_type)

    def show_legend(self):
        ...


class LeftFrame:
    """
    The left frame of the main window, which contains the entry box, the start button and the play button.
    """

    def __init__(self, frm):
        self.basic = Frame(master=frm, bg=BG_COLOUR, width=int(320 * RATE))
        self.basic.pack(side='left', padx=int(15 * RATE), pady=5, fill='y', expand=False)
        self.basic.propagate(0)
        Frame(master=self.basic, bg=BG_COLOUR, height=12).pack(side='top', fill='y', expand=False)
        self.LOGO = LOGO
        self.LOGO = PhotoImage(data=self.LOGO)
        self.logo_label = Label(master=self.basic, image=self.LOGO, bg=BG_COLOUR)
        self.logo_label.pack(side='top', fill='x', expand=False, pady=10)
        # 检索同级目录所有头为Design的文件夹，比如Design31099等
        self.available_designs = []
        self.all_folders = [f for f in os.listdir(
            '.') if os.path.isdir(os.path.join('.', f)) and f.startswith('Design')]
        for folder in self.all_folders:  # 检索文件夹下的所有xml文件
            for f in os.listdir(folder):
                if os.path.isfile(os.path.join(folder, f)) and f.endswith('.xml'):
                    self.available_designs.append(f[:-4])
        # 创建下拉框
        self.top1 = Frame(master=self.basic, bg=BG_COLOUR)
        self.top1.pack(side='top', expand=False, pady=0)
        self.combox = text_with_combox(
            self.top1, ' 选择设计:', (FONT1, FONT_SIZE12), 10, 65, self.available_designs, False)
        # 添加按钮
        style = ttkStyle()
        style.configure(
            "Treeview", rowheight=int(36 * RATE), font=(FONT0, FONT_SIZE12), foreground=FG_COLOUR, background=BG_COLOUR)
        style.configure("1.TButton", font=(FONT0, FONT_SIZE12), foreground=FG_COLOUR, background=BG_COLOUR)
        self.button = ttkButton(
            master=self.basic, text='读取图纸', style='1.TButton', width=25)
        self.button.pack(side='top', expand=False, padx=int(15 * RATE))
        # 船只类型显示栏
        Frame(master=self.basic, bg=BG_COLOUR, height=5).pack(side='top', fill='x', expand=False)
        self.top2 = Frame(master=self.basic, bg=BG_COLOUR)
        self.top2.pack(side='top', fill='x', expand=False, pady=0)
        # 初始化显示的图片变量
        _UNKNOWN = PhotoImage(data=UNKNOWN)
        _UB = PhotoImage(data=UB)
        _CS = PhotoImage(data=CS)
        _DD = PhotoImage(data=DD)
        _CL = PhotoImage(data=CL)
        _CA = PhotoImage(data=CA)
        _BM = PhotoImage(data=BM)
        _BC = PhotoImage(data=BC)
        _BB = PhotoImage(data=BB)

        # 所有船只类型的图片
        self.type_map = {
            "未知": _UNKNOWN, "UB": _UB, "CS": _CS, "DD": _DD, "CL": _CL, "CA": _CA, "BM": _BM, "BC": _BC, "BB": _BB,
        }
        # 所有特化类型的图片
        _DefaultS = PhotoImage(data=DefaultS)
        _MainS = PhotoImage(data=MainS)
        _ViceS = PhotoImage(data=ViceS)
        _TorpedoS = PhotoImage(data=TorpedoS)
        _AAS = PhotoImage(data=AAS)
        _PlaneS = PhotoImage(data=PlaneS)
        _Plane1S = PhotoImage(data=Plane1S)
        _Plane2S = PhotoImage(data=Plane2S)
        _HeavyS = PhotoImage(data=HeavyS)
        _DefenceS = PhotoImage(data=DefenceS)
        _SpeedS = PhotoImage(data=SpeedS)
        _ModernS = PhotoImage(data=ModernS)
        _ProductS = PhotoImage(data=ProductS)

        self.special_map = {
            "未知": _DefaultS, "DF": _DefaultS, "MW": _MainS, "SW": _ViceS, "TR": _TorpedoS, "AA": _AAS,
            "CR": _PlaneS, "CRI": _Plane1S, "CRII": _Plane2S, "HS": _HeavyS, "PT": _DefenceS, "MT": _SpeedS,
            "MD": _ModernS, "LG": _ProductS
        }
        # 创建显示图片的label
        Frame(master=self.top2, bg=BG_COLOUR, width=int(20 * RATE)).pack(side='right', fill='y', expand=False)
        self.special = Label(image=self.special_map['未知'], master=self.top2, bg='black')
        self.special.pack(side='right', fill='x', expand=False, padx=int(5 * RATE))
        self.ship_type = Label(image=self.type_map['未知'], master=self.top2, bg=BG_COLOUR)
        self.ship_type.pack(side='right', fill='x', expand=False, padx=5)
        # 创建2列的treeview，但是要隐藏第一行表头
        self.tree = Treeview(
            self.basic, columns=('key', 'value'), show="headings", height=int(13 * RATE), style="Treeview")
        self.tree['show'] = ''
        self.tree.column('key', width=int(120 * RATE), anchor='e')
        self.tree.column('value', width=int(170 * RATE), anchor='center')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.pack(side='top', expand=False, pady=int(6 * RATE))
        # 保存数据按钮
        self.button2 = ttkButton(
            master=self.basic, text='保存信息', style='1.TButton', width=25)
        self.button2.pack(side='top', expand=False, padx=int(15 * RATE))
        # 初始化左边栏的内容
        # 定义初始化数据
        data = [
            ('设计者ID', ''),
            ('排水体积比', ''),
            ('长宽吃水比', ''),
            ('方形系数', ''),
            ('装甲板重量', ''),
            ('装甲舱增重', ''),
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
        # 事件管理
        self.last_ship_type = '未知'
        self.last_ship_special = '未知'

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
            # "战舰类型": "战舰类型：\n这里的战舰类型包括特化类型。",
            "排水体积比": "排水体积比：\n战舰的排水体积与总体积的比值。该值越大，说明该设计的浮力储备越小。\n浮力储备不足时，战舰更容易被击沉。",
            "长宽吃水比": "长宽吃水比：\n战舰的长度与宽度的比值.前值越大，说明该设计的船体越细长，战舰越容易获得高速，但转向性能越差。",
            "方形系数": "方形系数：\n战舰的排水体积与水线下战舰方形体积的比值。该值越小，说明该设计的船体越扁平，战舰越容易获得高速，但稳定性越差。",
            "装甲板重量": "装甲板重量：\n战舰的装甲板总重量(吨)",
            "装甲舱增重": "装甲舱重量(皮重)：\n战舰的装甲舱总重量(吨)减相等体积的船体重量。",
            "火炮重量": "火炮重量：\n战舰的火炮总重量(吨)\n这里的火炮不包括防空炮和鱼雷发射器。",
            "排烟器种类": "排烟器种类：\n战舰的排烟器种类。",
            "轮机数量": "轮机数量：\n战舰的轮机数量。",
            "轮机重量": "轮机重量：\n战舰的轮机总重量(吨)",
            "推重比": "推重比：\n战舰的推重比，即战舰的推进力与战舰的总重量的比值。一般该值越大，说明该战舰越容易获得高速。"
        }
        messagebox.showinfo('详细信息', text[item[0]])

    def update_treeview(self):
        """
        更新treeview
        :return:
        """
        ANLS = Handler.Analyser
        if Handler.DesignReader.design['ShipCard'] == {}:
            for i in range(11):
                self.tree.set(f'I00{self.index2sixteen(i)}', 'value', '未知')
                return
        if ANLS.ShipType != self.last_ship_type:
            self.ship_type.config(image=self.type_map[ANLS.ShipType])
            self.last_ship_type = ANLS.ShipType
        if ANLS.ShipSpecial != self.last_ship_special:
            try:
                self.special.config(image=self.special_map[ANLS.ShipSpecial])
            except KeyError:
                show_text(f'遇到未知的特化类型：{ANLS.ShipSpecial}   敬请联系作者补全信息~\n'
                          f'', 'error')
            self.last_ship_special = ANLS.ShipSpecial
        _data = list(ANLS.left_frame_data.values())
        for i in range(len(_data)):
            self.tree.set(f'I00{self.index2sixteen(i)}', 'value', _data[i])

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


def show_text(text, mode, change_line=True):
    GUI.Bottom.result.config(state='normal')
    if not change_line:
        GUI.Bottom.result.delete('end-1c linestart', 'end')
    GUI.Bottom.result.insert('end', text + '\n', mode)
    GUI.Bottom.result.config(state='disabled')
    # 更新到最新的消息
    GUI.Bottom.result.see('end')


def show_time():
    GUI.Bottom.result.config(state='normal')
    GUI.Bottom.result.insert('end', f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n', 'time')
    GUI.Bottom.result.config(state='disabled')


if __name__ == '__main__':
    # 初始化GUI
    LOADING = True
    GUI = TkinterGUI()
    GUI.init()
    Handler = MainHandler()
    GUI.Left.button.config(command=Handler.combox_update)
    GUI.Left.button2.config(command=Handler.save_data)
    Handler.combox_update()
    LOADING = False
    # 启动主循环
    GUI.root.mainloop()
    # 存入数据：
    DesignAnalyser.store_data(DesignAnalyser.ALL_SHIP)
