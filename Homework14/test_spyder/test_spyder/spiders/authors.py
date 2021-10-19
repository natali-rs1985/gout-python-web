import scrapy
from scrapy.loader import ItemLoader
import requests
from bs4 import BeautifulSoup

from test_spyder.items import SpyderItem


class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            loader = ItemLoader(item=SpyderItem(), selector=quote)
            loader.add_xpath('tags', ".//div[@class='tags']/a/text()")
            loader.add_xpath('quote', ".//span[@class='text']/text()")
            author_url = self.start_urls[0] + quote.xpath("span[2]/a/@href").get()
            loader.add_value('author_url', author_url)

            r = requests.get(author_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            inf = soup.find('div', {'class': "author-details"})
            author = inf.find('h3', {'class': "author-title"}).text
            author_birthday = inf.find('span', {'class': "author-born-date"}).text
            author_location = inf.find('span', {'class': "author-born-location"}).text
            author_info = inf.find('div', {'class': "author-description"}).text

            loader.add_value('author', author)
            loader.add_value('author_birthday', author_birthday)
            loader.add_value('author_location', author_location)
            loader.add_value('author_info', author_info)
            yield loader.load_item()

            # quote_item = loader.load_item()
            # yield response.follow(author_url, callback=self.parse_author, meta={'quote_item': quote_item})

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    # def parse_author(self, response):
    #     # print('-------------------------------------------------------------------')
    #     # print(response.text)
    #
    #     quote_item = response.meta['quote_item']
    #     loader = ItemLoader(item=quote_item, response=response)
    #     loader.add_xpath('author', ".//h3/text()")
    #     loader.add_xpath('author_birthday', ".//span[@class='author-born-date']/text()")
    #     loader.add_xpath('author_location', ".//span[@class='author-born-location']/text()")
    #     loader.add_xpath('author_info', ".//div[@class='author-description']/text()")
    #     yield loader.load_item()
