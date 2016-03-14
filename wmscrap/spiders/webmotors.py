# -*- coding: utf-8 -*-
import scrapy
from unicodedata import normalize
from wmscrap.items import CarItem


class WebmotorsSpider(scrapy.Spider):
    name = "webmotors"
    allowed_domains = ["webmotors.com.br"]
    first_page_url = (
        'http://www.webmotors.com.br/comprar/carros/novos-usados/'
        'veiculos-todos-estados/?tipoveiculo=carros'
        '&tipoanuncio=novos%7Cusados'
        '&estado1=veiculos-todos-estados&o=1&p={}'
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
                callback=self.parse_car_link,
            )
            yield request

    def parse_car_link(self, response):
        """Create request to car detail description"""

        # filter links of car detail description
        results = response.xpath(
            '//*[contains(@id, "boxResultado")]'
            '/a/@href')

        for car_link in results:
            url_detail_description = car_link.extract()
            request = scrapy.Request(
                url=url_detail_description,
                callback=self.parse_car_detail_description,
            )
            yield request

    def remove_accents(txt, codif='utf-8'):
        return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')

    def parse_car_detail_description(self, response):
        makemodel_class = response.xpath(
            '//*[contains(@class,"makemodel")]'
            '/text()').extract_first()

        try:
            makemodel_class = makemodel_class.split()
            # brand = self.remove_accents(makemodel_class[0])
            brand = makemodel_class[0]
            # model = self.remove_accents(" ".join(makemodel_class[1:]))
            model = " ".join(makemodel_class[1:])
            model = self.remove_accents(str(model))
            print(model)
        except ValueError as e:
            print("URL {}, error : {}".format(response.url, e))
            return
        except Exception as e:
            print("URL {}, generic error : {}".format(response.url, e))
            return

        # Create car item
        car = CarItem()
        car['brand'] = brand
        car['model'] = model
        yield car
