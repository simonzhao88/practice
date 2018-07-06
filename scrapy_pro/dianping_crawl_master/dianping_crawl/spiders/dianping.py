

import scrapy
from scrapy import Request

from dianping_crawl.items import DianpingCrawlItem


class DianPingSpider(scrapy.Spider):

    name = 'dianping'

    start_urls = 'http://www.dianping.com/chengdu/ch10/g0r0'

    allow_domains = ['http://www.dianping.com']

    # page_url = 'http://www.dianping.com/chengdu/ch10/p{page}'

    headers = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               # 'Cookie': 'navCtgScroll=0; _hc.v="\"efde118c-7f60-4fb1-b3db-5782c262af02.1530783906\""; '
               #           'cy=8; cye=chengdu; _lxsdk_cuid=16469d63e4cc8-0cba818f4e73f1-393d5f0e-fa000-16469d63e4dc8; '
               #           '_lxsdk=16469d63e4cc8-0cba818f4e73f1-393d5f0e-fa000-16469d63e4dc8; s_ViewType=10; '
               #           '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=1646a284af6-e7-ed1-18b%7C%7C88',
               'Host': 'www.dianping.com',
               'Accept-Encoding': 'gzip, deflate',
               'Referer': 'http://www.dianping.com/chengdu/ch10/g0r0'}

    def start_requests(self):

        yield Request(self.start_urls,
                      headers=self.headers, callback=self.parse)

    def parse(self, response):
        """
        获取分类地址
        :param response:
        :return:
        """
        type_links = response.xpath('//*[@id="classfy"]/a/@href').extract()

        for link in type_links:
            yield Request(link, callback=self.get_tag_link)

    def get_tag_link(self, response):
        """
        获取标签地址
        :param response:
        :return:
        """
        tag_links = response.xpath('//*[@id="classfy-sub"]/a/@href').extract()[1:]
        for tag_link in tag_links:
            yield Request(tag_link, callback=self.get_bussi_area)

    def get_bussi_area(self, response):
        """
        获取商圈地址
        :param response:
        :return:
        """
        buss_area_links = response.xpath('//*[@id="bussi-nav"]/a/@href').extract()
        for buss_area_link in buss_area_links:
            yield Request(buss_area_link, meta={'link': buss_area_link}, callback=self.get_page_link)

    def get_page_link(self, response):
        """
        获取分页地址
        :param response:
        :return:
        """
        page_num = response.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/a/text()').extract()
        if not page_num:
            # 如果没有渠道页码，则无分页，直接返回
            items = DianpingCrawlItem()
            items['url'] = response.meta.get('link')

            return items
        else:
            page_num = int(page_num[-2])
            for i in range(1, page_num+1):
                items = DianpingCrawlItem()
                items['url'] = response.meta.get('link') + 'p' + str(i)

                yield items
