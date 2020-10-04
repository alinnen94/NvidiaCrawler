import scrapy


class BrickbotSpider(scrapy.Spider):
    name = 'brickbot'
    # allowed_domains = ['www.brickset.com']
    start_urls = ['http://brickset.com/sets/year-2016']

    # def parse(self, response):
    #     # Extracting the content using css selectors
    #     titles = response.css('.title.may-blank::text').extract()
    #     votes = response.css('.score.unvoted::text').extract()
    #     times = response.css('time::attr(title)').extract()
    #     comments = response.css('.comments::text').extract()
    #
    #     # Give the extracted content row wise
    #     for item in zip(titles, votes, times, comments):
    #         # create a dictionary to store the scraped info
    #         scraped_info = {
    #             'title': item[0],
    #             'vote': item[1],
    #             'created_at': item[2],
    #             'comments': item[3],
    #     }
    #
    #     # yield or give the scraped info to scrapy
    #     yield scraped_info

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
