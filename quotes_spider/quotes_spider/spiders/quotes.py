from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from quotes_spider.items import QuotesSpiderItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser



class QuotesSpider(Spider):
    name = 'quotes'
    # for login, don't need allowed domains
    #allowed_domains = ['quotes.toscrape.com']
    # start urls also will be different
    #start_urls = ['https://quotes.toscrape.com/']
    start_urls = ['https://quotes.toscrape.com/login']
    
    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        print(token)
        form_data = {
            'csrf_token': token,
            'password'  : 'foobar',
            'username'  : 'foob'
        }
        
        return FormRequest.from_response(response, formdata=form_data, callback=self.scrape_home)

    # Renaming this for login
    # def parse(self, response):
    def scrape_home(self, response):
        # use the response xpath here
        # h1_tag = response.xpath('//h1/a/text()').extract()[0]
        # tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        # yield {
        #     'h1': h1_tag,
        #     'Tags': tags 
        # }
        open_in_browser(response) # using debuging
        loader = ItemLoader(item=QuotesSpiderItem(), response=response)
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first()
            loader.add_value('text', text)
            loader.add_value('author', author)
            loader.add_value('tags', tags)
            yield loader.load_item()



        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolut_next_page_url = response.urljoin(next_page_url)

        yield Request(absolut_next_page_url)