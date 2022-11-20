"""
作者：zwq
日期:2022年08月13日
"""
# 数据库的数据模型
import time

from exts import db


class User(db.Document):
    """ 用户模型 """
    userId = db.IntField(default=time.time, unique=True)  # 用户Id---》唯一
    userName = db.IntField(required=True, max_length=11)  # 用户名 整数型
    userMail = db.EmailField(required=True, unique=True)  # 邮箱
    nickName = db.StringField(required=True, max_length=10)  # 昵称
    password = db.StringField(required=True)  # 密码
    createTime = db.IntField(default=time.time, unique=True)


class Code(db.Document):
    """ 存储验证码模型 """
    userMail = db.EmailField(required=True)  # 邮箱
    code = db.StringField(required=True, max_length=4)  # 验证码
    createTime = db.IntField(default=time.time)


class Question(db.Document):
    """ 存储问题的模型 """
    questionId = db.SequenceField(unique=True)  # 生成自动递增的数值
    subject = db.StringField(required=True)  # 题目
    answer = db.ListField(required=True)  # 答案
    answerTrue = db.ListField(required=True)  # 正确答案
    analysis = db.StringField(null=True)
    classification = db.StringField()  # 分类
