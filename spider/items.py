# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:

    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 时间
    time = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 人名
    name = scrapy.Field()
    # 头像
    icon_url = scrapy.Field()
    # 图片地址
    icon_path = scrapy.Field()
    # 目标地址
    target_url = scrapy.Field()
    # 状态
    status = scrapy.Field()
