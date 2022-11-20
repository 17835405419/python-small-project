"""
作者：zwq
日期:2022年08月13日
"""
# 配置文件

# 数据库配置
db = "Q_asnswer"
host = "localhost"
port = 27017

MONGODB_SETTINGS = {
    "db": db,
    "host": host,
    "port": port
}

# 邮件配置

MAIL_SERVER = "smtp.qq.com"  # 选择什么邮件
MAIL_PORT = "587"  # 固定端口号
MAIL_USE_TLS = True
MAIL_USERNAME = "xxxxxxxxx@qq.com"  # qq账号
MAIL_PASSWORD = "xxxxxxx"
MAIL_DEFAULT_SENDER = "xxxxxxxx@qq.com"  # 默认发送者

# jwt 秘钥 ---自定义
SECRET_KEY = "acdf213hgf"
