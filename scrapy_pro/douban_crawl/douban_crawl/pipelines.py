# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings


class DoubanCrawlPipeline(object):

    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'],
                                   )
        db = conn[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        for i in range(len(item['title'])):
            data = dict()
            data['title'] = item['title'][i]
            data['img_src'] = item['img_src'][i]
            data['directors'] = item['directors'][i]
            data['years'] = item['years'][i]
            data['country'] = item['country'][i]
            data['type'] = item['type'][i]
            data['rate'] = item['rate'][i]
            # data['introduce'] = item['introduce'][i]
            self.collection.insert(data)
        return item
