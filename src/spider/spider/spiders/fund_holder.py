#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy_splash import SplashRequest

from spider.items import FundHolderItem, FundRankItem, FuncInfoItem, FundStageRankItem

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

    def init(self):
        self.fund_cnt = 0
        self.cur_index = 1

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        self.init()
        fund_list = response.xpath("//select[@id='jjlist']/option/@value")
        self.fund_cnt = len(fund_list)
        for fund_id in fund_list:
            fund_id = fund_id.extract()
            yield self._build_fund_holder_request(fund_id)
            yield self._build_fund_rank_request(fund_id)
            yield self._build_fund_info_request(fund_id)
            yield self._build_fund_stage_increase_rank_request(fund_id)

    def _build_fund_holder_request(self, fund_id):
        url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=cyrjg&code=%s' % fund_id
        return SplashRequest(url, self.parse_fund_holder, meta={'fund_id': fund_id})

    def _build_fund_rank_request(self, fund_id):
        url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=quarterzf&code=%s' % fund_id
        return SplashRequest(url, self.parse_fund_rank, meta={'fund_id': fund_id})

    def _build_fund_info_request(self, fund_id):
        url = 'http://fund.eastmoney.com/%s.html' % fund_id
        return SplashRequest(url, self.parse_fund_info, meta={'fund_id': fund_id})

    def _build_fund_stage_increase_rank_request(self, fund_id):
        url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jdzf&code=%s' % fund_id
        return SplashRequest(url, self.parse_stage_increase_rank, meta={'fund_id': fund_id})

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

    def parse_stage_increase_rank(self, response):
        fund_id = response.meta['fund_id']
        fund_rank_list = []
        try:
            rank_list = response.css('.jdzfnew').xpath("./ul")
            last_week = rank_list[2]
            last_month = rank_list[3]
            for x in (last_week, last_month):
                fund_rank_list.append(self._calc_stage_rank_rate(x))
        except:
            pass

        item = FundStageRankItem()
        item['fund_id'] = fund_id
        item['fund_stage_rank_list'] = fund_rank_list
        return item

    def _calc_stage_rank_rate(self, rank):
        try:
            rank = rank.xpath('./li')[4].extract()
            m = re.match(r'<li.+>(\d+)<font.+/font>(\d+)</li>', rank)
            idx, total = m.groups()
            idx = float(idx)
            total = float(total)
            return 1.0 * idx / total
        except:
            return 100.0

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
        self.logger.info("%d/%d: %s" % (self.cur_index, self.fund_cnt, fund_id))
        self.cur_index += 1
        title = response.xpath('/html/head/title/text()')[0]
        fund_name = title.extract().split('(')[0]

        item = FuncInfoItem()
        item['fund_id'] = fund_id
        item['fund_name'] = fund_name
        item['fund_url'] = 'http://fund.eastmoney.com/%s.html' % fund_id
        return item


