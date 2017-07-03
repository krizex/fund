#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from fund.log.logger import log

__author__ = 'David Qian'

"""
Created on 07/03/2017
@author: David Qian

"""


class MLModel(object):
    def __init__(self, feature_count, label_count, data):
        self.feature_count = feature_count
        self.label_count = label_count
        self.data = data

    def get_training_verify_data_set(self, training_ratio):
        random.shuffle(self.data)
        if not 0 < training_ratio < 1:
            return None

        p = int(len(self.data) * training_ratio)
        return self.data[:p], self.data[p:]

    def print_verbose(self):
        log.debug('feature_count: %d' % self.feature_count)
        log.debug('label_count: %d' % self.label_count)
        for features, labels in self.data:
            log.debug('features: %s' % ','.join(['%f' % x for x in features]))
            log.debug('labels: %s' % ','.join(['%f' % x for x in labels]))