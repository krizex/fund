#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy_splash import SplashRequest

from spider.items import FundHolderItem, FundRankItem, FuncInfoItem

__author__ = 'David Qian'

"""
Created on 06/14/2017
@author: David Qian

"""


class FundSpider(scrapy.Spider):
    name = "fund_spider"
    allowed_domains = ['fund.eastmoney.com']
    start_urls = [
        'http://fund.eastmoney.com/f10/cyrjg_000801.html'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        fund_list = response.xpath("//select[@id='jjlist']/option/@value")
        for fund_id in fund_list:
            fund_id = fund_id.extract()
            yield self._build_fund_holder_request(fund_id)
            yield self._build_fund_rank_request(fund_id)
            yield self._build_fund_info(fund_id)

    def _build_fund_holder_request(self, fund_id):
        url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=cyrjg&code=%s' % fund_id
        return SplashRequest(url, self.parse_fund_holder, args={'wait': 0.5}, meta={'fund_id': fund_id})

    def _build_fund_rank_request(self, fund_id):
        url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=quarterzf&code=%s' % fund_id
        return SplashRequest(url, self.parse_fund_rank, args={'wait': 0.5}, meta={'fund_id': fund_id})

    def _build_fund_info(self, fund_id):
        url = 'http://fund.eastmoney.com/%s.html' % fund_id
        return SplashRequest(url, self.parse_fund_info, args={'wait': 0.5}, meta={'fund_id': fund_id})

    def parse_fund_holder(self, response):
        fund_id = response.meta['fund_id']
        holder_list = response.css('.cyrjg').xpath("//table/tbody/tr")
        if not holder_list:
            return None

        fund_holder_list = []
        for h in holder_list:
            keys = ['date', 'org_percent', 'individual_percent', 'inner_percent', 'total_share']
            fields = [field.extract() for field in h.xpath('./td/text()')]
            d = {}
            for f, k in zip(keys, fields):
                d[f] = k
            fund_holder_list.append(d)

        item = FundHolderItem()
        item['fund_id'] = fund_id
        item['fund_holder_list'] = fund_holder_list
        return item

    def parse_fund_rank(self, response):
        fund_id = response.meta['fund_id']
        fund_rank_list = []
        try:
            rank_list = response.css('.jndxq').xpath("./tbody/tr")[3]
            ranks = rank_list.xpath('./td')[1:]
            for rank in ranks:
                fund_rank_list.append(self._calc_rank_rate(rank))
        except:
            pass

        item = FundRankItem()
        item['fund_id'] = fund_id
        item['fund_rank_list'] = fund_rank_list
        return item

    def _calc_rank_rate(self, rank):
        try:
            rank = rank.extract()
            m = re.match(r'<td>(\d+)<span.+/span>(\d+)</td>', rank)
            idx, total = m.groups()
            idx = float(idx)
            total = float(total)
            return 1.0 * idx / total
        except:
            return 100.0

    def parse_fund_info(self, response):
        fund_id = response.meta['fund_id']
        title = response.xpath('/html/head/title/text()')[0]
        fund_name = title.extract().split('(')[0]

        item = FuncInfoItem()
        item['fund_id'] = fund_id
        item['fund_name'] = fund_name
        item['fund_url'] = 'http://fund.eastmoney.com/%s.html' % fund_id
        return item


