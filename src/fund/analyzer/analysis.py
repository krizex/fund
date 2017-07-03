#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

from fund.analyzer.model import MLModel
from fund.analyzer.tf.softmax import SoftmaxTrainer

__author__ = 'David Qian'

"""
Created on 07/03/2017
@author: David Qian

"""


def data_file():
    filename = os.path.join(os.path.dirname(__file__), '../../spider/items-2017-07-02-23-18-34.json')
    return filename


def js_data(filename):
    with open(filename) as f:
        data = json.load(f)

    return data


def label_func(label_count):
    step = 1.0 / label_count
    p = step
    ruler = []
    for i in range(label_count):
        ruler.append((i, p))
        p += step

    def _label_func(rank_ratio):
        labels = [0.0] * len(ruler)
        for label, ratio in ruler:
            if rank_ratio <= ratio:
                labels[label] = 1.0
                return labels

        return labels

    return _label_func


def build_model(feature_count, label_count, js_data):
    rank_size = feature_count + 1
    valid_js_data = []
    for d in js_data:
        rank_list = d['fund_rank_list']
        if len(rank_list) < rank_size:
            continue

        # ensure the valid rank data, `x` means the rank ratio, it should <= 1.0
        if any(map(lambda x: x > 1.0, rank_list[:rank_size])):
            continue

        valid_js_data.append(d)

    calc_label = label_func(label_count)

    data = []
    for d in valid_js_data:
        rank_list = d['fund_rank_list']
        features = rank_list[1:1+feature_count]
        label = calc_label(rank_list[0])
        data.append((features, label))

    return MLModel(feature_count, label_count, data)


def train(model, training_ratio, learning_rate, iterate_count):
    t_set, v_set = model.get_training_verify_data_set(training_ratio)
    sm = SoftmaxTrainer(model.feature_count, model.label_count, learning_rate, iterate_count)
    return sm.train(t_set, v_set)


if __name__ == '__main__':
    data = js_data(data_file())
    model = build_model(2, 5, data)
    train(model, 0.8, 0.000000003, 10000)
    # model.print_verbose()
    # learning_rate = 1.0
    # d = []
    # for i in range(20):
    #     accr = train(model, 0.9, learning_rate, 10)
    #     d.append((learning_rate, accr))
    #     learning_rate /= 3
    #
    # d = sorted(d, key=lambda x:x[1])
    # for x in d:
    #     print x

