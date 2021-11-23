import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response, **kwargs):
        self.logger.info('wana created a spider')
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('.text::text').get()
            }