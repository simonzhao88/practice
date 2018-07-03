import scrapy

from douban_crawl.items import DoubanCrawlItem
from scrapy.spiders import Rule, CrawlSpider  # 基于Spider的更强大的类
from scrapy.linkextractors import LinkExtractor


class DouBanSpider(CrawlSpider):
    name = 'douban'

    start_urls = [
        'https://movie.douban.com/top250',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'https://movie.douban.com/top250*'), callback='get_movies'),
    )

    # def parse(self, response):
    #     page_urls = response.xpath('//*[@id="content"]/div/div[1]/div[2]/a/@href').extract()
    #     page_urls.append('')
    #     for page_url in page_urls:
    #         page_url = 'https://movie.douban.com/top250' + page_url
    #         yield scrapy.Request(page_url, callback=self.get_movies)

    def get_movies(self, response):
        items = DoubanCrawlItem()
        # 电影名
        items['title'] = response.xpath(
            '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()
        # 图片
        items['img_src'] = response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()
        # 导演和主演
        directors = response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').extract()
        items['directors'] = [director.strip().replace('\xa0', ' ') for director in directors]
        # 年份、国家和分类
        years_info = response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').extract()
        years_info = [info.strip().replace('\xa0', ' ') for info in years_info]
        items['years'], items['country'], items['type'] = [], [], []
        for info in years_info:
            items['years'].append(info.split('/')[0])
            items['country'].append(info.split('/')[1])
            items['type'].append(info.split('/')[2])

        # 评分
        items['rate'] = response.xpath(
            '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()').extract()
        # 简介
        # items['introduce'] =
        # response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[2]/span/text()').extract()
        return items
