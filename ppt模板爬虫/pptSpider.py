"""
作者：zwq
日期:2022年10月30日
"""

import requests
from lxml import etree
from selenium.webdriver import Firefox, FirefoxOptions

from selenium.webdriver.common.by import By


class PptSpider():
    def __init__(self, page):
        # 爬取的页数
        self.page = page
        # 实例化属性
        options = FirefoxOptions()
        # 由于火狐浏览器未安装在默认位置 所以需要手动配置
        options.binary_location = r"D:/Firefox/firefox.exe"
        # 自定义下载地址
        options.set_preference("browser.download.folderList", 2)  # 默认地址 改 自定义地址
        options.set_preference("browser.download.dir", r"./ppt模板")
        # # 实例化浏览器
        self.driver = Firefox(options=options)

        self.mian_url = 'https://www.51pptmoban.com/'

    def _request(self, url):
        # 请求方法
        request = requests.get(url)
        request.encoding = "gb2312"
        return request.text

    def _tree(self, text):
        # 解析方法
        tree = etree.HTML(text)
        return tree

    def _analysis_main_url(self):
        # 解析主页面
        href_join_lists = []
        for num in range(1,self.page+1):
            url = f"https://www.51pptmoban.com/ppt/index_{num}.html"
            resp = self._request(url)
            tree = self._tree(resp)
            hrefList = tree.xpath("//div[@class='pdiv']/a/@href")
            # 拼接好的子页面列表
            href_join_list = [self.mian_url + href for href in hrefList]
            href_join_lists.extend(href_join_list)
        return href_join_lists

    def _analysis_child_url(self):
        # 解析子页面
            child_url_lists = self._analysis_main_url()
            down_href_lists = []
            for child_url in child_url_lists:
                child_resp = self._request(child_url)
                child_tree = self._tree(child_resp)
                child_href = child_tree.xpath("//div[@class='ppt_xz']/a/@href")[0]
                join_url = self.mian_url + child_href
                down_href_lists.append(join_url)
            return down_href_lists

    def main(self):
        down_href_list = self._analysis_child_url()
        for down_href in down_href_list:
            self.driver.get(down_href)
            self.driver.find_element(By.XPATH, "//a[@class='tjd0']").click()
            print("over 一个")
        print("over all")


if __name__ == '__main__':
    pptSpider = PptSpider(page=2)
    pptSpider.main()
