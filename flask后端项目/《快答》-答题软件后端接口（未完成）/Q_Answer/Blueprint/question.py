"""
作者：zwq
日期:2022年08月17日
"""

from flask import Blueprint, request, g
from server.question import add, findAll_class, find_one
import os
import datetime
# 导入excel工具类
from utils import Excel

question_bp = Blueprint("question", __name__, url_prefix="/question")


@question_bp.route("/up", methods=["POST"])
def up():
    question_info = request.form
    if question_info:
        try:
            add(question_info)
            return {
                "code": 0,
                "msg": "上传成功"
            }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "上传错误"
            }
    else:
        return {
            "code": 1,
            "err": "请输入内容"
        }


@question_bp.route("/upAll", methods=["POST"])
def upAll():
    """ 批量上传函数 """
    question_files = request.files["template"]
    if question_files:
        try:
            folderName = datetime.date.today()
            path = f"./upload/{folderName}/{g.userId}"
            if not os.path.exists(path):
                os.makedirs(path)
            question_files.save(f"{path}/template.xlsx")
            # 获取上传的数据
            data = Excel(f"{path}/template.xlsx").read()

            # 保存数据到数据库
            for i in data:
                add(i)
            return {
                "code": 0,
                "msg": "上传成功"
            }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "上传失败"
            }
    else:
        return {
            "code": 1,
            "err": "上传文件为空"
        }


@question_bp.route("/findAllByClass", methods=["GET"])
def findAllByClass():
    classification = request.args["classification"]
    if classification:
        try:
            question_info = findAll_class(classification)
            return {
                "code": 0,
                "data": question_info
            }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "查询出错"
            }
    else:
        return {
            "code": 1,
            "err": "请输入分类"
        }


@question_bp.route("/findAllById", methods=["GET"])
def findAllById():
    questionId = request.args["questionId"]
    if questionId:
        try:
            request_info = find_one(questionId)
            return {
                "code": 0,
                "data": request_info
            }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "查询出错"
            }
    else:
        return {
            "code": 1,
            "err": "Id不存在"
        }
