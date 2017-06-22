# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundHolderItem(scrapy.Item):
    fund_id = scrapy.Field()
    fund_holder_list = scrapy.Field()
    # date = scrapy.Field()
    # org_percent = scrapy.Field()
    # individual_percent = scrapy.Field()
    # inner_percent = scrapy.Field()
    # total_share = scrapy.Field()


class FundRankItem(scrapy.Item):
    fund_id = scrapy.Field()
    fund_rank_list = scrapy.Field()


class FuncInfoItem(scrapy.Item):
    fund_id = scrapy.Field()
    fund_name = scrapy.Field()
    fund_url = scrapy.Field()
