# -*- coding: utf-8 -*-
import scrapy


class WebmotorsSpider(scrapy.Spider):
    name = "webmotors"
    allowed_domains = ["webmotors.com.br"]
    start_urls = (
        'http://www.webmotors.com.br/',
    )

    def parse(self, response):
        pass
