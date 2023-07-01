# -*- coding: utf-8 -*-
"""

"""
from OpenGL.GL import *
from OpenGL.raw.GLU import gluLookAt, gluPerspective
from OpenGL.raw.GLUT import glutSwapBuffers, glutSolidCube
from pyopengltk import OpenGLFrame

from TkGUI import *
from xml_reader import *


class TkinterGUI:
    def __init__(self):
        self.root = tk.Tk()
        set_window(self.root, "My Server")
        self.notebook_main = ttk.Notebook(self.root)
        self.Bottom = BottomFrame(self.root, redirect=False)
        self.Left = LeftFrame(self.root)
        # 初始化标签页
        self.Frame_3D = tk.Frame(bg=BG_COLOUR)
        self.Frame_2 = tk.Frame(bg=BG_COLOUR)
        self.notebook_main.add(self.Frame_3D, text='   3D预览   ')
        self.notebook_main.add(self.Frame_2, text='   Func2   ')
        self.notebook_main.pack(fill='both', side='right', expand=True)
        self.FrameServerObj = None
        self.FrameClientObj = None


class BottomFrame(CodeEditor):
    """
    The bottom frm of the main root.
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


class LeftFrame:
    """
    The left frame of the main root, which contains the entry box, the start button and the play button.
    """

    def __init__(self, frm):
        self.basic = tk.Frame(master=frm, bg=BG_COLOUR, width=320)
        self.basic.propagate(0)
        self.basic.pack(side='left', padx=15, pady=5, fill='y', expand=False)
        main_title(self.basic, text='PTB 图纸信息', side='top')
        # 检索Designs文件夹下的所有xml文件
        self.available_designs = [f[:-4] for f in os.listdir(
            'Designs') if os.path.isfile(os.path.join('Designs', f))]
        # 创建下拉框
        self.top1 = tk.Frame(master=self.basic, bg=BG_COLOUR)
        self.top1.pack(side='top', fill='x', expand=False, pady=8)
        self.combox = text_with_combox(
            self.top1, '选择设计:', (FONT0, FONT_SIZE), 9, 15, self.available_designs, False)
        self.combox.box.bind('<<ComboboxSelected>>', self.combox_update)
        self.combox.box.bind('<Return>', self.combox_update)
        self.combox.box.bind('<Leave>', self.combox_update)
        self.combox.box.bind('<FocusOut>', self.combox_update)
        # 创建2列的treeview，但是要隐藏第一行表头
        # 用style设置行高和字体，居中显示
        style = ttk.Style()
        style.configure(
            "Treeview", rowheight=36, font=(FONT0, FONT_SIZE), foreground=FG_COLOUR, background=BG_COLOUR)
        self.tree = ttk.Treeview(
            self.basic, columns=('key', 'value'), show="headings", height=12, style="Treeview")
        self.tree['show'] = ''
        self.tree.column('key', width=125, anchor='e')
        self.tree.column('value', width=165, anchor='center')
        self.tree.heading('key', text="", anchor="w")
        self.tree.heading('value', text="", anchor="w")
        self.tree.pack(side='top', expand=False)
        # 信息
        self.last_design = None
        self.DesignReader = None

    def combox_update(self, event):
        """
        更新treeview
        :return:
        """
        if self.last_design == self.combox.box.get():
            return
        file_name = self.combox.box.get()+'.xml'
        path = os.path.join(os.path.abspath('.'), 'Designs', file_name)
        self.DesignReader = ReadDesign(path)
        self.update_treeview()
        self.last_design = self.combox.box.get()

    def update_treeview(self):
        """
        更新treeview
        :return:
        """
        # 清空treeview
        DR = self.DesignReader
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 插入信息
        self.tree.insert('', 'end', values=('设计师', DR.Designer))  # 设计师
        self.tree.insert('', 'end', values=('设计师ID', DR.DesignerID))  # 设计师ID
        self.tree.insert('', 'end', values=('战舰类型', DR.Type))  # 战舰类型
        self.tree.insert('', 'end', values=('排水量', str(DR.Displacement_in_t) + "t"))  # 排水量
        self.tree.insert('', 'end', values=('总体积', str(DR.Volume_in_m) + "m³"))  # 总体积
        self.tree.insert('', 'end', values=('排水体积比', str(DR.weight_ratio)))  # 排水体积比
        self.tree.insert('', 'end', values=('水线长', str(DR.Length_in_m) + "m"))  # 水线长
        self.tree.insert('', 'end', values=('水线宽', str(DR.Width_in_m) + "m"))  # 水线宽
        self.tree.insert('', 'end', values=('舰高', str(DR.Height_in_m) + "m"))  # 舰高
        self.tree.insert('', 'end', values=('吃水深度', str(DR.Draft_in_m) + "m"))  # 吃水
        self.tree.insert('', 'end', values=('方形系数', str(DR.SquareCoefficient)))  # 方形系数
        self.tree.insert('', 'end', values=('阻力系数', str(DR.Drag)))  # 阻力系数


def show_text(text, mode):
    GUI.Bottom.result.config(state='normal')
    GUI.Bottom.result.insert('end', text + '\n', mode)
    GUI.Bottom.result.config(state='disabled')


class MyOpenGLFrame(OpenGLFrame):
    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    def redraw(self):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluPerspective(45, self.width / self.height, 0.1, 50.0)
            gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)
            self.draw_cube(2)
            self.tkSwapBuffers()

    def draw_cube(self, size):
        vertices = [
            [size / 2, -size / 2, -size / 2],
            [size / 2, size / 2, -size / 2],
            [-size / 2, size / 2, -size / 2],
            [-size / 2, -size / 2, -size / 2],
            [size / 2, -size / 2, size / 2],
            [size / 2, size / 2, size / 2],
            [-size / 2, -size / 2, size / 2],
            [-size / 2, size / 2, size / 2]
        ]

        faces = [
            [0, 1, 2, 3],  # 前面
            [3, 2, 7, 6],  # 左面
            [6, 7, 5, 4],  # 后面
            [4, 5, 1, 0],  # 右面
            [1, 5, 7, 2],  # 上面
            [4, 0, 3, 6]  # 底面
        ]

        normals = [
            [0, 0, -1],  # 前面
            [-1, 0, 0],  # 左面
            [0, 0, 1],  # 后面
            [1, 0, 0],  # 右面
            [0, 1, 0],  # 上面
            [0, -1, 0]  # 底面
        ]

        glBegin(GL_QUADS)
        for face, normal in zip(faces, normals):
            glNormal3fv(normal)
            for vertex_index in face:
                glVertex3fv(vertices[vertex_index])
        glEnd()

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)



if __name__ == '__main__':
    GUI = TkinterGUI()
    app = MyOpenGLFrame(GUI.Frame_3D, width=1500, height=650)
    app.pack(side="top", expand=True)
    app.mainloop()

