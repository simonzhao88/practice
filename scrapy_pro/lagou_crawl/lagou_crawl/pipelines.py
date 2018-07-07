# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

from lagou_crawl.items import LagouCrawlItem, HrInfoItem, JobDetailItem


class LagouCrawlPipeline(object):
    def __init__(self):
        self.coon = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                        port=settings['MONGODB_PORT'])
        self.db = self.coon[settings['MONGODB_DB']]

    def process_item(self, item, spider):

        if isinstance(item, LagouCrawlItem):
            self.collections = self.db[LagouCrawlItem.Collections]
            self.collections.update({'positionId': item['positionId']},
                                    {'$set': item}, upsert=True)

        if isinstance(item, HrInfoItem):
            self.collections = self.db[HrInfoItem.Collections]
            self.collections.update({'positionId': item['positionId']},
                                    {'$set': item}, upsert=True)

        if isinstance(item, JobDetailItem):
            self.collections = self.db[JobDetailItem.Collections]
            self.collections.update({'positionId': item['positionId']},
                                    {'$set': item}, upsert=True)
        return item
