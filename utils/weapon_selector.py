"""
This file contains the class WeaponSelector, which is used to select a weapon
"""
from tkinter import Tk, PhotoImage
from utils.TkGUI import *
from Data.PartAttrMaps import *
from images import Img_mainWeapon


def show_weapon_name_rule():
    # 子窗口
    window = Toplevel()
    window.title("武器名称规则")
    window.configure(background=BG_COLOUR2)
    # 居中显示
    window.update_idletasks()
    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
    window.geometry("+%d+%d" % (x, y))
    window.geometry("1000x900")
    window.wm_attributes('-topmost', 1)  # 窗口置顶
    # 窗口内容
    Frame(window, height=30, bg=BG_COLOUR2).pack()
    Label(window, text="武器名称规则", font=(FONT0, 20), bg=BG_COLOUR2).pack()
    text = str(
        "一.火炮武器\n"
        "    1.火炮名称由 国家，武器口径*武器联装数-武器型号，武器改型编号 组成\n"
        "     例如：'日460*3'，'德380*2-SKC34L'，'德380*2-SKC34LK'\n"
        "    2.一般情况，武器没有编号，只有国家口径联装。设置编号的情况有：\n"
        "     1）一个口径一种联装数的武器有多种版本；\n"
        "       - 偶尔会直接用A，B，C来区分一种口径一种联装的不同型号，\n"
        "         例如'日12723-B'系列,'日127*2-S'（三年式用S）；\n"
        "     2）同一款武器有不同的版本，例如加雷达，救生筏，改进版等等；\n"
        "       - 雷达或则测距仪会加上'L'，比如1中的第一个德380，就指的是测距仪版；\n"
        "       - 救生筏会加上'J'；\n"
        "       - 防空炮版会加上'K'；\n"
        "       - 改进版会加上'G'（鱼雷也是）；\n"
        "       - 有舷台底座的一般情况会加上'D'，此类改型命名起来比较复杂，作者也忘记了命名法/doge；\n"
        "             例如'日127*2-BKB','日127*2-BDB'；\n"
        "             （第一个B应该是对武器型号的区分，后面两个字母应该是对改型型号的区分）\n"
        "       - 如果占据多项，就把字母连在一起写，例如1中的第二个德380。\n"
        "     3）一个武器的编号有非常高的流传度；\n"
        "二.鱼雷武器\n"
        "    1.鱼雷名称由 国家，鱼雷联装数-鱼雷改型编号 组成\n"
        "     例如：'日雷3'，'德雷4'，'美雷4-G'\n"
        "    2.鱼雷的改型编号规则和火炮一样\n"
        "三.防空武器\n"
        "    1.防空武器名称由 武器中文名，武器口径*武器联装数-武器改型编号 组成：\n"
        "     例如：\n"
        "       '手拉机37*2-D'，'德高炮88*1'，'中高炮57*2'，'九六式25*3-DR'\n"
        "       '弗莱克20*4'（即Flack），'斯塔格40*2'（即STAAG），'马克十76*1'（即MK10）"
    )
    for line in text.split('\n'):
        if "一." in line or "二." in line or "三." in line:
            _frm = Frame(window, bg=BG_COLOUR2)
            _frm.pack(side='top', expand=False, fill='x', padx=30)
            Label(_frm, text=line, font=(FONT0, 14), bg=BG_COLOUR2).pack(side='left', expand=False)
        elif "  1." in line or "  2." in line or "  3." in line:
            _frm = Frame(window, bg=BG_COLOUR2)
            _frm.pack(side='top', expand=False, fill='x', padx=30)
            Label(_frm, text=line, font=(FONT0, 12), bg=BG_COLOUR2).pack(side='left', expand=False)
        else:
            _frm = Frame(window, bg=BG_COLOUR2)
            _frm.pack(side='top', expand=False, fill='x', padx=30)
            Label(_frm, text=line, font=(FONT1, 12), bg=BG_COLOUR2).pack(side='left', expand=False)
    window.mainloop()


