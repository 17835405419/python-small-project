"""
作者：zwq
日期:2022年11月05日
"""
import asyncio
import aiohttp
import aiofiles

from lxml import etree
from 随机ip.randomIp import RandomIp


class BqbSpider:
    def __init__(self):
        # 实例化获取ip类
        self.ip = RandomIp()
        self.main_url = "https://www.doutub.com"
        self.headers = {
            'Origin': 'https://www.doutub.com',
            'Referer': 'https://www.doutub.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',

        }

    async def _request(self, url, arg="text"):
        """
        :param url: 请求的url
        :param arg: 规定返回的数据格式
        :return: 返回数据
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as res:
                if arg == "text":
                    return await res.text()
                elif arg == "content":
                    return await res.read()

    async def _downLoad(self, html):
        """下载函数 ---下载子页面的图片 """
        tree = etree.HTML(html)
        src = tree.xpath("//div[@class='img-content']/img/@src")[0]
        img_name = tree.xpath("//h2/text()")[0]
        content = await self._request(src, arg="content")
        async with aiofiles.open(f"./tupian/{img_name}.jpg", mode="wb") as f:
            await f.write(content)
            print(f"over {img_name}")

    async def _getChildhref(self, html):
        """解析函数  --- 获取子页面的url """
        tree = etree.HTML(html)
        lists = tree.xpath("//div[@class='cell']/a/@href")
        href_lists = [self.main_url + i for i in lists]

        tasks = []
        for href in href_lists:
            tasks.append(asyncio.create_task(self._downLoad(await self._request(href))))
        await asyncio.wait(tasks)

    async def _main(self, url, page=1):
        """
        主函数入口
        :param url: 爬取的网页
        :param page: 爬取的页数
        """
        for i in range(10, page + 1):
            main_html = await self._request(url.replace(url.split("/")[-1], str(i)))

            await self._getChildhref(main_html)

    def start(self, url, page):
        """启动爬虫"""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._main(url, page))


if __name__ == '__main__':
    url = "https://www.doutub.com/img_lists/new/1"
    spider = BqbSpider()
    spider.start(url, 10)
