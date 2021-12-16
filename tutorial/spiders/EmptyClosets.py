import scrapy
from itemloaders import ItemLoader

class EmptyClosetsSpider(scrapy.Spider):
    name = 'EmptyClosets'

    allowed_domains = ['forum.emptyclosets.com']
    start_urls = ['https://forum.emptyclosets.com/']

    def parse(self, response):
        pass
    """
    From main page
    Ex: https://forum.emptyclosets.com/index.php
    Gets links to forums
        div.nodeText > h3.nodeTitle > a[data-description]::attr(href)
    
    Navbar next
        nav > a:last-child.text::attr(href)
    Empty on single-page stuff

    From forum page
    Ex: https://forum.emptyclosets.com/index.php?forums/family-friends-and-relationships.142/
    Gets a thread selector
        li.discussionListItem
    Get thread link
        h3.title > a.PreviewTooltip::attr(href)
    
    From post page
    Get text
        li.sectionMain.message div.messageContent blockquote.messageText").xpath("normalize-space(.)
    """
