# -*- coding: utf-8 -*-
import scrapy
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
        ''' Create request to first page '''
        request = scrapy.Request(
            url=WebmotorsSpider.first_page_url.format(1),
            callback=self.parse_page,
        )
        yield request

    def parse_page(self, response):
        '''
        Create requests to links of all pages
        and set the last page
        '''
        # get anchor link on "last page" button
        last_button_anchor = response.xpath(
            '//*[contains(@id, "boxResultado")]/div/a/@href')[-1].extract()
        # get the last page from href
        self.last_page = int(last_button_anchor.split("p=")[-1])

        if self.force_last_page:
            self.last_page = self.force_last_page

        # page 1 to last page
        for page in range(1, self.last_page):
            request = scrapy.Request(
                url=WebmotorsSpider.first_page_url.format(page),
                callback=self.parse,
            )
            yield request

    def parse(self, response):
        """Parse all information to CarItem"""

        ''' Extract the link '''
        link_items = response.xpath(
            '//*[contains(@id, "boxResultado")]/a/@href').extract()

        links = []
        for l in link_items:
            try:
                links.append(l)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        ''' Extract model and maker '''
        model_items = response.xpath(
            '//*[contains(@class,"make-model")]'
            '/text()').extract()

        makers = []
        models = []
        for m in model_items:
            try:
                model_maker = m.split()
                maker = model_maker[0]
                model = " ".join(model_maker[1:])
                makers.append(maker)
                models.append(model)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        ''' Extract price '''
        prices_items = response.xpath(
            '//*[contains(@class,"price")]/text()').extract()

        prices = []
        for p in prices_items:
            try:
                clean_price = p.strip()
                if clean_price == '':
                    continue
                prices.append(clean_price)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        ''' Extract image '''
        image_tags = response.xpath(
            '//*[contains(@id, "boxResultado")]//img'
            '/@data-original').extract()

        images = []
        for i in image_tags:
            try:
                images.append(i)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        ''' Extract city '''
        city_tags = response.xpath(
            '//*[contains(@class,"card-footer")]'
            '/span[1]/text()').extract()

        cities = []
        for city in city_tags:
            try:
                cities.append(city)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        ''' Extract yearMaker '''
        yearmaker_tags = response.xpath(
            '//*[contains(@class,"features")]/div[1]/span[1]/text()').extract()

        yearmakers = []
        for yearmaker in yearmaker_tags:
            try:
                yearmakers.append(yearmaker)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        ''' Extract Km '''
        km_tags = response.xpath(
            '//*[contains(@class,"features")]/div[2]/span[1]/text()').extract()

        kms = []
        for km in km_tags:
            try:
                kms.append(km)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

        # If size of lists is not equal something wrong
        if len(prices) == len(models) == len(makers) == len(images):
            size = len(prices)
            for i in range(0, size):
                car = CarItem()
                car['link'] = links[i]
                car['maker'] = makers[i]
                car['model'] = models[i]
                car['price'] = prices[i]
                car['image'] = images[i]
                car['city'] = cities[i]
                # state
                car['yearmaker'] = yearmakers[i]
                # yearModel
                car['km'] = kms[i]
                yield car
        else:
            error_message = ("Error with size of lists: prices={}, "
                             "models={}, makers={}, images={}")
            print(error_message.format(len(prices), len(
                models), len(makers), len(images)))
