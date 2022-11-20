"""
作者：zwq
日期:2022年08月13日
"""
# 将第三方插件导入启动 抽离出来 便于后期维护
from flask_mongoengine import MongoEngine
# 发送邮件插件
from flask_mail import Mail
# # jwt 相关插件
# from flask_httpauth import HTTPBasicAuth

db = MongoEngine()
mail = Mail()

