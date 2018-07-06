# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingCrawlItem(scrapy.Item):
    Collections = 'dianping'
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    star_level = scrapy.Field()
    consumption_per = scrapy.Field()
    taste_rate = scrapy.Field()
    environment_rate = scrapy.Field()
    server_rate = scrapy.Field()
    cook_style = scrapy.Field()
    min_buss_area = scrapy.Field()
    local = scrapy.Field()
    recom_foods = scrapy.Field()
    link = scrapy.Field()
    where_from = scrapy.Field()
    type = scrapy.Field()
    tag = scrapy.Field()
    buss_area = scrapy.Field()
