# -*- coding: utf-8 -*-
"""
    This module is used to simplify the use of tkinter.
"""
import ctypes
import sys
import json
import time
from tkinter import Frame, Label, Canvas, Button, Scrollbar, \
    Text, Menu, Toplevel, \
    StringVar, IntVar, \
    TclError, INSERT
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox, Treeview
from tkinter.ttk import Style as ttkStyle
from tkinter.ttk import Button as ttkButton
from tkinter.ttk import Entry as ttkEntry

BG_COLOUR = 'Beige'  # 背景色
BG_COLOUR2 = 'ivory'  # 背景色
FG_COLOUR = 'black'  # 前景色
FONT0 = 'microsoft yahei'
FONT1 = '幼圆'
# 获取分辨率：
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 设置高分辨率
user32 = ctypes.windll.user32
width_ = user32.GetSystemMetrics(0)
height_ = user32.GetSystemMetrics(1)
RATE = width_/1920

ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)  # 获取屏幕的缩放因子

FONT_SIZE7 = int(7 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE8 = int(8 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE9 = int(9 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE10 = int(10 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE12 = int(12 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE14 = int(14 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE16 = int(16 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE18 = int(18 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE20 = int(20 * 125 * width_ / (ScaleFactor * 1920))
FONT_SIZE22 = int(22 * 125 * width_ / (ScaleFactor * 1920))


def set_window(window, title: str, transparent=True):
    """
    initialize the window, set the window size, title, icon, etc.
    :param window: tk.Tk() object.
    :param title: str, the title of the window.
    :param transparent: bool, whether the window is transparent.
    """
    window.attributes("-alpha", 0)  # 设置窗口透明度
    if transparent:
        TransparentColor = 'gray'
        window.wm_attributes("-transparentcolor", TransparentColor)
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 告诉操作系统使用程序自身的dpi适配
    window.tk.call('tk', 'scaling', ScaleFactor / 75)  # 设置程序缩放
    try:
        window.state("zoomed")
    except TclError:
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        window.geometry("%dx%d" % (w, h))
    # master.iconbitmap(os.path.join(os.path.dirname(own_path), 'images/icon.ico'))  # 更改窗口图标
    window.title(title)  # 窗口名
    window.minsize(int(1200*RATE), int(860*RATE))
    window.configure(bg=BG_COLOUR)  # 背景色


def main_title(master, text, side):
    Frame(master=master, bg=BG_COLOUR, height=int(10*RATE)).pack(side='top', fill='x')
    title_v = Label(
        master,
        text=text,  # 标签的文字
        bg=BG_COLOUR,  # 标签背景颜色
        font=(FONT1, FONT_SIZE14),  # 字体和字体大小
        width=int(30*RATE), height=1)  # 标签长宽
    title_v.pack(side=side, pady=0, expand=False, anchor='center')  # 固定窗口位置
    Frame(master=master, bg=BG_COLOUR, height=int(6*RATE)).pack(side='top', fill='x')
    Frame(master=master, bg='ivory', height=4).pack(side='top', fill='x')


# 显示的音符名
def title(text, bg_colour):
    def _title(belonging, master, position, font_size, expand, wid, hei, fill=None, padx=0, pady=0, ipadx=0, ipady=0):
        _title_v = Label(
            master,
            text=text,
            bg=bg_colour,  # 标签背景颜色
            font=(FONT1, font_size),  # 字体和字体大小
            width=wid, height=hei)  # 标签长宽
        _title_v.pack(side=position, fill=fill, padx=padx, pady=pady, expand=expand, ipadx=ipadx, ipady=ipady)  # 固定窗口位置
        if belonging:
            belonging.append(_title_v)
        return _title_v

    return _title


def button(master, expand, belonging, hit_func, text, side, width, style=None):
    BTStyle = ttkStyle()
    BTStyle.configure('TButton', borderradius=5, font=(FONT0, FONT_SIZE12))
    _style = style if style else 'TButton'
    b = ttkButton(master, text=text, width=width, command=hit_func, style=_style)
    b.configure()
    b.pack(side=side, padx=5, pady=4, expand=expand)
    if belonging:
        belonging.append(b)
    return b


# 定义下拉选择框
def combox(master, belonging, selected_func, values, position='basic', width=19, height=5, style_name=None):
    text_var = StringVar()
    cb = Combobox(
        master, textvariable=text_var, state='readonly',
        font=(FONT0, FONT_SIZE12), width=width, height=height,
        values=values
    )
    if style_name:
        cb.configure(style=style_name)
    cb.bind("<<ComboboxSelected>>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    cb.bind("<Leave>", selected_func)  # 绑定事件(鼠标离开时，绑定函数selected_func)
    # _combox.bind("<Return>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    cb.pack(side=position, padx=5)
    if belonging:
        belonging.append(cb)
    return cb


def column_selected(name):
    messagebox.showinfo('', f'{name}')


class MyTreeView:
    def __init__(self, master, columns, dataframe, height, style_name=None):
        self.columns = list(columns.keys())
        self.data = dataframe
        self.h = height
        self.w_s = list(columns.values())
        self.style_name = style_name
        TVStyle = ttkStyle()
        TVStyle.configure('Treeview', rowheight=self.h, font=(FONT0, FONT_SIZE12))
        self.VScroll1 = Scrollbar(
            master, relief='flat', troughcolor=BG_COLOUR, width=int(30*RATE), orient='vertical')
        self.VScroll1.pack(side='right', fill='y', padx=0)
        self.tv = Treeview(
            master=master,  # 父容器
            height=len(self.data),  # 表格显示的行数,height行
            columns=self.columns,  # 显示的列
            show='headings',  # 隐藏首列
            style='Treeview',
            yscrollcommand=self.VScroll1.set
        )
        for i in range(len(columns)):
            self.tv.heading(column=self.columns[i], text=self.columns[i], anchor="center",  # 显示表头
                            command=lambda name=self.columns[i]:
                            column_selected(name)
                            )
            self.tv.column(column=self.columns[i], width=self.w_s[i], minwidth=80, anchor="center", )  # 定义列
        self.VScroll1.configure(command=self.tv.yview)
        self.tv.bind('<ButtonRelease-1>', self.treeviewClick)
        self.tv.pack(expand=True)
        self.tv.yview_moveto(1)

    def treeviewClick(self, ent):  # 单击
        # print('单击')
        for item in self.tv.selection():
            item_text = self.tv.item(item, "values")
            # print(item_text[0])  # 输出所选行的第一列的值

    def destroy(self):
        self.tv.destroy()
        self.VScroll1.destroy()


def fill_tv_with_json(json_filepath, tv):
    with open(json_filepath, '_r') as rf:
        json_data = json.load(rf)
    for i in range(len(json_data['date'])):
        tv.insert(
            '', i,
            values=(json_data['date'][i], json_data['_time'][i], json_data['sheet'][i], json_data['score'][i])
        )


def treeview_sort_column(treeview, column, reverse):  # Treeview、列名、排列方式
    lst = [(treeview.set(k, column), k) for k in treeview.get_children('')]
    print(treeview.get_children(''))
    lst.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(lst):  # 根据排序后索引移动
        treeview.move(k, '', index)
        print(k)
    treeview.heading(column, command=lambda: treeview_sort_column(treeview, column, not reverse))  # 重写标题，使之成为再点倒序的标题


class EntryBox3parts:
    """
    可以记录历史输入的输入框，有文字和按钮，用于输入字符串
    """

    def __init__(self, master, position, text2, width3, bt_command, font, memory_max_len):
        """
        :param master:
        :param position:
        :param text2: text's text and button text
        :param width3: text's width, entry's width, button's width
        :param bt_command:
        :param font: font-size and font family
        :param memory_max_len:
        """
        self.basic = Frame(master, bg=BG_COLOUR)
        self.basic.pack(side=position, expand=0, padx=9)
        self.text = Label(self.basic, text=text2[0], font=font, width=width3[0], bg=BG_COLOUR)
        self.text.pack(side="left", expand=0, padx=5)
        self.box = ttkEntry(self.basic, justify="center", font=font, width=width3[1])
        self.box.pack(side="left", expand=0, padx=5)
        self.style = ttkStyle()
        self.style.configure('TButton', font=font)

        self.button = ttkButton(self.basic, text=text2[1], width=width3[2], command=bt_command)
        self.button.pack(side="right", expand=0, padx=4)
        self.box.insert(0, '')
        # 当输入框正在输入时，在下方显示输入记录，并且可以通过鼠标点击记录来输入
        self.box.bind('<KeyRelease>', self.onKeyRelease)
        self.memory_menu = Menu(self.box, tearoff=0)
        self.memory = []
        self.memory_max_len = memory_max_len

    def onKeyRelease(self, event=None):
        """
        当输入框正在输入时，在下方显示输入记录，并且可以通过鼠标点击记录来输入
        """
        if self.box.get() == '':
            self.memory_menu.post(0, 0)

    def save_to_memory(self):
        self.memory.append(self.box.get())
        # 重新映射命令：
        self.memory_menu.delete(0, 'end')
        index = self.memory.index(self.box.get())  # 获取索引
        if index >= self.memory_max_len:
            self.memory = self.memory[index - self.memory_max_len + 1:]
        # 重新映射命令：
        for i in range(len(self.memory)):
            self.memory_menu.add_command(label=self.box.get(), command=lambda: self.box.insert(0, self.memory[i]))


class EntryBoxMouseWheel:
    """
    可以鼠标滚动控制值的输入框，用于输入整数
    """

    def __init__(self, master, belonging, position, font, width, default,
                 setRange: list, touch_func=None, msWheel_func=None, _queue=None):
        self.get = default
        EStyle = ttkStyle()
        EStyle.configure('TEntry', borderradius=10)
        self.box = ttkEntry(master, justify="center", font=font, width=width, style='TEntry')
        self.box.pack(side=position, expand=0)
        self.box.insert(0, default)
        if _queue:
            self.q = _queue
            self.q.put(default)
        if touch_func:
            self.box.bind("<Return>", touch_func)
            self.box.bind("<Button-1>", touch_func)
            self.box.bind("<Leave>", touch_func)
            # self.box.bind("<Enter>", touch_func)
        else:
            self.range = setRange
            self.box.bind("<Return>", self.get_beat)
            self.box.bind("<Enter>", self.get_beat)
            self.box.bind("<Button-1>", self.get_beat)
            self.box.bind("<Leave>", self.get_beat)
        if msWheel_func:
            self.box.bind("<MouseWheel>", msWheel_func)
        else:
            self.box.bind("<MouseWheel>", self.mouse_wheel_change)
        if belonging:
            belonging.append(self.box)

    def mouse_wheel_change(self, ent):
        num = int(ent.widget.get())
        if ent.delta > 0 and num < self.range[1]:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(num + 1))
            self.q.put(str(num + 1))
        if ent.delta <= 0 and num > self.range[0]:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(num - 1))
            self.q.put(str(num - 1))
        if num <= self.range[0] or num >= self.range[1]:
            pass

    def get_beat(self, ent):
        txt = ent.widget.get()
        try:
            entry_num = abs(int(txt))
            if self.range[0] <= entry_num <= self.range[1]:
                self.get = entry_num
                self.q.put(entry_num)
            else:
                ent.widget.delete(0, 'end')
        except ValueError:
            ent.widget.delete(0, 'end')


class ComboBoxMouseWheel2:
    """
    可以鼠标滚动控制值的输入框
    """

    def __init__(self, master, belonging, position, font, width, default,
                 entry_list: list, touch_func=None, msWheel_func=None):
        if default not in entry_list:
            entry_list.append(default)
            # 将default放在第一个：
            entry_list = [entry_list[-1]] + entry_list[:-1]
        self.box = Combobox(master, justify="center", font=font, width=width, values=entry_list)
        self.box.pack(side=position, expand=False, padx=5, pady=5)
        self.box.insert(0, default)
        self.i = 0
        self.get = default
        if touch_func:
            self.range = [default] + entry_list
            self.box.bind("<Return>", touch_func)
            self.box.bind("<Button-1>", touch_func)
            self.box.bind("<Leave>", touch_func)
        else:
            self.range = [default] + entry_list
            # print(self.range)
            self.box.bind("<Return>", self.get_beat)
            self.box.bind("<Enter>", self.get_beat)
            self.box.bind("<Button-1>", self.get_beat)
            self.box.bind("<Leave>", self.get_beat)
        if msWheel_func:
            self.box.bind("<MouseWheel>", msWheel_func)
        else:
            self.box.bind("<MouseWheel>", self.mouse_wheel_change)
        if belonging:
            belonging.append(self.box)

    def mouse_wheel_change(self, ent):
        if ent.delta <= 0 and self.i < len(self.range) - 1:
            self.i += 1
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, self.range[self.i])
        if ent.delta > 0 and self.i > 0:
            self.i -= 1
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, self.range[self.i])
        if self.i <= 0:
            self.i = 0
        if self.i >= len(self.range) - 1:
            self.i = len(self.range) - 1

    def get_beat(self, ent):
        txt = ent.widget.get()
        _range = [str(i) for i in self.range]
        if txt in _range:
            self.get = txt


def text_with_combox(master, text, font, text_w, combox_w, combox_list, add_wu=True):
    combox_list = ["无"] + list(combox_list) if add_wu else list(combox_list)
    title(text, BG_COLOUR)(None, master, 'left', font[1], False, text_w, hei=1, padx=0, pady=0)
    c = Combobox(master, justify="center", font=(FONT0, font[1]), width=combox_w, values=combox_list)
    # 设置默认值
    if combox_list:
        c.current(0)
    c.pack(side='left', expand=False, padx=int(5*RATE), pady=int(5*RATE))
    return c


class EntryBoxMouseWheel2:
    """
    可以鼠标滚动控制值的输入框，用于输入整数
    """

    def __init__(self, master, belonging, position, font, width, default,
                 setRange: list, touch_func=None, msWheel_func=None, _queue=None):
        self.get = default
        EStyle = ttkStyle()
        EStyle.configure('TEntry', borderradius=10)
        self.box = ttkEntry(master, justify="center", font=font, width=width, style='TEntry')
        self.box.pack(side=position, expand=0)
        self.box.insert(0, default)
        if _queue:
            self.q = _queue
            self.q.put(default)
        if touch_func:
            self.box.bind("<Return>", touch_func)
            self.box.bind("<Button-1>", touch_func)
            self.box.bind("<Leave>", touch_func)
            # self.box.bind("<Enter>", touch_func)
        else:
            self.range = setRange
            self.box.bind("<Return>", self.get_beat)
            self.box.bind("<Enter>", self.get_beat)
            self.box.bind("<Button-1>", self.get_beat)
            self.box.bind("<Leave>", self.get_beat)
        if msWheel_func:
            self.box.bind("<MouseWheel>", msWheel_func)
        else:
            self.box.bind("<MouseWheel>", self.mouse_wheel_change)
        if belonging:
            belonging.append(self.box)

    def mouse_wheel_change(self, ent):
        num = int(ent.widget.get())
        if ent.delta > 0 and num < self.range[1]:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(num + 1))
            self.q.put(str(num + 1))
        if ent.delta <= 0 and num > self.range[0]:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(num - 1))
            self.q.put(str(num - 1))
        if num <= self.range[0] or num >= self.range[1]:
            pass

    def get_beat(self, ent):
        txt = ent.widget.get()
        try:
            entry_num = abs(int(txt))
            if self.range[0] <= entry_num <= self.range[1]:
                self.get = entry_num
        except ValueError:
            ent.widget.delete(0, 'end')


def release_protection(func):
    def wrapper(*args, **kwargs):
        TextEntryWithMenu.text.unbind('<KeyRelease>')
        func(*args, **kwargs)
        TextEntryWithMenu.text.bind('<KeyRelease>', TextEntryWithMenu.save_to_undo_stack)

    return wrapper


class TextEntryWithMenu:
    text = None

    def __init__(self, frame, font=('Consolas', FONT_SIZE12)):
        # 左边：带滚动条的代码文本编辑器
        self.basic = frame
        self.text = Text(master=self.basic, bg='ivory', width=70, height=8, font=font)
        TextEntryWithMenu.text = self.text
        self.text.config(spacing3=5)  # 扩大行间距
        self.text.pack(side='left', fill='y', expand=False)
        self.scroll = Scrollbar(master=self.basic)
        self.scroll.pack(side='left', fill='y', expand=False)
        # 将滚动条与代码文本编辑器绑定
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        self.text.bind('<Control-z>', self._undo)  # 绑定撤回快捷键
        # Control-Shift-z 为重做快捷键
        self.text.bind('<Control-x>', self._redo)  # 绑定重做快捷键
        self.text.bind('<Control-s>', self._save)  # 绑定保存快捷键
        self.text.bind('<Button-3>', self._popup)  # 绑定右键菜单栏
        # 检测到内容改变时：保存到撤回栈
        self.text.bind('<Key>', self.save_to_undo_stack)
        # 右键菜单栏：
        self.menu = Menu(master=self.text, tearoff=0)
        self.menu.add_command(label='撤回', command=self._undo)
        self.menu.add_command(label='重做', command=self._redo)
        self.menu.add_command(label='清空', command=self.clear)
        self.menu.add_command(label='保存', command=self._save)
        self.undo_stack = []
        self.redo_stack = []

    def _popup(self, event=None):
        # 在鼠标右键点击的位置显示右键菜单栏
        self.menu.post(event.x_root, event.y_root)

    # @release_protection
    def save_to_undo_stack(self, event=None):
        # 如果按住的是control，shift，z就不保存
        if event:
            if event.keysym in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'z']:
                self.text.bind('<KeyRelease>', self.save_to_undo_stack)  # 重新绑定
                return
        text = self.text.get('1.0', 'end')
        # 保存到撤回栈
        if not self.undo_stack:
            self.undo_stack.append((text, self.text.index(INSERT), self.scroll.get()))
        elif text != self.undo_stack[-1][0]:
            self.undo_stack.append((text, self.text.index(INSERT), self.scroll.get()))
            while len(self.undo_stack) > 1000:
                self.undo_stack.pop(0)
            # print(self.undo_stack)

    # @release_protection
    def _undo(self, event=None):
        text = self.text.get('1.0', 'end')
        # 撤回
        if self.undo_stack:
            if text == self.undo_stack[-1][0]:
                self.undo_stack.pop(-1)
            if self.redo_stack:
                if text != self.redo_stack[-1][0]:
                    self.redo_stack.append((text, self.text.index(INSERT), self.scroll.get()))
            else:
                self.redo_stack.append((text, self.text.index(INSERT), self.scroll.get()))
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', self.undo_stack[-1][0])
            self.text.mark_set(INSERT, self.undo_stack[-1][1])
            self.text.yview_moveto(self.undo_stack[-1][2][0])  # 输入框也要随着滚动条的位置变化而变化
            self.text.update()
            self.undo_stack.pop(-1)
            # print(self.undo_stack)
        while len(self.redo_stack) > 1000:
            self.undo_stack.pop(0)

    # @release_protection
    def _redo(self, event=None):
        text = self.text.get('1.0', 'end')
        # 重做
        if self.redo_stack:
            if self.undo_stack:
                if text != self.undo_stack[-1][0]:
                    self.undo_stack.append((text, self.text.index(INSERT), self.scroll.get()))
            else:
                self.undo_stack.append((text, self.text.index(INSERT), self.scroll.get()))
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', self.redo_stack[-1][0])
            self.text.mark_set(INSERT, self.redo_stack[-1][1])
            self.text.yview_moveto(self.undo_stack[-1][2][0])  # 输入框也要随着滚动条的位置变化而变化
            self.text.update()
            self.redo_stack.pop(-1)
        while len(self.undo_stack) > 1000:
            self.undo_stack.pop(0)

    def _save(self, event=None):
        # 保存为xml文件
        filename = filedialog.asksaveasfilename(
            title='保存为',
            filetypes=[('xml文件', '*.xml'), ('所有文件', '*.*')]
        )
        if filename:
            # 保存为xml文件
            path = filename + '.xml' if not filename.endswith('.xml') else filename
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.text.get('1.0', 'end'))
                f.close()

    def clear(self, event=None):
        # 弹出确认框
        if not messagebox.askokcancel('确认', '所有记录都会丢失，确定要清空吗？'):
            return
        # 清空文本框
        self.text.delete('1.0', 'end')
        self.text.update()
        self.redo_stack = []
        self.undo_stack = []


class TextRedirector(object):
    """
    A class for redirecting the output of the console to the text widget.
    """

    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, _str):
        self.widget.configure(state='normal')
        self.widget.insert('end', _str, (self.tag,))
        self.widget.configure(state='disabled')


