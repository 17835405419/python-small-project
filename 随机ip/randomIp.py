"""
作者：zwq
日期:2022年07月08日
"""
from pymongo import MongoClient
import random


class RandomIp:
    # 获取数据库中的ip
    def __init__(self):
        self.cliet = MongoClient("localhost",27017)
        self.db = self.cliet["random_ip"]
        # 选择一个集合
        self.col = self.db["ip_list"]

    def change_ip(self):
        # 获取数据
        ipdict = self.col.find()
        # 列表推导式
        iplist = [f'http://{i["ip"]}:{i["port"]}' for i in ipdict]
        # 随机选一个
        ip = random.choice(iplist)
        return ip


if __name__ == '__main__':
    ip = RandomIp()
    ip = ip.change_ip()
    print(ip)

