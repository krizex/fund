#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

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
        jjlist = response.xpath("//select[@id='jjlist']")
        print jjlist.extract()
