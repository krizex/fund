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

    def rank_rate_per_season_gen(self, num, season_cnt):
        for i in range(num):
            rec = self._ranked_js[i]
            rank_rate_per_season = ['%3.1f%%' % (rank_rate * 100) for rank_rate in rec['fund_rank_list'][:season_cnt]]
            yield ', '.join(rank_rate_per_season)

    def latest_month_rank_rate_gen(self, num):
        for i in range(num):
            rec = self._ranked_js[i]
            yield '%3.1f%%' % (rec['fund_stage_rank_list'][1] * 100)

    def print_fund_rank_with_generator(self, num, *gens):
        for i in range(num):
            idx = i + 1
            rec = self._ranked_js[i]
            fund_id = rec['fund_id']
            fund_name = rec['fund_name']
            s = ', '.join(map(lambda x: x.next(), gens))
            print "%2d => %s -- %s -- %s" % (idx, fund_id, fund_name, s)

    def print_fund_rank(self, num, season_cnt):
        self.print_fund_rank_with_generator(num,
                                            self.rank_rate_per_season_gen(num, season_cnt))

    def print_fund_rank_with_latest_month(self, num, season_cnt):
        self.print_fund_rank_with_generator(num,
                                            self.latest_month_rank_rate_gen(num),
                                            self.rank_rate_per_season_gen(num, season_cnt))

    def total_performance_by_season(self, season_cnt, skip_season_cnt=0):
        return lambda rec: sum(rec['fund_rank_list'][skip_season_cnt:skip_season_cnt+season_cnt])


class FundRankByPerformance(FundRankBase):
    def __init__(self, fund_file, season_cnt):
        super(FundRankByPerformance, self).__init__(fund_file)
        self.season_cnt = season_cnt

    def prepare_rank_list(self):
        self._ranked_js = filter(lambda rec: self.rank_list_len(rec) >= self.season_cnt, self._ranked_js)

    def rank(self):
        self.prepare_rank_list()
        self._ranked_js = sorted(self._ranked_js, key=self.total_performance_by_season(self.season_cnt), reverse=False)


class FundRankByPastIncrease(FundRankBase):
    def __init__(self, fund_file, season_cnt, skip_season_cnt):
        super(FundRankByPastIncrease, self).__init__(fund_file)
        self.season_cnt = season_cnt
        self.skip_season_cnt = skip_season_cnt

    def prepare_rank_list(self):
        self._ranked_js = filter(lambda rec: self.rank_list_len(rec) >= (self.skip_season_cnt + self.season_cnt), self._ranked_js)
        self._ranked_js = filter(self.rank_should_increase, self._ranked_js)

    def rank(self):
        self.prepare_rank_list()
        self._ranked_js = sorted(self._ranked_js, key=self.total_performance_by_season(self.season_cnt, self.skip_season_cnt), reverse=False)

    def rank_should_increase(self, rec):
        rank_list = rec['fund_rank_list']
        for i in range(self.skip_season_cnt, self.skip_season_cnt + self.season_cnt - 1):
            if rank_list[i] > rank_list[i+1]:
                return False

        return True


class FundRankByLatestIncrease(FundRankByPastIncrease):
    def __init__(self, fund_file, season_cnt):
        super(FundRankByLatestIncrease, self).__init__(fund_file, season_cnt, 0)


class FundRankByStageIncreaseAndSeason(FundRankByPerformance):
    def rank(self):
        self.prepare_rank_list()
        self._ranked_js = sorted(self._ranked_js, key=self.performance_with_latest_month, reverse=False)

    def performance_with_latest_month(self, rec):
        return self.total_performance_by_season(self.season_cnt, 0)(rec) + rec['fund_stage_rank_list'][1] / 3

    def prepare_rank_list(self):
        super(FundRankByStageIncreaseAndSeason, self).prepare_rank_list()
        self._ranked_js = filter(lambda rec: len(rec['fund_stage_rank_list']) > 1, self._ranked_js)


def rank_by_latest(file, season_cnt):
    print_fund_cnt = 100
    ranker = FundRankByLatestIncrease(file, season_cnt)
    ranker.rank()
    ranker.print_fund_rank(print_fund_cnt, season_cnt)


def rank_by_past(file, season_cnt, skip_season_cnt):
    print_fund_cnt = 100
    ranker = FundRankByPastIncrease(file, season_cnt, skip_season_cnt)
    ranker.rank()
    ranker.print_fund_rank(print_fund_cnt, season_cnt + skip_season_cnt)


def rank_by_stage_increase_and_past(file, season_cnt):
    print_fund_cnt = 100
    ranker = FundRankByStageIncreaseAndSeason(file, season_cnt)
    ranker.rank()
    ranker.print_fund_rank_with_latest_month(print_fund_cnt, season_cnt)

def main():
    file = '/home/qy/dev/fund/src/spider/items-2017-10-23-21-52-33.json'
    rank_by_stage_increase_and_past(file, 2)


if __name__ == '__main__':
    main()

