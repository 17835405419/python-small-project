"""
作者：zwq
日期:2022年08月09日
"""
import math
from PIL import ImageFont, Image, ImageDraw
# 导入操作word库
from docx import Document
# 导入gui 库
import tkinter as tk
# 导入上传组件
from tkinter import filedialog
# 导入弹窗
from tkinter import messagebox


# gui 界面
def gui():
    root = tk.Tk()
    root.title("强哥作业自动生成器")
    root.geometry('450x300')

    # 上传控件
    frm = tk.Frame(root)
    frm.grid(padx='20', pady='50')
    btn = tk.Button(frm, text='上传文件', command=upload_file)
    btn1 = tk.Button(frm, text='生成作业', command=main)
    btn.grid(row=0, column=0, ipadx='3', ipady='3', padx='10', pady='20')
    btn1.grid(row=3, column=1, ipadx='6', ipady='3', padx='10', pady='20')

    global entry1
    entry1 = tk.Entry(frm, width='40')
    entry1.grid(row=0, column=1)
    # 标签
    label = tk.Label(root, text="""点击上传文件，选择.docx后缀的文档，点击生成。\n（文件会自动保存在根目录work文件下）""")
    label.grid(row=4, column=0)

    root.mainloop()


# 上传操作
def upload_file():
    selectFile = tk.filedialog.askopenfilename()
    entry1.insert(0, selectFile)
    global filePath
    filePath = entry1.get()
    if filePath.split('.')[-1] != 'docx':
        messagebox.showinfo(title="出错了！！！", message='上传文件失败！')
        entry1.delete(0, 'end')


# 函数： 获取word文本内容
def getText():
    text = ''
    # 打开word文档
    document = Document(filePath)
    # 获取所有段落
    all_paragraphs = document.paragraphs
    for paragraph in all_paragraphs:
        # 打印每一个段落的文字
        text += paragraph.text
    return text


# 函数： 将文字写到背景图上
def draws(im1, text, h):
    # 加载背景图片
    draw = ImageDraw.Draw(im1)
    draw.text((30, h), text, (0, 0, 0), font=font)


# 主程序
def main():
    # 获取作业内容
    texts = getText()
    # 行数  向上取整
    rowNum = math.ceil(len(texts) / 30)
    # 页数
    pageNum = math.ceil(rowNum / 24)
    for page in range(pageNum):
        img = Image.open(imageFile)
        h = 70
        for i in range(24 * page, 24 * (page + 1)):
            text = texts[i * 30:(i + 1) * 30]
            draws(img, text, h)
            h += 42
        img.save(f"./work/work{page + 1}.png")
    messagebox.showinfo(title="成功", message="生成成功")
    entry1.delete(0, 'end')


if __name__ == '__main__':
    # 设置字体，如果没有，也可以不设置
    font = ImageFont.truetype("./font/font.ttf", 25)

    # 背景图片地址
    imageFile = "./bgc/bgc.gif"
    # 定义一个上传文件路径

    # 调用gui主程序
    try:
        gui()
    except:
        messagebox.showerror(title="出错", message="发生未知错误")
