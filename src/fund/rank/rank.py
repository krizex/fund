#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'David Qian'

"""
Created on 07/05/2017
@author: David Qian

"""

import json


class FundRankBase(object):
    def __init__(self, fund_file):
        self.fund_file = fund_file
        self._data_js = self._load(fund_file)
        self._ranked_js = self._data_js

    def _load(self, file):
        with open(file) as f:
            return json.load(f)

    def rank_list_len(self, rec):
        return len(rec['fund_rank_list'])

    def print_fund_holder(self, num):
        for i in range(1, num + 1):
            rec = self._ranked_js[i]
            fund_id = rec['fund_id']
            fund_name = rec['fund_name']
            fund_hold_org_percent = rec['fund_holder_list'][0]['org_percent']
            fund_hold_individual_percent = rec['fund_holder_list'][0]['individual_percent']
            fund_hold_inner_percent = rec['fund_holder_list'][0]['inner_percent']
            print "%2d => %s -- %s -- org: %s, individual: %s, inner: %s" % \
                  (i, fund_id, fund_name, fund_hold_org_percent,
                   fund_hold_individual_percent, fund_hold_inner_percent)

    def print_fund_rank(self, num, season_cnt):
        for i in range(1, num + 1):
            rec = self._ranked_js[i]
            fund_id = rec['fund_id']
            fund_name = rec['fund_name']
            rank_rate_per_season = ['%3.1f%%' % (rank_rate*100) for rank_rate in rec['fund_rank_list'][:season_cnt]]
            print "%2d => %s -- %s -- %s" % (i, fund_id, fund_name, ', '.join(rank_rate_per_season))

    def total_performance(self, season_cnt):
        return lambda rec: sum(rec['fund_rank_list'][:season_cnt])


class FundRankByPerformance(FundRankBase):
    def rank(self, season_cnt):
        self._ranked_js = filter(lambda rec: self.rank_list_len(rec) >= season_cnt, self._ranked_js)
        self._ranked_js = sorted(self._ranked_js, key=self.total_performance(season_cnt), reverse=False)


class FundRankByIncrease(FundRankBase):
    def rank(self, season_cnt):
        self._ranked_js = filter(lambda rec: self.rank_list_len(rec) >= season_cnt, self._ranked_js)
        self._ranked_js = filter(self.rank_increase(season_cnt), self._ranked_js)
        self._ranked_js = sorted(self._ranked_js, key=self.total_performance(season_cnt), reverse=False)

    def rank_increase(self, season_cnt):
        def _inner(rec):
            rank_list = rec['fund_rank_list']
            for i in range(season_cnt - 1):
                if rank_list[i] > rank_list[i+1]:
                    return False

            return True

        return _inner


if __name__ == '__main__':
    file = '/home/qy/dev/fund/src/spider/items-2017-07-02-23-18-34.json'
    rank = FundRankByIncrease(file)
    rank.rank(4)
    rank.print_fund_rank(100, 4)

