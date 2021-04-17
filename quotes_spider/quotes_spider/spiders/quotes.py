import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        # use the response xpath here
        h1_tag = response.xpath('//h1/a/text()').extract()[0]
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        yield {
            'h1': h1_tag,
            'Tags': tags 
        }

