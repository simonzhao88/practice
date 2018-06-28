import json

import aiohttp
import asyncio

from pymongo import MongoClient


class DouBanMovie(object):

    def __init__(self):
        self.tag_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
        self.tags = []
        self.move_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s' \
                        '&sort=recommend&page_limit=20&page_start=%s'
        self.page = 10
        self.conn = MongoClient('mongodb://127.0.0.1:27017')
        db = self.conn['spider']
        self.connection = db['douban']

    async def get_html_info(self):
        """
        爬取数据
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.tag_url) as response:
                tags = await self.parse(await response.text())
                self.tags = tags['tags']

            for tag in self.tags:
                for start_page in range(self.page):
                    async with session.get(self.move_url % (tag, start_page*20)) as response:
                        data = await self.parse(await response.text())
                        for movie_info in data['subjects']:
                            await self.save(movie_info)

    async def parse(self, response):
        """
        处理数据
        :param response:
        :return:
        """
        data_json = json.loads(response)
        return data_json

    async def save(self, data):
        """
        保存到数据库
        :param data:
        :return:
        """
        self.connection.insert_one(data)

    def run(self):
        loop = asyncio.get_event_loop()
        task = asyncio.wait([self.get_html_info()])
        loop.run_until_complete(task)


if __name__ == '__main__':
    dbm = DouBanMovie()
    dbm.run()

