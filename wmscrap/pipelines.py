# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from time import time

import redis
from scrapy import signals
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class JsonExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CsvExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class RedisExportPipeline(object):

    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost')
        self.start_time = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def dict_to_redis_hset(self, hkey, dict_to_store):
        """Store dict on redis hset"""
        return all([
            self.redis.hset(hkey, k, v) for k, v in dict_to_store.items()])

    def spider_opened(self, spider):
        start = datetime.now().isoformat(' ')
        self.start_time = time()
        print("Start spider {} at {}".format(spider.name, start))
        # self.exporter.start_exporting()

    def spider_closed(self, spider):
        end = datetime.now().isoformat(' ')
        print("Finish spider {} at {}".format(spider.name, end))
        print("Elapsed time {}".format(time() - self.start_time))
        # self.exporter.finish_exporting()

    def process_item(self, item, spider):
        hkey = (
            u"{}-{}".format(
                item['model'],
                item['brand'])
        )
        self.dict_to_redis_hset(hkey, item)
        return item
