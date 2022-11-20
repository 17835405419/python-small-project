"""
作者：zwq
日期:2022年03月06日
"""
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import kuwo
import time


class Winui():
    def __init__(self):
        # 创建一个主窗口对象
        self.window = Tk()

        # 设置标题
        self.window.title("音乐下载器")
        # 设置窗口大小
        self.window.geometry('550x400+400+150')

        # 显示输入框
        self.show_input()
        # 显示按钮
        self.show_btn()

        # 调用mainloop()显示主窗口
        self.window.mainloop()

    def show_input(self):
        # 标签
        self.lbl = Label(self.window, text="请输入搜索的歌曲名：")
        self.lbl.grid(column=0, row=0)
        # 输入框
        self.txt = Entry(self.window, width=30)
        self.txt.grid(column=1, row=0)
        self.lbl.place(relx=0.05, rely=0.05)
        self.txt.place(relx=0.3, rely=0.05)
        # 标签2
        self.lbl2 = Label(self.window, text="请输入下载数：")
        self.lbl2.grid(column=0, row=1)
        # 输入框2
        self.txt2 = Entry(self.window, width=30)
        self.txt2.grid(column=1, row=1)
        self.lbl2.place(relx=0.05, rely=0.1)
        self.txt2.place(relx=0.3, rely=0.12)

    #     显示按钮
    def show_btn(self):
        # 按钮
        btn = Button(self.window, text="确认", command=self.down_btn, height=2, width=7)
        btn.grid(column=2, row=0)
        btn.place(relx=0.7, rely=0.05)

    #     下载功能
    def down_btn(self):
        self.song_name = self.txt.get()
        self.song_num = self.txt2.get()
        self.lists = kuwo.main(self.song_name, self.song_num)
        if not self.song_name:
            return messagebox.showerror("提示", "请输入歌名")

        elif not self.song_num:
            return messagebox.showerror("提示", "请输入爬取数量")
        elif self.lists == '该文件夹已存在':
            return messagebox.showerror("提示", "该文件夹已存在")

        # # 显示下载进度
        self.show_progs()

    def show_down(self):
        # 创建Listbox控件
        listbox = Listbox(self.window, width=70, height=10)
        listbox.place(relx=0.05, rely=0.3)
        # 清除Listbox控件的内容
        listbox.delete(0, END)
        # 在Listbox控件内插入选项
        for i in range(int(self.song_num)):
            listbox.insert(END, self.lists[i])

    #     显示进度条
    def show_progs(self):
        bar = Progressbar(self.window, length=400)
        bar.grid(column=0, row=0)
        bar.place(relx=0.1, rely=0.21)
        i = 0
        while i < 100:
            time.sleep(0.2)
            i += 10
            bar['value'] = i
        if i == 100:
            self.show_down()
            messagebox.showinfo("提示", "下载完成")


wi = Winui()
