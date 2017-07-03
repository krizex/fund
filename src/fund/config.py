#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


root_node = {
    'path': os.path.join(os.path.dirname(__file__), 'running')
}

data_node = {
    'path': os.path.join(root_node['path'], 'data')
}

file_store = {
    'path': os.path.join(data_node['path'], 'images')
}

scanner = {
    'interval': 24 * 3600
}

logger = {
    'path': os.path.join(root_node['path'], 'logs'),
    'file': 'fund.log',
    'level': logging.DEBUG,
}
