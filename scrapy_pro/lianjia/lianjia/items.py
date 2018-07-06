# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Collections = 'lianjia'
    house_amount = scrapy.Field()
    title = scrapy.Field()
    street = scrapy.Field()
    floor = scrapy.Field()
    local = scrapy.Field()
    type = scrapy.Field()
    house_info = scrapy.Field()
    follow_info = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    area = scrapy.Field()


# class LianjiaInfoItem(scrapy.Item):
#     title = scrapy.Field()
#     house_info = scrapy.Field()
#     follow_info = scrapy.Field()
