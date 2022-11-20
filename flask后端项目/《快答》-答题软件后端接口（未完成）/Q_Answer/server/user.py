"""
作者：zwq
日期:2022年08月15日
"""
import time
from model import User, Code
from werkzeug.security import generate_password_hash  # 密码加密 底层库


# 验证码操作
def code_add(code_info):
    code = Code(userMail=code_info["userMail"], code=code_info["code"])
    code.save()


def code_find(condition):
    res = Code.objects(userMail=condition).first()
    if res:
        return res


def code_update(data):
    """ BUG --> 修改后的时间为服务器时间   可以之后由客户端上传 """
    data["mail_res"].update(code=data["code"], createTime=time.time())


# 用户操作
# 增
def add(user):
    hash_password = generate_password_hash(user["password"])
    user = User(userName=user["userName"], userMail=user["userMail"], nickName=user["nickName"],
                password=hash_password)
    user.save()


def find(condition,isShow=True):
    if isShow:
        res = User.objects(userName=condition).first()
    else:
        res = User.objects(userName=condition).exclude("password", "createTime")

    if res:
        return res
