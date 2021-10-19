# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime


def remove_quotes(text):
    return text[1:-1]


def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y').date()


def parse_location(text):
    return text.removeprefix('in ')


def parse_info(text):
    return text.strip().replace('\n', '')


class SpyderItem(Item):
    author = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    quote = Field(input_processor=MapCompose(remove_quotes), output_processor=TakeFirst())
    tags = Field()
    author_url = Field()
    author_birthday = Field(input_processor=MapCompose(convert_date), output_processor=TakeFirst())
    author_location = Field(input_processor=MapCompose(parse_location), output_processor=TakeFirst())
    author_info = Field(input_processor=MapCompose(parse_info), output_processor=TakeFirst())
