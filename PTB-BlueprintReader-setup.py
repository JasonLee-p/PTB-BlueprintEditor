"""
    This file is used to setup the PTB-BlueprintReader app.
"""
import base64
import os
import time
import tkinter as tk
import webbrowser
import zlib
from tkinter import ttk, messagebox

from win32com.client import Dispatch
from images.Img_main import *

import PROGRAM


def find_ptb():
    PTB_path = None
    # 从C盘开始寻找：
    # 优先在用户目录下寻找，先遍历所有账户名：
    for user in os.listdir('C:\\Users'):
        # 找到AppData/LocalLow/茕海开发组/工艺战舰Alpha
        if os.path.isdir(os.path.join('C:\\Users', user, 'AppData', 'LocalLow', '茕海开发组', '工艺战舰Alpha')):
            PTB_path = os.path.join('C:\\Users', user, 'AppData', 'LocalLow', '茕海开发组', '工艺战舰Alpha')
            break
    # 如果在用户目录下没有找到，就在C盘根目录下寻找
    if PTB_path is None:
        for root, dirs, files in os.walk('C:\\'):
            if '工艺战舰Alpha' in dirs:
                PTB_path = os.path.join(root, '工艺战舰Alpha')
                break
    return PTB_path


class MainWindow:
    def __init__(self):
        # -------------------------------------------------------------------------------Path
        self.PATH = None
        # -------------------------------------------------------------------------------Window
        self.window = tk.Tk()
        self.window.title('工艺战舰图纸阅读器v0.0.4——安装程序')  # 窗口名
        self.window.geometry('700x600')  # 窗口大小
        self.window.resizable(width=False, height=False)  # 窗口大小不可变
        self.window.configure(bg=BG_COLOR2)  # 窗口背景色
        self.transparent_color = 'gray'  # 透明色
        self.window.attributes("-transparentcolor", self.transparent_color)

        self.ICO = tk.PhotoImage(data=base64.b64decode(ICO))
        self.LOGO = tk.PhotoImage(data=base64.b64decode(LOGO))
        self.window.iconphoto(True, self.ICO)
        # -------------------------------------------------------------------------------Left
        self.Left = tk.Frame(self.window, width=230, height=600, bg=BG_COLOR)
        self.Left.pack(side='left', fill='y')
        self.Left.pack_propagate(0)
        tk.Label(self.Left, image=self.ICO, bg=BG_COLOR).pack(side='top', pady=20)
        self.Left0 = tk.Frame(self.Left, bg=BG_COLOR)
        tk.Label(self.Left0, text='联系我们：', font=('微软雅黑', 9), bg=BG_COLOR).pack(anchor='w', pady=0)
        tk.Label(self.Left0, text='邮箱：2593292614@qq.com', font=('微软雅黑', 9), bg=BG_COLOR).pack(anchor='w', pady=0)
        tk.Label(self.Left0, text='Github：JasonLee-p', font=('微软雅黑', 9), bg=BG_COLOR).pack(anchor='w', pady=0)
        self.Left0.pack(side='bottom', fill='x', pady=25, padx=25)
        # -------------------------------------------------------------------------------Right
        tk.Frame(self.window, width=15, bg=BG_COLOR2).pack(side='left', fill='y')
        tk.Frame(self.window, width=15, bg=BG_COLOR2).pack(side='right', fill='y')
        self.Right = tk.Frame(self.window, width=460, height=600, bg=BG_COLOR)
        self.Right.pack(side='right', fill='both', pady=15, padx=0)
        self.Right.pack_propagate(0)
        self.Right1 = tk.Frame(self.Right, bg=BG_COLOR, pady=160)
        self.Right2 = tk.Frame(self.Right, bg=BG_COLOR, pady=160)
        self.Right3 = tk.Frame(self.Right, bg=BG_COLOR, pady=160)
        tk.Label(self.Right3, text='  安装进度：', font=('微软雅黑', 12), bg=BG_COLOR).pack(side='top', pady=0)
        self.style = ttk.Style()
        self.style.configure('1.TButton', font=('微软雅黑', 18), foreground=FRONT_COLOR, background=BG_COLOR)
        self.style.configure('red.Horizontal.TProgressbar', foreground='red', background='red')
        self.bar_frame = tk.Frame(self.Right3, bg=BG_COLOR)
        self.bar_frame.pack(side='top', pady=0)
        self.progressbar = ttk.Progressbar(self.bar_frame, length=300,
                                           mode='determinate', style='red.Horizontal.TProgressbar')
        self.progressbar.pack(side='left', pady=5)
        self.StrVar = tk.StringVar()
        self.StrVar.set('0%')
        tk.Label(self.bar_frame, textvariable=self.StrVar, font=('微软雅黑', 12), bg=BG_COLOR).pack(
            side='left', pady=0)

        # -------------------------------------------------------------------------------Right1
        self.Right1.pack(side='top', fill='both', expand=True)
        tk.Label(self.Right1, text='Process The Battleship', font=('微软雅黑', 20), bg=BG_COLOR).pack(side='top', pady=0)
        tk.Label(self.Right1, text='———图纸阅读器———', font=('微软雅黑', 30), bg=BG_COLOR).pack(side='top', pady=0)
        tk.Frame(self.Right1, bg=BG_COLOR, height=100).pack(side='top', pady=0)
        ttk.Button(master=self.Right1, style='1.TButton', text='快速开始', command=self.install0, width=15).pack(
            side='bottom', pady=0)

    def install0(self):
        self.Right1.destroy()
        self.Right2.pack(side='top', fill='both', expand=True)
        tk.Frame(self.Right2, bg=BG_COLOR, height=10).pack(side='top', pady=0)
        tk.Label(self.Right2, text='. . . 正在寻找工艺战舰目录 . . .',
                 font=('微软雅黑', 10), bg=BG_COLOR).pack(side='top', pady=0)
        self.PATH = find_ptb()
        if self.PATH is None:
            tk.Label(self.Right2, text='未找到目录，请安装工艺战舰！',
                     font=('微软雅黑', 18), bg=BG_COLOR, foreground='firebrick').pack(side='top', pady=0)
            tk.Frame(self.Right2, bg=BG_COLOR, height=112).pack(side='top', pady=0)
            ttk.Button(master=self.Right2, style='1.TButton', text='下载PTB', command=self.no_ptb, width=15).pack(
                side='bottom', pady=0)
        else:
            tk.Label(self.Right2, text='  已找到目录：',
                     font=('微软雅黑', 18), bg=BG_COLOR, foreground=FRONT_COLOR).pack(side='top', pady=0)
            tk.Label(self.Right2, text=self.PATH,
                     font=('微软雅黑', 10), bg=BG_COLOR, foreground="black").pack(side='top', pady=0)
            tk.Frame(self.Right2, bg=BG_COLOR, height=112).pack(side='top', pady=0)
            ttk.Button(master=self.Right2, style='1.TButton', text='确认安装', command=self.install1, width=15).pack(
                side='bottom', pady=0)

    def no_ptb(self):
        webbrowser.open('https://gongyizhanjian.qionghaigame.com/')
        self.window.destroy()

    def install1(self):
        self.Right2.destroy()
        self.Right3.pack(side='top', fill='both', expand=True)
        # 显示进度条
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = 100
        setup_succeed = self.setup()
        if setup_succeed:
            tk.Label(self.Right3, text='  安装成功！',
                     font=('微软雅黑', 18), bg=BG_COLOR, foreground=FRONT_COLOR).pack(side='top', pady=0)
            tk.Frame(self.Right3, bg=BG_COLOR, height=90).pack(side='top', pady=0)
            ttk.Button(master=self.Right3, style='1.TButton', text='打开程序', command=self.open, width=15).pack(
                side='bottom', pady=0)
            tk.Label(self.Right3, text='若首次安装，请手动用管理员模式打开桌面快捷方式',
                     font=('微软雅黑', 10), bg=BG_COLOR, foreground='black').pack(side='bottom', pady=0)
        else:
            tk.Label(self.Right3, text='  安装失败！',
                     font=('微软雅黑', 18), bg=BG_COLOR, foreground='firebrick').pack(side='top', pady=0)
            tk.Frame(self.Right3, bg=BG_COLOR, height=112).pack(side='top', pady=0)
            ttk.Button(master=self.Right3, style='1.TButton', text='重试', command=self.install1, width=15).pack(
                side='bottom', pady=0)
        self.window.update()

    def is_installed(self):
        if os.path.exists(os.path.join(self.PATH, 'PTB-BlueprintReader.exe')):
            return True
        else:
            return False

    def setup(self):
        # 删除旧版本
        old_version = self.is_installed()
        while old_version:
            if old_version:
                try:
                    os.remove(os.path.join(self.PATH, 'PTB-BlueprintReader.exe'))
                    old_version = self.is_installed()
                except PermissionError:
                    time.sleep(0.5)
                    messagebox.showerror('错误', '请关闭正在运行的旧版本！')
        # 把PGM从base64解码后写入exe文件
        path = os.path.join(self.PATH, 'PTB-BlueprintReader.exe')
        self.progressbar_update(10)
        with open(path, 'wb') as f:
            f.write(program_data)
        self.progressbar_update(30)
        # 在桌面生成该程序的快捷方式：
        # 1.获取桌面路径
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.progressbar_update(40)
        # 2.生成快捷方式（用win32com模块）
        shell = Dispatch("WScript.Shell")
        self.progressbar_update(50)
        shortcut_path = os.path.join(desktop_path, '工艺战舰图纸阅读器.lnk')
        shortcut = shell.CreateShortCut(shortcut_path)
        self.progressbar_update(60)
        shortcut.TargetPath = os.path.join(self.PATH, 'PTB-BlueprintReader.exe')
        self.progressbar_update(70)
        shortcut.WorkingDirectory = self.PATH
        self.progressbar_update(80)
        shortcut.Arguments = ''
        shortcut.WindowStyle = 1
        self.progressbar_update(90)
        shortcut.Description = '工艺战舰图纸阅读器'
        self.progressbar_update(100)
        shortcut.save()
        return True

    def open(self):
        # 给予桌面快捷方式管理员权限
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        shortcut_path = os.path.join(desktop_path, '工艺战舰图纸阅读器.lnk')
        os.system('powershell "Start-Process -Verb runAs -FilePath {}"'.format(shortcut_path))
        self.window.destroy()

    def progressbar_update(self, value):
        self.progressbar['value'] = value
        self.StrVar.set(str(value) + '%')
        self.bar_frame.update()


if __name__ == '__main__':
    FONT_SIZE = 10
    BG_COLOR = 'ivory'
    BG_COLOR2 = '#fafffc'
    FRONT_COLOR = '#aa3300'
    Root = MainWindow()
    program_data = base64.b64decode(PROGRAM.PGM)
    program_data = zlib.decompress(program_data)

    Root.window.mainloop()