class CodeEditor(TextEntryWithMenu):
    def __init__(self, frame, redirect=True):
        super().__init__(frame)
        self.redirect = redirect
        self.default_code = \
            "# Python\n" \
            "for i in range(1, 101):  # 这是一个循环语句：\n" \
            "    text = f'DPFM {i}times!'  # 缩进4空格\n" \
            "    print(text)"
        # 中间：运行按钮
        self.button = Button(master=self.basic, text='Run', command=self.run)
        self.button.pack(side='left', fill="both", padx=8)
        # 右边：带滚动条的显示运行结果的文本框，包括警告和报错信息
        self.result = Text(master=self.basic, bg='ivory', width=90, height=8, font=("Source Code Pro", 12))
        # 为右边的文本框添加滚动条
        self.scroll2 = Scrollbar(master=self.basic)
        self.scroll2.pack(side='right', fill='y', expand=False)
        self.result.pack(side='left', fill='both', expand=False)
        self.scroll2.config(command=self.result.yview)
        self.result.config(yscrollcommand=self.scroll2.set)
        self.result.config(state='disabled')
        if redirect:
            sys.stdout = TextRedirector(self.result, "stdout")
            sys.stderr = TextRedirector(self.result, "stderr")
        self.result.tag_config("stderr", foreground="firebrick")
        self.result.tag_config("stdout", foreground="black")
        self.text.bind('<Control-r>', self.run)  # 绑定运行快捷键
        self.menu.add_separator()
        self.menu.add_command(label='运行', command=self.run)
        # 填入默认示例代码
        self.text.insert(
            'end',
            self.default_code
        )
        # 鼠标停止不动时间2s后，显示当前行数：
        self.line_label = Label(master=self.text, text=' 行数：', bg='white', font=(FONT1, FONT_SIZE12))
        self.line_label.config(bd=1, relief='solid', anchor='w')
        self.text.bind('<Motion>', self._show_line)
        self.timer = time.time()

    def run(self, event=None):
        """
        用于运行可视化代码的函数
        """
        self.result.config(state='normal')
        clear_output = False
        if clear_output:
            self.result.delete('1.0', 'end')
        # 用蓝色显示运行时间
        # Q: 如何用蓝色显示运行时间？
        # A: 用tag_config()方法
        self.result.tag_config('_time', foreground='blue', font=("Source Code Pro", FONT_SIZE9))
        self.result.tag_config('init', foreground='blue', font=("Source Code Pro", FONT_SIZE9))
        self.result.tag_config('blue', foreground='blue', font=("Source Code Pro", FONT_SIZE12))
        self.result.tag_config('receive', foreground='black', font=("Source Code Pro", FONT_SIZE12))
        self.result.insert('end', time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime()), ('_time',))
        self.result.insert('end', ' 运行代码：\n', "blue")
        self.result.config(state='disabled')
        code = self.text.get('1.0', 'end')
        # 监测恶意代码
        if 'os' in code or 'sys' in code:
            self.result.config(state='normal')
            self.result.insert('end', '警告：请勿输入恶意代码！\n')
            self.result.config(state='disabled')
            return
        exec(code)
        self.result.insert('end', '\n\n')
        # 跳转到最后
        self.result.see('end')

    def _show_line(self, event=None):
        self.timer = time.time()
        self.line_label.place_forget()  # 隐藏行数
        # 非阻塞式检测时间，如果鼠标停止不动1s后，显示当前行数：
        self.text.after(2000, self._show_line2)

    def _show_line2(self, event=None):
        if time.time() - self.timer < 1:
            return
        # 获取鼠标的坐标：
        x = self.text.winfo_pointerx() - self.text.winfo_rootx()
        y = self.text.winfo_pointery() - self.text.winfo_rooty()
        # 在鼠标位置显示一个文本框，显示鼠标位置的行数
        row = self.text.index(f"@{x},{y}").split('.')[0]
        self.line_label.config(text=f' 第{row}行 ')
        self.line_label.place(x=x, y=y)


class MyMenu:
    def __init__(self, basic, menu_labels_funcs):
        # 添加右键菜单
        self.basic = basic
        self.menu = Menu(basic, tearoff=0)
        for label in menu_labels_funcs:
            self.menu.add_command(label=label, command=menu_labels_funcs[label])
        basic.bind('<Button-3>', self.popup)

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)


class TempTransparentWin:
    def __init__(self, text_color):
        self.root = Toplevel(highlightcolor='gray')
        self.root.attributes("-transparentcolor", "gray")
        self.root.config(bg='gray')
        # 设置窗口最大化
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        # print(width, height)
        self.root.geometry("%dx%d+100+0" % (width, height))
        self.root.wm_attributes("-topmost", True)
        self.root.overrideredirect(True)  # 设置窗口隐藏边框
        Label(self.root, text='——— 正在读取图纸 ———', font=(FONT0, int(40*RATE)), bg='gray', fg='#888888'
              ).place(relx=0.666, rely=0.85, anchor='center')
        for i in range(1, 17):
            self.root.attributes("-alpha", i / 20)
            self.root.update()
            time.sleep(0.005)

    def destroy(self):
        self.root.destroy()

# if __name__ == "__main__":
#     ...
