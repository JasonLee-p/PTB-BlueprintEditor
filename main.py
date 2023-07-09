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
        更新treeview
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
                        GUI.Right2.update_messages()
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
        self.Frame_CA = tk.Frame(bg=BG_COLOUR)
        self.Frame_3D = tk.Frame(bg=BG_COLOUR)
        self.notebook_main.add(self.Frame_BP, text='   图纸详细信息   ')
        self.notebook_main.add(self.Frame_CA, text='        计算器        ')
        self.notebook_main.add(self.Frame_3D, text='       3D预览       ')
        self.notebook_main.pack(fill='both', side='right', expand=True)
        self.Right2 = None

    def init(self):
        self.Right2 = RightFrame2(self.Frame_BP)


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


class RightFrame2:
    def __init__(self, frm):
        self.basic = frm
        main_title(self.basic, text='图纸详细信息', side='top')

        # 读取图片，把base64编码的图片解码成可用格式
        self.bg_base64 = base64.b64decode(BG)
        self.BG1 = tk.PhotoImage(data=self.bg_base64)
        # 显示图片
        self.canvas = tk.Canvas(self.basic, width=self.BG1.width(), height=self.BG1.height(), bg=BG_COLOUR)
        self.canvas.pack(side='top', fill='both', expand=True)
        self.canvas.create_image(-215, -130, image=self.BG1, anchor='nw')

    def update_messages(self):
        """
        更新treeview
        :return:
        """
        DR = Handler.DesignReader
        # 插入信息


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
            ('设计师', ''),
            ('设计师ID', ''),
            ('战舰类型', ''),
            ('排水量', ''),
            ('总体积', ''),
            ('排水体积比', ''),
            ('水线长', ''),
            ('水线宽', ''),
            ('吃水深度', ''),
            ('长宽吃水比', ''),
            ('水上高度', ''),
            ('方形系数', ''),
            ('阻力系数', '')
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
        self.tree.set('I001', 'value', DR.Designer)  # 设计师
        self.tree.set('I002', 'value', DR.DesignerID)  # 设计师ID
        self.tree.set('I003', 'value', DR.Type)  # 战舰类型
        self.tree.set('I004', 'value', str(DR.Displacement_in_t) + "t")  # 排水量
        self.tree.set('I005', 'value', str(DR.Volume_in_m) + "m³")  # 总体积
        self.tree.set('I006', 'value', str(DR.weight_ratio))  # 排水体积比
        self.tree.set('I007', 'value', str(DR.Length_in_m) + "m")  # 水线长
        self.tree.set('I008', 'value', str(DR.Width_in_m) + "m")  # 水线宽
        self.tree.set('I009', 'value', str(DR.Draft_in_m) + "m")  # 吃水深度
        self.tree.set('I00A', 'value', str(DR.Len_Wid_Dra))  # 长宽吃水比
        self.tree.set('I00B', 'value', str(DR.Height_in_m) + "m")  # 水上高度
        self.tree.set('I00C', 'value', str(DR.SquareCoefficient))  # 方形系数
        self.tree.set('I00D', 'value', str(DR.Drag))  # 阻力系数


def show_text(text, mode):
    GUI.Bottom.result.config(state='normal')
    GUI.Bottom.result.insert('end', text + '\n', mode)
    GUI.Bottom.result.config(state='disabled')


if __name__ == '__main__':
    GUI = TkinterGUI()
    GUI.init()
    Handler = MainHandler()
    # 启动主循环
    GUI.root.mainloop()