class WeaponSelector:
    """
    武器选择器
    需要宽度为440，高度为180
    """
    def __init__(self, frame, side, expand, fill, padx, pady):
        self.H = 240
        self.W = 550
        self.basic = Frame(frame, width=self.W, height=self.H, bg=BG_COLOUR2)
        self.basic.pack(expand=expand, side=side, fill=fill, padx=padx, pady=pady)
        self.basic.propagate(0)
        # 武器信息
        self.left = Frame(self.basic, width=390, height=self.H - 20, bg=BG_COLOUR2)
        self.left.pack(expand=False, side="left", ipady=5, ipadx=7)
        self.left.propagate(0)
        # 武器图片
        self.PhotoImage = PhotoImage(data=Img_mainWeapon.W110000300)
        self.right = Label(self.basic, width=self.W - 400, height=self.H - 20, bg=BG_COLOUR2, image=self.PhotoImage)
        self.right.pack(expand=False, side="right", ipady=5, ipadx=7)
        self.right.propagate(0)
        # 标题
        self.title = Label(self.left, text="武器筛选", font=(FONT0, 15), bg=BG_COLOUR)
        self.title.pack(side='top', expand=False, fill='x', padx=9)
        Frame(self.left, bg=BG_COLOUR2, height=4).pack(side='top', expand=False, fill='x')
        # 挑选武器种类
        self.top1_frame = Frame(self.left, bg=BG_COLOUR)
        self.top1_frame.pack(side='top', expand=False, fill='x', padx=9)
        self.select_type_combox = text_with_combox(
            self.top1_frame, " 种类：", (FONT0, FONT_SIZE), 5, 8, ["大口径", "中口径", "鱼雷", "防空炮", "其他"], True)
        # 挑选武器国家
        self.select_country_combox = text_with_combox(
            self.top1_frame, " 国家：", (FONT0, FONT_SIZE), 5, 8, [
                "英系", "美系", "德系", "日系", "苏系", "意系", "法系", "泛亚", "泛欧"], True)
        Frame(self.left, bg=BG_COLOUR2, height=4).pack(side='top', expand=False, fill='x')
        # 搜索框
        self.search_input_box = EntryBox3parts(
            self.left, "top", [" 输入关键字：", "筛选"], [9, 13, 6], self.search, (FONT0, FONT_SIZE), 10)
        Frame(self.left, bg=BG_COLOUR2, height=4).pack(side='top', expand=False, fill='x')
        # 创建2列的treeview，但是要隐藏第一行表头
        self.top2_frame = Frame(self.left, bg=BG_COLOUR)
        self.top2_frame.pack(side='top', expand=False)
        _style = ttkStyle()
        _style.configure("1.Treeview", font=(FONT0, 10), rowheight=28)
        self.tree = Treeview(
            self.top2_frame, columns=('key', 'value'), show="headings", height=3, style="1.Treeview")
        self.tree['show'] = ''
        self.tree.column('key', width=240, anchor='w')
        self.tree.column('value', width=120, anchor='w')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.pack(side='left', expand=False, pady=6)
        # 绑定选中事件
        self.tree.bind('<<TreeviewSelect>>', self.select)
        self.selectedID = None
        self.selectedName = None
        # 绑定菜单
        self.menu0 = Menu(self.search_input_box.box, tearoff=0)
        self.menu0.add_command(label='查看武器名称规则', command=show_weapon_name_rule)
        self.search_input_box.box.bind("<Button-3>", self.popup)
        self.tree.bind("<Button-3>", self.popup)
        self.right.bind("<Button-3>", self.popup)
        # 创建滚动条
        self.scrollbar = Scrollbar(self.top2_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.tree.yview)
        # 鼠标停止不动时间2s后，显示当前行数：
        self.line_label = Label(master=self.tree, text=' 行数：', bg='white', font=(FONT1, FONT_SIZE))
        self.line_label.config(bd=1, relief='solid', anchor='w')
        self.tree.bind('<Motion>', self._show_line)
        self.select_country_combox.bind('<Motion>', self._show_line)
        self.right.bind('<Motion>', self._show_line)
        self.timer = time.time()

    def popup(self, event):
        event.widget.focus()
        self.menu0.post(event.x_root, event.y_root)

    def search(self, event=None):
        search_content = self.search_input_box.box.get()
        country = self.select_country_combox.get()
        weapon_type = self.select_type_combox.get()

        self.tree.delete(*self.tree.get_children())
        search_dict = PartType11.copy()

        if search_content:
            search_dict = {weapon_id: weapon_name for weapon_id, weapon_name in search_dict.items() if
                           search_content in weapon_name}

        if country != '无':
            search_dict = {
                weapon_id: weapon_name
                for weapon_id, weapon_name in search_dict.items()
                if (
                    (country[0] in weapon_name[0])
                    or (country[:2] in '泛亚' and '中' in weapon_name)
                    or (country[:2] in '泛欧' and weapon_name[0] in '奥荷芬')
                    or ('博福斯' in weapon_name and country[0] in '英美')
                    or ('弗莱克' in weapon_name and country[0] in '德')
                    or ('手拉' in weapon_name and country[0] in '德')
                    or ('斯塔格' in weapon_name and country[0] in '英')
                    or ('三年' in weapon_name and country[0] in '日')
                )
            }

        if weapon_type != '无':
            search_dict = {
                weapon_id: weapon_name
                for weapon_id, weapon_name in search_dict.items()
                if (
                    ('110' in weapon_id[:3] and int(weapon_name[1:4]) < 190 and weapon_type == '中口径')
                    or ('110' in weapon_id[:3] and int(weapon_name[1:4]) >= 190 and weapon_type == '大口径')
                    or ('113' in weapon_id[:3] and weapon_type == '鱼雷')
                    or ('112' in weapon_id[:3] and weapon_type == '防空炮')
                    or (weapon_type == '其他')
                )
            }

        for weapon_id, weapon_name in search_dict.items():
            self.tree.insert('', 'end', values=(weapon_name, weapon_id))

    def select(self, event):
        self.selectedName = event.widget.item(event.widget.selection()[0], "values")[0]
        self.selectedID = event.widget.item(event.widget.selection()[0], "values")[1]
        img = eval(f'Img_mainWeapon.W{self.selectedID}')
        # 更新左边的武器图片
        self.right.destroy()
        self.PhotoImage = PhotoImage(data=img)
        self.right = Label(self.basic, width=self.W - 320, height=self.H - 20, bg=BG_COLOUR2, image=self.PhotoImage)
        self.right.pack(expand=True, side="left", ipady=5, ipadx=7)
        self.right.propagate(0)

    def _show_line(self, event=None):
        self.timer = time.time()
        self.line_label.place_forget()  # 隐藏行数
        # 非阻塞式检测时间，如果鼠标停止不动1s后，显示当前行数：
        self.tree.after(2000, self._show_line2)

    def _show_line2(self, event=None):
        if time.time() - self.timer < 1:
            return
        # 获取鼠标的坐标：
        x = self.tree.winfo_pointerx() - self.tree.winfo_rootx()
        y = self.tree.winfo_pointery() - self.tree.winfo_rooty()
        self.line_label.config(text=f'右键查看武器名称规范')
        self.line_label.place(x=x, y=y)


if __name__ == "__main__":
    from TkGUI import *
    root = Tk()
    set_window(root, "测试")
    from plt_ import Plot3D
    import numpy as np
    plt1 = Plot3D(root, "测试", figsize=(11, 8), place=(800, 0))
    # 定义三维数据

    xx = np.arange(0, 10, 0.1)
    yy = np.arange(0, 10, 0.1)
    X, Y = np.meshgrid(xx, yy)
    Z = np.sin(X) + np.cos(Y)
    plt1.plot(X, Y, Z, (0, 10), (0, 10), (-2, 2))
    root.mainloop()
