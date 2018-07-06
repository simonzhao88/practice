# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

from lianjia.items import LianjiaItem


class LianjiaPipeline(object):

    def __init__(self):
        self.MONGODB_HOST = settings['MONGODB_HOST']
        self.MONGODB_PORT = settings['MONGODB_PORT']
        self.MONGODB_DB = settings['MONGODB_DB']
        self.COLLECTION = LianjiaItem.Collections

        mongo_client = pymongo.MongoClient(host=self.MONGODB_HOST,
                                           port=self.MONGODB_PORT)
        db = mongo_client[self.MONGODB_DB]
        self.collection = db[self.COLLECTION]

    def process_item(self, item, spider):
        # if isinstance(item, LianjiaItem):
        self.collection.update({'title': item['title']}, {'$set': item}, upsert=True)
        # if isinstance(item, LianjiaInfoItem):
        #     self.collection.update({'title': item['title']},
        #                            {'$addToSet': {
        #                                'house_info': item['house_info'],
        #                                'follow_info': item['follow_info']
        #                            }}, True)
        return item
