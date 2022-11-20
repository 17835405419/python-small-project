"""
作者：zwq
日期:2022年08月13日
"""
from flask import Flask, request, g
from exts import db, mail
# 导入配置
import configs
from verify import validate_token

# 导入蓝图
from Blueprint.user import user_bp
from Blueprint.question import question_bp

# 导入cros 解决跨域问题
from flask_cors import *

# 初始化app
app = Flask(__name__)
# 解决跨域 配置
CORS(app, supports_credentials=True)

# 加载配置文件
app.config.from_object(configs)

# db绑定app
db.init_app(app)
mail.init_app(app)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(question_bp)


# 每次请求之前处理操作
@app.before_request
def before_request():
    """ 登录权限检测 """
    if request.path in ["/user/login", "/user/register", "/user/email"]:
        return
    else:
        try:
            token = request.headers["Token"]
            res = validate_token(token)
            return res
        except Exception as e:
            print(e)
            return {
                "code": 1,
                "err": "请输入token"
            }


if __name__ == '__main__':
    app.run(debug=True)
