"""
This file contains the class WeaponSelector, which is used to select a weapon
"""
from utils.TkGUI import *
from Data.PartAttrMaps import *


def show_weapon_name_rule():
    # 子窗口
    window = tk.Toplevel()
    window.title("武器名称规则")
    window.configure(background=BG_COLOUR2)
    window.geometry("880x720")
    window.wm_attributes('-topmost', 1)  # 窗口置顶
    # 窗口内容
    tk.Frame(window, height=30, bg=BG_COLOUR2).pack()
    tk.Label(window, text="武器名称规则", font=(FONT0, 20), bg=BG_COLOUR2).pack()
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
            _frm = tk.Frame(window, bg=BG_COLOUR2)
            _frm.pack(side='top', expand=False, fill='x', padx=30)
            tk.Label(_frm, text=line, font=(FONT0, 14), bg=BG_COLOUR2).pack(side='left', expand=False)
        elif "  1." in line or "  2." in line or "  3." in line:
            _frm = tk.Frame(window, bg=BG_COLOUR2)
            _frm.pack(side='top', expand=False, fill='x', padx=30)
            tk.Label(_frm, text=line, font=(FONT0, 12), bg=BG_COLOUR2).pack(side='left', expand=False)
        else:
            _frm = tk.Frame(window, bg=BG_COLOUR2)
            _frm.pack(side='top', expand=False, fill='x', padx=30)
            tk.Label(_frm, text=line, font=(FONT1, 12), bg=BG_COLOUR2).pack(side='left', expand=False)
    window.mainloop()


class WeaponSelector:
    def __init__(self, frame):
        self.basic = frame
        self.search_input_box = EntryBox3parts(
            self.basic, "top", [" 输入搜索内容：", "搜索"], [10, 10, 6], self.search, (FONT0, FONT_SIZE), 10)
        self.menu = tk.Menu(self.search_input_box.box, tearoff=0)
        self.menu.add_command(label='查看武器名称规则', command=show_weapon_name_rule)
        self.search_input_box.box.bind("<Button-3>", self.popup)
        # 创建2列的treeview，但是要隐藏第一行表头
        self.top2_frame = tk.Frame(self.basic, bg=BG_COLOUR)
        self.top2_frame.pack(side='top', expand=False)
        _style = ttk.Style()
        _style.configure("1.Treeview", font=(FONT0, FONT_SIZE), rowheight=26)
        self.tree = ttk.Treeview(
            self.top2_frame, columns=('key', 'value'), show="headings", height=3, style="1.Treeview")
        self.tree['show'] = ''
        self.tree.column('key', width=180, anchor='w')
        self.tree.column('value', width=90, anchor='w')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.pack(side='left', expand=False, pady=6)
        # 创建滚动条
        self.scrollbar = tk.Scrollbar(self.top2_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.tree.yview)
        # 挑选武器种类
        self.top3_frame = tk.Frame(self.basic, bg=BG_COLOUR)
        self.top3_frame.pack(side='top', expand=False)
        self.select_type_combox = text_with_combox(
            self.top3_frame, " 种类：", (FONT0, FONT_SIZE), 5, 7, ["大口径", "中口径", "鱼雷", "防空炮", "其他"], True)
        # 挑选武器国家
        self.select_country_combox = text_with_combox(
            self.top3_frame, " 国家：", (FONT0, FONT_SIZE), 5, 7, [
                "英系", "美系", "德系", "日系", "苏系", "意系", "法系", "泛亚", "泛欧"], True)

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def search(self, event=None):
        search_content = self.search_input_box.box.get()
        for weapon_name in PartType11.values():
            print(weapon_name)
            print(search_content)
            if search_content in weapon_name and search_content != "":
                self.tree.insert("", "end", values=(weapon_name, search_content))
            else:
                self.tree.insert("", "end", values=(weapon_name, "没有找到武器，请重新输入"))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("测试")
    root.configure(bg=BG_COLOUR)
    root.resizable(False, False)
    frame = tk.Frame(root, width=800, height=600, bg=BG_COLOUR)
    frame.pack(expand=True)
    WeaponSelector(frame)
    root.mainloop()
    # 把图片转为base64编码
    import base64
    with open("PTB.png", "rb") as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        print(base64_data)
