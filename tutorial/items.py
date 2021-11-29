# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class TutorialItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ForumPost(Item):
    date = Field()
    author = Field()
    text = Field(
        output_processor=
    )
