# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, Join
from datetime import datetime

def convert_date(text):
    return datetime.strptime(text, '%Y-%m-%d, %H:%M')

def get_end_of_url(text):
    return text.split('/')[-1]

class ForumPost(Item):
    post_id = Field()
    date = Field(
        output_processor = MapCompose(convert_date)
    )
    author = Field(
        output_processor = MapCompose(get_end_of_url)
    )
    text = Field(
        input_processor = MapCompose(str.strip, str.lower),
        output_processor = Join()
    )
    # thread = Field()
    # thread_id = Field()
