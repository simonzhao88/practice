# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    img_src = scrapy.Field()
    directors = scrapy.Field()
    years = scrapy.Field()
    country = scrapy.Field()
    type = scrapy.Field()
    rate = scrapy.Field()
    # introduce = scrapy.Field()
