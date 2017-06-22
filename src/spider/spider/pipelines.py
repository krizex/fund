# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import time


class WriteFilePipeline(object):
    def open_spider(self, spider):
        self.items = {}
        self.file = open('items-%s.json' % self._current_time_stamp(), 'w')

    def _current_time_stamp(self):
        now = int(time.time())
        timeArray = time.localtime(now)
        time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
        return time_stamp

    def close_spider(self, spider):
        l = [v for v in self.items.itervalues()]
        json.dump(l, self.file)
        self.file.close()

    def process_item(self, item, spider):
        fund_id = item['fund_id']
        if fund_id not in self.items:
            self.items[fund_id] = dict(item)
        else:
            self.items[fund_id].update(dict(item))

        return item

