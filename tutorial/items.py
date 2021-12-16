# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field
from itemloaders.processors import MapCompose, Join
from datetime import datetime

def convert_date(text):
    return datetime.strptime(text, '%Y-%m-%d, %H:%M')

def get_end_of_url(text):
    return text.split('/')[-1]

# lowercases, then removes urls
def get_clean_text(text: str):
    clean_text = text.lower()
    clean_text = re.sub(r'https?://\S+', '', clean_text)
    # clean_text = re.sub(r'[^a-z ]+', '', clean_text)

    return clean_text

# '#41' => '41'
def get_post_number(text):
    return text[1:]

class ForumPost(Item):
    post_id = Field()
    date = Field()
    author = Field(
        output_processor = MapCompose(get_end_of_url)
    )
    text = Field(
        input_processor = MapCompose(get_clean_text),
        output_processor = Join()
    )
    forum_id = Field()
    thread_id = Field()

class BerserkPost(Item):
    post_id = Field()
    date = Field()
    author = Field(
        output_processor = MapCompose(get_end_of_url)
    )
    text = Field(
        input_processor = MapCompose(get_clean_text),
        output_processor = Join()
    )
    forum_id = Field()
    thread_id = Field()
    
