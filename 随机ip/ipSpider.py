"""
作者：zwq
日期:2022年07月08日
"""
from pymongo import MongoClient
import requests
from lxml import etree


def downPy(item):
    with MongoClient("localhost", 27017) as cliet:
        db = cliet["random_ip"]
        # 选择一个集合
        col = db["ip_list"]
        # 插入数据
        result = col.insert_one(item)
        if result:
            print("保数一条数据成功")


def main(url):
    resp = requests.get(url)
    tree = etree.HTML(resp.text)
    node_list = tree.xpath("//table/tbody/tr")
    for node in node_list:
        ip_content = node.xpath("./td[1]/text()")[0]
        port_content = node.xpath("./td[2]/text()")[0]
        address = node.xpath("./td[5]/text()")[0]
        # 封装一个字典
        item = {"ip": ip_content, "port": port_content, "address": address}
        downPy(item)


if __name__ == '__main__':
    num = int(input("输入爬取的页数:"))
    for i in range(1, num + 1):
        first_url = f"https://free.kuaidaili.com/free/inha/{i}/"
        main(first_url)
