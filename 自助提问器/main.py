"""
作者：zwq
日期:2022年08月22日
"""
from question import AskQuestion, question
# 导入gui 库
import tkinter as tk
# 导入上传组件
from tkinter import filedialog
# 导入弹窗
from tkinter import messagebox


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("强哥自助提问器")
        self.root.geometry('450x300')
        self.frm = tk.Frame(self.root)
        self.entry1 = tk.Entry(self.frm, width='40')
        # 滚动条
        self.scale1 = tk.Scale(self.root, from_=100, to=500, orient=tk.HORIZONTAL, tickinterval=100, length=200)

        # 实例化播报类
        self.bobao = AskQuestion()

    def interface(self):
        # 上传控件
        print(1)
        self.frm.grid(padx='20', pady='20')
        btn = tk.Button(self.frm, text='上传文件', command=self.upload_file)
        btn1 = tk.Button(self.frm, text='随机提问', command=self.main)
        btn2 = tk.Button(self.frm, text='语速更换', command=self.change)
        btn.grid( column=0, ipadx='3', ipady='3', padx='10')
        btn1.grid( column=1, ipadx='6', ipady='3', padx='10')
        btn2.grid()
        # 滚动条
        self.scale1.grid()

        # 默认100
        self.scale1.set(100)
        # 上传框
        self.entry1.grid(row=0, column=1)
        # 显示gui
        self.root.mainloop()

    # 上传操作
    def upload_file(self):

        selectFile = tk.filedialog.askopenfilename()
        self.entry1.insert(0, selectFile)
        self.filePath = self.entry1.get()  # 获取上传文件的路径
        if self.filePath.split('.')[-1] != 'xlsx':
            messagebox.showinfo(title="出错了！！！", message='上传文件失败！')
            self.entry1.delete(0, 'end')
        else:
            # 实例化 问题类
            self.question = question(self.filePath)

    def change(self):
        """ 更换语速"""
        try:
            rate = self.scale1.get()
            self.bobao.setRate(rate)
            messagebox.showinfo(title="成功", message='速度更改成功！')
        except Exception as e:
            messagebox.showerror(title="出错了！！！", message=e)

    # 主函数入口
    def main(self):
        print("播报开始")
        questionRandom = self.question.getquestion()
        self.bobao.speak(questionRandom)


# 启动界面
gui = Gui()
gui.interface()
