# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Collections = 'lagou_jobs'
    companyId = scrapy.Field()
    positionName = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    jobNature = scrapy.Field()
    companyLogo = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    financeStage = scrapy.Field()
    industryField = scrapy.Field()
    positionId = scrapy.Field()
    approve = scrapy.Field()
    createTime = scrapy.Field()
    positionAdvantage = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    companyLabelList = scrapy.Field()
    publisherId = scrapy.Field()
    score = scrapy.Field()
    district = scrapy.Field()
    positionLables = scrapy.Field()
    industryLables = scrapy.Field()
    businessZones = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    adWord = scrapy.Field()
    resumeProcessRate = scrapy.Field()
    resumeProcessDay = scrapy.Field()
    companyFullName = scrapy.Field()
    imState = scrapy.Field()
    lastLogin = scrapy.Field()
    explain = scrapy.Field()
    plus = scrapy.Field()
    pcShow = scrapy.Field()
    appShow = scrapy.Field()
    deliver = scrapy.Field()
    gradeDescription = scrapy.Field()
    promotionScoreExplain = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    isSchoolJob = scrapy.Field()
    subwayline = scrapy.Field()
    stationname = scrapy.Field()
    linestaion = scrapy.Field()
    hitags = scrapy.Field()
    formatCreateTime = scrapy.Field()


class HrInfoItem(scrapy.Item):
    Collections = 'lagou_hr'
    positionId = scrapy.Field()
    userId = scrapy.Field()
    userLevel = scrapy.Field()
    positionName = scrapy.Field()
    receiveEmail = scrapy.Field()
    phone = scrapy.Field()
    realName = scrapy.Field()
    portrait = scrapy.Field()
    canTalk = scrapy.Field()


class JobDetailItem(scrapy.Item):
    Collections = 'lagou_job_detail'
    positionId = scrapy.Field()
    positionName = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    jobNature = scrapy.Field()
    formatCreateTime = scrapy.Field()
    positionAdvantage = scrapy.Field()
    jobRequire = scrapy.Field()
    address = scrapy.Field()
