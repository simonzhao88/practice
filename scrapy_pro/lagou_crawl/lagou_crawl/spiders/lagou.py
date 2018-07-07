import json

import scrapy
from scrapy import Request

from lagou_crawl.items import LagouCrawlItem, HrInfoItem, JobDetailItem


class LaGouSpider(scrapy.Spider):
    name = 'lagou'

    interf_urls = 'https://www.lagou.com/jobs/positionAjax.json?' \
                  'px=default&city=成都&district={area}&needAddtionalResult=false'

    # start_url = 'https://www.lagou.com/jobs/list_?px=new&city=成都&district={area}#filterBox'

    areas = ['高新区', '武侯区', '锦江区', '青羊区', '金牛区', '成华区', '郫县', '双流区',
             '双流县', '龙泉驿区', '新都区', '温江区', '崇州市', '青白江区', '都江堰市',
             '大邑县', '新津县', '邛崃市', '彭州市', '蒲江县']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36',

    }
    referer = 'https://www.lagou.com/jobs/list_python?city=成都BD' \
              '&district={area}&cl=false&fromSearch=true&labelWords=&suginput='

    job_link = 'https://www.lagou.com/jobs/{positionId}.html'

    def start_requests(self):
        for area in self.areas:
            self.headers['Referer'] = self.referer.format(area=area)
            yield scrapy.FormRequest(self.interf_urls.format(area=area), headers=self.headers,
                                     meta={'area': area}, callback=self.get_page_size)

    def get_page_size(self, response):
        page_size = json.loads(response.text).get('content').get('pageSize')
        self.headers['Referer'] = self.referer.format(area=response.meta['area'])
        for pn in range(1, page_size + 1):
            yield scrapy.FormRequest(self.interf_urls.format(area=response.meta['area']),
                                     headers=self.headers,
                                     formdata={'pn': str(pn)},
                                     callback=self.get_data)

    def get_data(self, response):
        result_json = json.loads(response.text)

        hrs_data = result_json.get('content').get('hrInfoMap')

        jobs_data = result_json.get('content').get('positionResult').get('result')

        jobs_items = LagouCrawlItem()
        hrs_items = HrInfoItem()
        for job_data in jobs_data:
            positionId = job_data.get('positionId')
            hr_data = hrs_data.get(str(positionId))
            hr_data['positionId'] = positionId
            for i in job_data.keys():
                jobs_items[i] = job_data[i]
            for j in hr_data.keys():
                hrs_items[j] = hr_data[j]
            yield jobs_items
            yield hrs_items
            self.headers['Referer'] = self.job_link.format(positionId=positionId)
            yield Request(self.job_link.format(positionId=positionId), headers=self.headers,
                          meta={'id': positionId}, callback=self.get_job_detail)

    def get_job_detail(self, response):
        items = JobDetailItem()
        items['positionId'] = response.meta['id']
        items['positionName'] = response.xpath('/html/body/div[2]/div/div[1]/div/span/text()').extract()[0]
        items['salary'] = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()').extract()[0]
        items['city'] = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()').extract()[0]
        items['workYear'] = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()').extract()[0]
        items['education'] = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()').extract()[0]
        items['jobNature'] = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()').extract()[0]
        items['formatCreateTime'] = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()').extract()[0]
        items['positionAdvantage'] = response.xpath('//*[@id="job_detail"]/dd[1]/p/text()').extract()[0]
        items['jobRequire'] = response.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()').extract()
        items['address'] = response.xpath('//*[@id="job_detail"]/dd[3]/div[1]/text()').extract()[0]

        yield items
