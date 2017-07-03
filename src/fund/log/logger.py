#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from logging.handlers import RotatingFileHandler

from fund import config

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


class Logger(object):
    def __init__(self):
        logging.getLogger().setLevel(config.logger['level'])
        self.logger = logging.getLogger('scv')
        self.logger.setLevel(config.logger['level'])
        log_file_dir = config.logger['path']
        if not os.path.exists(log_file_dir):
            os.mkdir(log_file_dir)

        formatter = logging.Formatter("[%(asctime)s] - %(name)-20s - %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")

        handler = RotatingFileHandler(
            os.path.join(log_file_dir, config.logger['file']))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        term_handler = logging.StreamHandler()
        term_handler.setFormatter(formatter)
        self.logger.addHandler(term_handler)


log = Logger().logger
