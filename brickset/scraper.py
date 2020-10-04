import scrapy
from scrapy.crawler import CrawlerProcess
import time
import logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater
from playsound import playsound

# Turn logging off
logging.getLogger('scrapy').propagate = False

earth_wind_fire = "C:/Users/linne/Downloads/September.mp3"


# Spider
class NvidiaSpider(scrapy.Spider):
    name = 'nvidia'
    start_urls = ['http://www.nvidia.com/en-gb/geforce/graphics-cards/30-series/rtx-3080']

    # Landing page
    def parse(self, response):
        card_name = response.css('h1 ::text').extract()
        # out_of_stock = response.css('.cta-button.btn.show-out-of-stock ::text').extract()
        # out_of_stock = response.xpath("//*[contains(text(), 'Out of Stock')]/text()").extract()
        out_of_stock = response.xpath("//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', \
         'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]").extract() or None

        print(out_of_stock)

        if out_of_stock is None:
            out_of_stock = True
        else:
            out_of_stock = False

        scraped_info = {
            'Card name': card_name,
            'Out of stock': out_of_stock
        }

        if out_of_stock == False:
            playsound(earth_wind_fire)

        print(scraped_info)
        return scraped_info


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


process = CrawlerProcess(get_project_settings())


def _crawl(result, spider):
    deferred = process.crawl(spider)
    # deferred.addCallback(lambda results: print('waiting 5 seconds before restart...'))
    deferred.addCallback(sleep, seconds=5)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, NvidiaSpider)
process.start()
