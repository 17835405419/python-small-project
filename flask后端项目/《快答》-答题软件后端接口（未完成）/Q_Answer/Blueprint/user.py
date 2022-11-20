"""
作者：zwq
日期:2022年08月14日
"""

from flask import Blueprint, request, jsonify, g
from server.user import add, find, code_add, code_find, code_update
from exts import mail
from flask_mail import Message  # 发送信息
import random
from werkzeug.security import check_password_hash
from verify import generate_token,validate_token


user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=['POST'])
def register():
    user = request.json
    if user:
        try:
            res = code_find(user["userMail"])
            if user["code"] == res["code"]:
                add(user)
                return {
                    "code": 0,
                    "mag": "用户注册成功"
                }
            else:
                return {
                    "code": 1,
                    "err": "验证码错误"
                }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "用户注册失败"
            }
    else:
        return {
            "code": 1,
            "err": "请正确输入数据"
        }


@user_bp.route("/login", methods=["POST"])
def login():
    """ 登录功能的实现 """
    user = request.json
    if user:
        try:
            user_res = find(user["userName"])

            if user_res["userName"] and check_password_hash(user_res["password"], user["password"]):
                token = generate_token(user_res["userName"])
                token = str(token).split("'")[1]
                return jsonify(
                    {
                        "code": 0,
                        "msg": "登录成功",
                        "token": token
                    }
                )
            else:
                return {
                    "code": 1,
                    "err": "账号或密码错误"
                }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "登录失败"
            }
    else:
        return {
            "code": 1,
            "err": "请输入信息"
        }


@user_bp.route("/email", methods=["GET"])
def email_send():
    """
        发送邮件函数  subject 为 邮件标题
        recipients 接受者

    """

    # now_time = time.strftime('%H:%M:%S',time.localtime(time.time())).split(":")
    # # 调用该函数 当前时间
    # present_time = int(now_time[0])*3600+int(now_time[1])*60+int(now_time[2])
    # # 规定发送间隔为一分钟
    # if not g.send_time:
    #     g.send_time = 0
    #
    # if present_time - g.send_time > 60 :

    # 传递参数 qq号
    email = request.args["email"]

    # 验证码
    code = ''
    for i in range(4):
        code = code + str(random.randint(1, 9))

    try:
        # send_times = time.strftime('%H:%M:%S', time.localtime(time.time())).split(":")
        # # 发送时间时间
        # send_time_handle = int(send_times[0]) * 3600 + int(send_times[1]) * 60 + int(send_times[2])
        # # 全局挂载 发送时间

        message = Message(subject="Q_answer 注册邮件", recipients=[email], body=f'您的邮箱验证码是{code}，请妥善保管')
        mail.send(message)
        # 判断是否存在该qq邮箱
        mail_res = code_find(email)
        if not mail_res:
            code_add({"userMail": email, "code": code})
        else:
            # 更新验证码
            code_update({"mail_res": mail_res, "code": code})
        return {
            "code": 0,
            "msg": "发送成功"
        }
    except Exception as e:
        print(e)
        return {
            "err": "发送失败"
        }
    # else:
    #     return {
    #         "code":1,
    #         "err":"发送频率过快"
    #     }


@user_bp.route("/getUserInfo", methods=["GET"])
def getUserInfo():
    token = request.args["token"]
    res = validate_token(token)
    if res:
        return res
    else:
        try:
            userInfo = find(g.userName, isShow=False)
            return {
                "code": 0,
                "userInfo": userInfo
            }
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "该用户不存在"
            }

