import scrapy


class NvidiaSpider(scrapy.Spider):
    name = 'nvidia'
    # allowed_domains = ['https://www.nvidia.com/en-gb/geforce/graphics-cards/30-series/rtx-3080/']
    start_urls = ['http://www.nvidia.com/en-gb/geforce/graphics-cards/30-series/rtx-3080']

    # Landing page
    def parse(self, response):
        card_name = response.css('h1 ::text').extract()
        # out_of_stock = response.css('.cta-button.btn.show-out-of-stock ::text').extract()
        # out_of_stock = response.xpath("//*[contains(text(), 'Out of Stock')]/text()").extract()
        out_of_stock = response.xpath("//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see all')]").extract() or None

        if out_of_stock is None:
            out_of_stock = True
        else:
            out_of_stock = False

        scraped_info = {
            'Card name': card_name,
            'Out of stock': out_of_stock
        }

        print(scraped_info)
        return scraped_info
