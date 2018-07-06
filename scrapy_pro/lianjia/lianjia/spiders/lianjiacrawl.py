# -*- coding: utf-8 -*-
import json

import scrapy

from lianjia.items import LianjiaItem
from scrapy import Request
from scrapy_redis.spiders import RedisSpider


class LianjiacrawlSpider(RedisSpider):
    name = 'lianjiacrawl'

    allowed_domains = ['cd.lianjia.com']
    # 新盘
    # start_urls = 'https://cd.fang.lianjia.com/loupan/pg{page}'

    domains_url = 'https://cd.lianjia.com'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0'

    headers = {'User-Agent': user_agent}

    # def start_requests(self):
    #      新房获取100页数据
    #     for i in range(1, 101):
    #         yield Request(self.start_urls.format(page=i), headers=self.headers,
    #                       callback=self.parse)

    # def parse(self, response):
    #
    #     return item

    # 二手房
    start_urls = 'https://cd.lianjia.com/ershoufang'

    def start_requests(self):

        yield Request(self.start_urls, headers=self.headers, callback=self.get_area_url)

    def get_area_url(self, response):
        areas_link = response.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a')
        for area in areas_link:
            area_href = area.xpath('./@href').extract()[0]
            area_name = area.xpath('./text()').extract()[0]

            yield Request(self.domains_url + area_href, headers=self.headers,
                          callback=self.get_page, meta={'area': area_name, 'href': area_href})

    def get_page(self, response):
        page_box = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        page_num = json.loads(page_box[0]).get('totalPage')

        for i in range(1, page_num + 1):
            yield Request(self.domains_url + response.meta.get('href') + 'pg' + str(i),
                          headers=self.headers, meta={'name': response.meta.get('area')},
                          callback=self.get_house_info)

    def get_house_info(self, response):
        house_list = response.xpath('/html/body/div[4]/div[1]/ul/li')
        for house in house_list:
            try:
                items = LianjiaItem()
                # 数量
                items['house_amount'] = response.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()').extract()[0]
                # 房屋名   西雅苑标准套二，中楼层，安静不临街
                items['title'] = house.xpath('div[1]/div[1]/a/text()').extract()[0]
                # 街道/位置  较场坝东街67号
                items['street'] = house.xpath('div[1]/div[2]/div/a/text()').extract()[0]
                # 总价
                items['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').extract()[0]
                # 单价
                items['unit_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').extract()[0]
                # 房屋信息    | 2室1厅 | 54.25平米 | 北 东北 | 精装 | 无电梯
                house_info = house.xpath('div[1]/div[2]/div/text()').extract()[0]
                # 楼层信息  高楼层(共7层)板楼
                items['floor'] = house.xpath('div[1]/div[3]/div/text()').extract()[0]
                # 商圈  合江亭
                items['local'] = house.xpath('div[1]/div[3]/div/a/text()').extract()[0]
                # 关注信息   237人关注 / 共37次带看 / 1个月以前发布
                follow_info = house.xpath('div[1]/div[4]/text()').extract()[0]
                # 房屋类型
                items['type'] = '二手房'
                items['area'] = response.meta.get('name')

                huxing = house_info.split('|')[1]
                mianji = house_info.split('|')[2]
                info = house_info.split('|')[3:]
                house_infos = {'huxing': huxing, 'mianji': mianji, 'info': info}

                follow_num = follow_info.split('/')[0]
                publish_time = follow_info.split('/')[-1]
                follow_infos = {'follow_num': follow_num, 'publish_time': publish_time}

                items['house_info'] = house_infos
                items['follow_info'] = follow_infos

                # infos = LianjiaInfoItem()
                # infos['title'] = items['title']
                # infos['house_info'] = house_infos
                # infos['follow_info'] = follow_infos
                yield items

                # yield infos
            except Exception:
                pass

