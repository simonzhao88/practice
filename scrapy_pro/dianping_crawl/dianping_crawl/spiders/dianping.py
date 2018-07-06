

import scrapy
from scrapy import Request

from dianping_crawl.items import DianpingCrawlItem
from scrapy_redis.spiders import RedisSpider


class DianPingSpider(RedisSpider):

    name = 'dianping'

    redis_key = 'dianping:start_urls'
    allow_domains = ['http://www.dianping.com']

    headers = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Host': 'www.dianping.com',
               'Accept-Encoding': 'gzip, deflate',
               'Referer': 'http://www.dianping.com/chengdu/ch10/g0r0'}

    def parse(self, response):
        """
        获取商家数据
        :param response:
        :return:
        """
        store_list = response.xpath('//*[@id="shop-all-list"]/ul/li')

        for store in store_list:
            items = DianpingCrawlItem()
            # 图片
            items['img'] = store.xpath('div[1]/a/img/@src').extract()[0]
            # 店名
            items['title'] = store.xpath('div[2]/div[1]/a[1]/h4/text()').extract()[0]
            # 星级
            items['star_level'] = store.xpath('div[2]/div[2]/span/@title').extract()[0]
            # 人均消费
            if store.xpath('div[2]/div[2]/a[2]/b/text()').extract():
                items['consumption_per'] = store.xpath('div[2]/div[2]/a[2]/b/text()').extract()[0]
            else:
                items['consumption_per'] = 'null'
            # 口味评分
            if store.xpath('div[2]/span/span[1]/b/text()').extract():
                items['taste_rate'] = store.xpath('div[2]/span/span[1]/b/text()').extract()[0]
            else:
                items['taste_rate'] = 'null'
            # 环境评分
            if store.xpath('div[2]/span/span[2]/b/text()').extract():
                items['environment_rate'] = store.xpath('div[2]/span/span[2]/b/text()').extract()[0]
            else:
                items['environment_rate'] = 'null'
            # 服务评分
            if store.xpath('div[2]/span/span[3]/b/text()').extract():
                items['server_rate'] = store.xpath('div[2]/span/span[3]/b/text()').extract()[0]
            else:
                items['server_rate'] = 'null'
            # 菜系
            if store.xpath('div[2]/div[3]/a[1]/span/text()').extract():
                items['cook_style'] = store.xpath('div[2]/div[3]/a[1]/span/text()').extract()[0]
            else:
                items['cook_style'] = 'null'
            # 商圈
            if store.xpath('div[2]/div[3]/a[2]/span/text()').extract():
                items['min_buss_area'] = store.xpath('div[2]/div[3]/a[2]/span/text()').extract()[0]
            # 位置
            if store.xpath('div[2]/div[3]/span/text()').extract():
                items['local'] = store.xpath('div[2]/div[3]/span/text()').extract()[0]
            else:
                items['local'] = 'null'
            # 推荐菜 []
            items['recom_foods'] = store.xpath('div[2]/div[4]/a/text()').extract()
            # 详情页面
            items['link'] = store.xpath('div[2]/div[1]/a[1]/@href').extract()[0]
            # id
            items['id'] = items['link'].split('/')[-1]
            # 来自于
            items['where_from'] = '大众点评'
            # 分类
            items['type'] = response.xpath('/html/body/div[2]/div[1]/span[3]/a/span/text()').extract()[0]
            # 标签
            items['tag'] = response.xpath('/html/body/div[2]/div[1]/span[5]/a/span/text()').extract()[0]
            # 商圈
            items['buss_area'] = response.xpath('/html/body/div[2]/div[1]/span[9]/a/span/text()').extract()[0]
            yield items
