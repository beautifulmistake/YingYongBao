# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YingyongbaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    # 搜索关键字
    keyword = scrapy.Field()
    # APP名称
    appName = scrapy.Field()
    # 应用信息
    description = scrapy.Field()
    # 上架时间
    appPublishTime = scrapy.Field()
    # 开发商
    authorName = scrapy.Field()
    # 下载量
    appDownCount = scrapy.Field()
    # 图片地址
    iconUrl = scrapy.Field()
    # 详情页的链接
    detail_page_url = scrapy.Field()
    # APP种类
    categoryName = scrapy.Field()
    # APP大小
    fileSize = scrapy.Field()
    # 版本号
    versionName = scrapy.Field()
    # 评分
    averageRating = scrapy.Field()
    # APP评论数
    commentNum = scrapy.Field()










