# -*- coding: utf-8 -*-
import scrapy
from wmscrap.items import CarItem


class WebmotorsSpider(scrapy.Spider):
    name = "webmotors"
    allowed_domains = ["webmotors.com.br"]
    first_page_url = (
        'http://www.webmotors.com.br/comprar/carros/usados/'
        'veiculos-todos-estados/'
        '?tipoveiculo=carros'
        '&tipoanuncio=usados'
        '&estado1=veiculos-todos-estados&qt=12&o=1&p={}'
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
<<<<<<< HEAD
                callback=self.parse,
            )
            yield request

    def parse(self, response):
        """Parse all information to CarItem"""

        model_items = response.xpath(
            '//*[contains(@class,"make-model")]'
            '/text()').extract()

        brands = []
        models = []
        for m in model_items:
            try:
                model_brand = m.split()
                brand = model_brand[0]
                model = " ".join(model_brand[1:])
                brands.append(brand)
                models.append(model)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

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

        # If size of lists is not equal something wrong
        if len(prices) == len(models) == len(brands) == len(images):
            size = len(prices)
            for i in range(0, size):
                car = CarItem()
                car['brand'] = brands[i]
                car['model'] = models[i]
                car['price'] = prices[i]
                car['image'] = images[i]
                yield car
        else:
            error_message = ("Error with size of lists: prices={}, "
                             "models={}, brands={}, images={}")
            print(error_message.format(len(prices), len(models), len(brands),
                                       len(images)))
=======
                callback=self.parse_car_description,
            )
            yield request

    def parse_car_description(self, response):
        # get make and model of car
        results = response.xpath(
            '//*[@class="info"]/h2/span[1]/text()').extract()

        try:
            model = results
        except ValueError as e:
            print("URL {}, error: {}".format(response.url, e))
            return
        except Exception as e:
            print("URL {}, generic error: {}".format(response.url, e))
            return

        # Create car item
        car = CarItem()
        car['model'] = model
        yield car

        # print('---------------')
        # for result in results:
        #     print(result)
        # print('---------------')
>>>>>>> master
