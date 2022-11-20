"""
作者：zwq
日期:2022年02月24日
"""
import os
import shutil  # 迁移文件模块
import glob     # 查找路径模块

src_path = './'
new_path = './分类文件夹'
if not os.path.exists(new_path):
    os.mkdir(new_path)

# 计数
file_num = 0
dir_num = 0

for file in glob.glob(f'{src_path}/**/*',recursive=True):
    if os.path.isfile(file):
        filename = os.path.basename(file)
        if '.' in filename:
            suffix = filename.split('.')[-1]
        else:
            suffix = '未分类'
        if not os.path.exists(f'{new_path}/{suffix}'):
            os.mkdir(f'{new_path}/{suffix}')
            dir_num += 1
        shutil.copy(file,f'{new_path}/{suffix}')
        file_num +=1
print(f'有{dir_num}个文件夹被创建，{file_num}个文件被分类')

