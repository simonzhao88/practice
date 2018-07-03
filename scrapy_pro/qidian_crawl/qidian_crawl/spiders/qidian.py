

import scrapy


class QiDianSpider(scrapy.Spider):

    # 启动项目指定的name参数
    name = 'qidian'

    # 需要爬去的页面
    start_urls = [
        'https://www.qidian.com/'
    ]

    def parse(self, response):
        tags = response.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()
        url = response.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        print(tags, url)
        return response
