import json

from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider  # 基于Spider的更强大的类
from scrapy.linkextractors import LinkExtractor

from weibospider.items import WeibospiderItem
import scrapy


class DouBanSpider(scrapy.Spider):
    name = 'weibo'

    # 用户url
    start_urls = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&containerid=100505{uid}'
    start_user_uuid = ['1350995007', '1195354434']

    def start_requests(self):
        for uid in self.start_user_uuid:
            yield Request(url=self.start_urls.format(uid=uid), callback=self.parse)

    def parse(self, response):

        items = WeibospiderItem()
        response = json.loads(response.text)
        user_params = {
            'id': 'id',
            'screen_name': 'screen_name',
            'profile_image_url': 'profile_image_url',
            'profile_url': 'profile_url',
            'verified_reason': 'verified_reason',
            'description': 'description',
            'followers_count': 'followers_count',
            'follow_count': 'follow_count',
            'avatar_hd': 'avatar_hd'
        }
        for k, v in user_params.items():
            items[k] = response['data']['userInfo'][v]

        print(items)

        return items