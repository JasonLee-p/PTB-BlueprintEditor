# -*- coding: utf-8 -*-
"""
Created on 2023/6/24 15:00
Project: PTB
File: main.py

    This file is the main file of PTB-BlueprintReader.
"""
import base64
from IMGS import *
from TkGUI import *
from xml_reader import *


class MainHandler:
    def __init__(self):
        self.tree1 = GUI.Left.tree
        self.combox = GUI.Left.combox
        self.combox.box.bind('<<ComboboxSelected>>', self.combox_update)
        self.combox.box.bind('<Return>', self.combox_update)
        self.combox.box.bind('<Leave>', self.combox_update)
        self.combox.box.bind('<FocusOut>', self.combox_update)
        self.last_design = None
        self.DesignReader = None

    def combox_update(self, event):
        """
        更新所有信息
        :return:
        """
        if self.last_design == self.combox.box.get():
            return
        file_name = self.combox.box.get() + '.xml'
        # 在同目录下寻找有Design字样的文件夹:
        for root, dirs, files in os.walk(os.path.abspath('.')):
            for _dir in dirs:
                if 'Design' in _dir:
                    path = os.path.join(root, _dir, file_name)
                    if os.path.exists(path):
                        self.DesignReader = ReadDesign(path)
                        GUI.Left.update_treeview()
                        GUI.ShowFrame.update_messages()
                        self.last_design = self.combox.box.get()
                        return


