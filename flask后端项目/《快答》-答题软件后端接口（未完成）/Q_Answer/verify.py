"""
作者：zwq
日期:2022年08月17日
"""
from configs import SECRET_KEY
from authlib.jose import jwt, JoseError
from flask import g


# 生成token
def generate_token(userName):
    """ 生成token """
    # 签名算法
    header = {'alg': 'HS256'}
    # 待签名的数据负载 "exp"token 过期时间
    data = {'userName': userName, "exp": 7200}
    return jwt.encode(header=header, payload=data, key=SECRET_KEY)



def validate_token(token):
    """ 解密token """
    try:
        data = jwt.decode(token, SECRET_KEY)
        g.userName = data["userName"]
    except JoseError as e:
        print(e)
        return {
            "code": 1,
            "error": e.error
        }

#
