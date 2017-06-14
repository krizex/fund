# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundHolderItem(scrapy.Item):
    date = scrapy.Field()
    org_percent = scrapy.Field()
    individual_percent = scrapy.Field()
    inner_percent = scrapy.Field()
    total_share = scrapy.Field()