class TkinterGUI:
    def __init__(self):
        self.root = tk.Tk()
        set_window(self.root, "PTB Blueprint Reader")
        # 检查是否有图标文件
        self.ICO_PATH = os.path.join(os.path.abspath('.'), 'PTB.ico')
        if not os.path.exists(self.ICO_PATH):
            # 设置窗口图标
            self.ICO = base64.b64decode(ICO)
            # 把图标写入文件
            with open(self.ICO_PATH, 'wb') as f:
                f.write(self.ICO)
        # 设置窗口图标
        self.root.iconbitmap(self.ICO_PATH)
        # notebook
        self.notebook_main = ttk.Notebook(self.root)
        self.Bottom = BottomFrame(self.root, redirect=False)
        self.Left = LeftFrame(self.root)
        # 初始化标签页
        self.Frame_BP = tk.Frame(bg=BG_COLOUR)
        self.Frame_CP = tk.Frame(bg=BG_COLOUR)
        self.Frame_CA = tk.Frame(bg=BG_COLOUR)
        self.Frame_3D = tk.Frame(bg=BG_COLOUR)
        self.notebook_main.add(self.Frame_BP, text='   图纸详细信息   ')
        self.notebook_main.add(self.Frame_CP, text='        对比器        ')
        self.notebook_main.add(self.Frame_CA, text='        计算器        ')
        self.notebook_main.add(self.Frame_3D, text='       3D预览       ')
        self.notebook_main.pack(fill='both', side='right', expand=True)
        self.ShowFrame = None
        self.CompFrame = None
        self.CalFrame = None

    def init(self):
        self.ShowFrame = ShowShipFrame(self.Frame_BP)
        self.CompFrame = CompareFrame(self.Frame_CP)
        self.CalFrame = CalculatorFrame(self.Frame_CA)


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
        self.combox = text_with_combox(
            self.top1, '选择要对比的设计:', (FONT0, FONT_SIZE), 16, 15, self.available_designs, False)
        # 添加按钮
        ttk.Style().configure("3.TButton", padding=5, relief="flat",
                              background=BG_COLOUR, foreground='firebrick', font=(FONT0, FONT_SIZE))
        self.CompareBt = ttk.Button(
            style="3.TButton", master=self.top1, text='开始对比', width=10, command=self.start)
        self.CompareBt.pack(side='right', fill='y', expand=False, padx=100)
        tk.Frame(master=self.basic, bg=BG_COLOUR2, height=3).pack(side='top', fill='x', expand=False)

    def start(self):
        if self.combox.box.get() == '':
            messagebox.showerror('错误', '请选择要对比的设计！')
            return
        # 判断是否选择了两个不同的设计
        if self.combox.box.get() == GUI.Left.combox.box.get():
            messagebox.showerror('错误', '请选择两个不同的设计！')
            return
        # 开始对比



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
        # 添加右键菜单
        self.menu = tk.Menu(self.canvas, tearoff=0)
        self.menu.add_command(label='F1', command=self.F1)
        self.canvas.bind('<Button-3>', self.popup)
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
        self.BtPos = [780, 657]
        self.Button = self.canvas.create_rectangle(
            self.BtPos[0] - 130, self.BtPos[1] - 20, self.BtPos[0] + 130, self.BtPos[1] + 20,
            outline='white', width=2)
        # 文字
        self.ButtonText = self.canvas.create_text(
            self.BtPos[0], self.BtPos[1], text="船只介绍", anchor='center', font=(FONT0, 13), fill='white')
        # 绑定事件
        self.canvas.tag_bind(self.Button, '<Button-1>', self.button_down)
        self.canvas.tag_bind(self.ButtonText, '<Button-1>', self.button_down)
        # 简介界面
        self.IntroCv = tk.Canvas(self.canvas, width=1300, height=500)
        self.IntroCv.config(scrollregion=(0, 0, 1300, 500))  # Canvas显示大小
        self.IntroCv.config(bg='white', highlightthickness=0)
        self.IntroCv.bind('<MouseWheel>', self.on_mousewheel)  # 鼠标滚轮
        # 插入图片
        self.ImgX = -345
        self.ImgY = -265
        self.IntroCv.create_image(self.ImgX, self.ImgY, image=self.BG1, anchor='nw',
                                  tags=('introduction', 'image'))

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def F1(self):
        ...

    def button_down(self, event=None):
        if self.canvas.itemcget(self.ButtonText, 'text') == '船只介绍':
            self.canvas.itemconfig(self.ButtonText, text='性能参数')
            self.canvas.itemconfig('values', state='hidden')
            self.IntroCv.place(x=780, y=135, anchor='n')
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
                780, 60, text=f"{DR.ShipName}", anchor='center', font=(FONT0, 22), fill='white',
                tags=('content',))
            self.canvas.create_text(
                780, 115, text=f"设计者:{DR.Designer}", anchor='center', font=(FONT0, 18), fill='white',
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
        # 添加右键菜单
        self.menu = tk.Menu(self.canvas, tearoff=0)
        self.menu.add_command(label='F1', command=self.F1)
        self.canvas.bind('<Button-3>', self.popup)

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

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
        self.top1 = tk.Frame(master=self.basic, bg=BG_COLOUR)
        self.top1.pack(side='top', fill='x', expand=False, pady=6)
        self.combox = text_with_combox(
            self.top1, '选择设计:', (FONT0, FONT_SIZE), 9, 15, self.available_designs, False)
        # 创建2列的treeview，但是要隐藏第一行表头
        # 用style设置行高和字体，居中显示
        style = ttk.Style()
        style.configure(
            "Treeview", rowheight=36, font=(FONT0, FONT_SIZE), foreground=FG_COLOUR, background=BG_COLOUR)
        self.tree = ttk.Treeview(
            self.basic, columns=('key', 'value'), show="headings", height=13, style="Treeview")
        self.tree['show'] = ''
        self.tree.column('key', width=125, anchor='e')
        self.tree.column('value', width=165, anchor='center')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.pack(side='top', expand=False)
        # 初始化左边栏的内容
        # 定义初始化数据
        data = [
            ('设计师ID', ''),
            ('战舰类型', ''),
            ('排水体积比', ''),
            ('长宽吃水比', ''),
            ('方形系数', ''),
        ]

        # 批量插入数据
        for item in data:
            self.tree.insert('', 'end', values=item)

    def update_treeview(self):
        """
        更新treeview
        :return:
        """
        DR = Handler.DesignReader
        # 直接修改treeview的值
        datas = [
            DR.DesignerID,
            DR.Type,
            str(DR.weight_ratio),
            str(DR.Len_Wid_Dra),
            str(DR.SquareCoefficient),
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
    GUI = TkinterGUI()
    GUI.init()
    Handler = MainHandler()
    GUI.ShowFrame.update_messages()
    # 启动主循环
    GUI.root.mainloop()
