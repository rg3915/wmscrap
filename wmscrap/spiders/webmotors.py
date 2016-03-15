# -*- coding: utf-8 -*-
import scrapy
from wmscrap.items import CarItem


class WebmotorsSpider(scrapy.Spider):
    name = "webmotors"
    allowed_domains = ["webmotors.com.br"]
    first_page_url = (
        'http://www.webmotors.com.br/comprar/carros/novos-usados/'
        'veiculos-todos-estados/?tipoveiculo=carros&tipoanuncio'
        '=novos%7Cusados&palavrachave=megane&estado1=veiculos-todos-estados'
        '&qt=12&o=1&p={}'
    )

    def __init__(self, force_last_page=None):
        # Paramether force_last_page
        if force_last_page:
            self.force_last_page = int(force_last_page)

        self.last_page = None

    def start_requests(self):
        """Create request to first page"""
        request = scrapy.Request(
            url=WebmotorsSpider.first_page_url.format(1),
            callback=self.parse_page,
        )
        # print("Request:", request)
        # print("*** url: ***", request.url)
        # print("*** callback: ***", request.callback)
        yield request

    def parse_page(self, response):
        """
        Create requests to links of all pages and
        set the last page
        """
        # get anchor link on "last page" button
        last_button_anchor = response.xpath(
            '//*[contains(@id, "boxResultado")]'
            '/div/a/@href')[-1].extract()

        # get the last page from href
        self.last_page = int(last_button_anchor.split("p=")[-1])

        if self.force_last_page:
            self.last_page = self.force_last_page

        for page in range(1, self.last_page):
            request = scrapy.Request(
                url=WebmotorsSpider.first_page_url.format(self.last_page),
                # callback=self.parse_car_link,
            )
            print("Request:", request)
            print("*** url: ***", request.url)
            # print("*** callback: ***", request.callback)
            yield request

        # # Create car item
        # car = CarItem()
        # car['brand'] = brand
        # car['model'] = model
        # yield car
