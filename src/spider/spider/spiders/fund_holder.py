#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from spider.items import FundHolderItem

__author__ = 'David Qian'

"""
Created on 06/14/2017
@author: David Qian

"""


class FundHolderSpider(scrapy.Spider):
    name = "fund_holder"
    allowed_domains = ['fund.eastmoney.com']
    start_urls = [
        'http://fund.eastmoney.com/f10/cyrjg_000801.html'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        jjlist = response.xpath("//select[@id='jjlist']/option/@value")
        for jjid in jjlist:
            jjid = jjid.extract()
            yield self._build_fund_holder_request(jjid)

    def _build_fund_holder_request(self, fund_id):
        url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=cyrjg&code=%s' % fund_id
        return SplashRequest(url, self.parse_fund_holder, args={'wait': 0.5}, meta={'fund_id': fund_id})

    def parse_fund_holder(self, response):
        fund_id = response.meta['fund_id']
        holder_list = response.css('.cyrjg').xpath("//table/tbody/tr")
        if not holder_list:
            return None

        fund_holder_list = []
        for h in holder_list:
            keys = ['date', 'org_percent', 'individual_percent', 'inner_percent', 'total_share']
            fields = [field.extract() for field in h.xpath('//td/text()')]
            d = {}
            for f, k in zip(keys, fields):
                d[f] = k
            fund_holder_list.append(d)

        item = FundHolderItem()
        item['fund_id'] = fund_id
        item['fund_holder_list'] = fund_holder_list
        return item
