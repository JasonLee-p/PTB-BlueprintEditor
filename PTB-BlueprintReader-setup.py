"""
    This file is used to setup the PTB-BlueprintReader app.
"""
import base64
import ctypes
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk
from win32com.client import Dispatch

import Data.PROGRAM as PROGRAM


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
    # 如果在C盘根目录下没有找到，就在所有其他盘符下寻找
    # 检测所有可用盘符
    if PTB_path is None:
        for i in range(65, 91):
            vol = chr(i) + ':\\'
            if os.path.isdir(vol):
                for root, dirs, files in os.walk(vol):
                    if '工艺战舰Alpha' in dirs:
                        PTB_path = os.path.join(root, '工艺战舰Alpha')
                        break
            if PTB_path is not None:
                break
    # 如果还是没有找到，就报错
    if PTB_path is None:
        raise FileNotFoundError('未找到工艺战舰Alpha目录，请检查是否安装了工艺战舰Alpha\n'
                                'https://gongyizhanjian.qionghaigame.com/')
    return PTB_path


def setup():
    global PATH, Unfinished, ProgramFinished
    count1 = 0
    count2 = 0
    while Unfinished:
        print('正在安装...')
        if PATH is not None and count1 == 0:
            tk.Label(window, text=f'找到路径{PATH}', font=('微软雅黑', FONT_SIZE), bg='beige').pack()
            tk.Label(window, text='...正在生成程序...', font=('微软雅黑', FONT_SIZE), bg='beige').pack()
            count1 += 1
        if ProgramFinished and count2 == 0:
            tk.Label(window, text='...正在生成快捷方式...', font=('微软雅黑', FONT_SIZE), bg='beige').pack()
            tk.Label(window, text='安装完成！', font=('微软雅黑', 20), bg='beige').pack(pady=20)
            style = ttk.Style()
            style.configure('TButton', font=('微软雅黑', 20), foreground='firebrick', background='beige')
            button = ttk.Button(window, text='立即启动', command=start)
            button.config(style='TButton')
            button.pack(pady=10)
            count2 += 1


def start():
    global PATH
    try:
        # 变更目录
        os.chdir(PATH)
        # 启动程序
        subprocess.run('powershell -Command "Start-Process -FilePath '
                       f'\'{os.path.join(PATH, "PTB-BlueprintReader.exe")}\' -Verb RunAs"')
        window.destroy()
    except Exception as e:
        if "不是有效的 Win32 应用程序。" in str(e):
            e = "错误码：001\n"
            e += "安装的程序出现了问题，请联系作者\n"
            tk.Label(window, text=f'启动失败！\n{e}', font=('微软雅黑', FONT_SIZE), bg='beige',
                     foreground='firebrick').pack(side='bottom', ipady=20)
        elif "找不到指定的文件。" in str(e):
            e = "错误码：002\n"
            e += "找不到应用程序，请检查是否正确安装了工艺战舰图纸阅读器\n"
            tk.Label(window, text=f'启动失败！\n{e}', font=('微软雅黑', FONT_SIZE), bg='beige',
                     foreground='firebrick').pack(side='bottom', ipady=20)
        else:
            e = "错误码：003\n"
            e += "未知错误，请联系作者\n"
            tk.Label(window, text=f'启动失败！\n{e}', font=('微软雅黑', FONT_SIZE), bg='beige',
                     foreground='firebrick').pack(side='bottom', ipady=20)


def check_whether_installed():
    global PATH
    # 在安装路径下寻找PTB-BlueprintReader.exe
    if os.path.isfile(os.path.join(PATH, 'PTB-BlueprintReader.exe')):
        # 检查是否和当前版本一致
        with open(os.path.join(PATH, 'PTB-BlueprintReader.exe'), 'rb') as f2:
            if f2.read() == base64.b64decode(PROGRAM.PGM):
                # 一致，不需要安装
                return True
            else:
                # 不一致，需要重新安装
                return False


if __name__ == '__main__':
    # 给自己加上管理员权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    FONT_SIZE = 10
    PATH = None
    Unfinished = True
    ProgramFinished = False
    window = tk.Tk()
    window.title('工艺战舰图纸阅读器————安装程序')  # 窗口名
    window.geometry('800x450')  # 窗口大小
    window.resizable(width=False, height=False)  # 窗口大小不可变
    window.configure(bg='beige')  # 背景色
    # 生成窗口内容
    tk.Frame(window, width=800, height=45, bg='beige').pack()
    tk.Label(window, text='工艺战舰图纸阅读器  安装程序', font=('微软雅黑', 25), bg='beige').pack(pady=20)
    tk.Label(window, text='...正在寻找您的工艺战舰路径...', font=('微软雅黑', FONT_SIZE), bg='beige').pack()
    t = threading.Thread(target=setup)
    t.start()
    PATH = find_ptb()
    # 检查是否已经安装
    if check_whether_installed():
        # 已经安装，直接启动
        tk.Label(window, text='...您的程序已经是最新版本，即将启动...', font=('微软雅黑', FONT_SIZE), bg='beige').pack()
        time.sleep(1)
        start()
    else:  # 未安装，开始安装
        try:
            # 把PGM从base64解码后写入exe文件
            path = os.path.join(PATH, 'PTB-BlueprintReader.exe')
            with open(path, 'wb') as f:
                f.write(base64.b64decode(PROGRAM.PGM))
            ProgramFinished = True
            # 在桌面生成该程序的快捷方式：
            # 1.获取桌面路径
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            # 2.生成快捷方式（用win32com模块）
            shell = Dispatch("WScript.Shell")
            shortcut_path = os.path.join(desktop_path, '工艺战舰图纸阅读器.lnk')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = os.path.join(PATH, 'PTB-BlueprintReader.exe')
            shortcut.WorkingDirectory = PATH
            shortcut.Arguments = ''
            shortcut.WindowStyle = 1
            shortcut.Description = '工艺战舰图纸阅读器'
            shortcut.save()

        except Exception as _e:
            if "拒绝访问。" in str(_e):
                _e = "错误码：004\n"
                _e += "拒绝访问，请以管理员身份运行程序\n"
                tk.Label(window, text=f'安装失败！\n{_e}', font=('微软雅黑', FONT_SIZE), bg='beige',
                         foreground='firebrick').pack(side='bottom', ipady=20)
            else:
                _e = "错误码：005\n"
                _e += "未知错误，请联系作者\n"
                tk.Label(window, text=f'安装失败！\n{_e}', font=('微软雅黑', FONT_SIZE), bg='beige',
                         foreground='firebrick').pack(side='bottom', ipady=20)
    Unfinished = False
    # 弹出消息框
    if ProgramFinished:
        tk.Label(window, text='...安装完成，即将启动...', font=('微软雅黑', FONT_SIZE), bg='beige').pack()
    window.mainloop()
