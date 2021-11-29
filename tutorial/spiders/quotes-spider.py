import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import ForumPost

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['https://www.quakeworld.nu/forum/6/page/1']

    def parse(self, response, **kwargs):
        yield from response.follow_all(
            self.get_links_from_navbar(response), 
            callback=self.parse_forum)

        # print(response.css("div.forumpost-body div.row:first-child div:not(.bb-quote):not(.bb-quote-header)::text").getall()[-3])
        # [link.split('\'')[1] for link in response.css("div > div > div.table span.pagenav::attr(onclick)").getall()]
        # [f"{page_link_prefix}/{page_num + 1}" for page_num in range(int(last_link.split('/')[-1]))]
    
    """
    Example url: https://www.quakeworld.nu/forum/6
    Gathers links to threads, callbacks to parse_thread
    """
    def parse_forum(self, response, **kwargs):
        thread_titles = response.css('a.forumname-read')
        
        yield {
            'title': thread_titles[0].css('::text').get()
        }
    

    """
    Example url: https://www.quakeworld.nu/forum/topic/7310/gaming-monitor
    

    """
    def parse_thread(self, response, **kwargs):
        pass


    """
    Example url: https://www.quakeworld.nu/forum/topic/7310/gaming-monitor
    """
    def parse_page(self, response, **kwargs):
        full_posts = response.css("div.forumpost-0, div.forumpost-1")

        for full_post in full_posts:
            post_loader = ItemLoader(item=ForumPost(), selector=full_post)
            post_loader.add_css(
                'text', 
                'div.forumpost-body div.row:first-child div:not(.bb-quote):not(.bb-quote-header)::text'
            )
            post_loader.add_css(
                'date',
                'div.col_forum::text'
            )
            post_loader.add_css(
                'author',
                'a.link_body::attr(href)'
            )

            post_loader.load_item()

    def get_links_from_navbar(self, response):
        urls = response.css(
            "div > div > div.table span:last-child::attr(onclick)"
        )

        last_url = urls[-1].get().split('\'')[1] # split on quote mark to get url
        last_url_split = last_url.split('/') # split url to get index
        last_url_index = int(last_url_split[-1])
        url_prefix = '/'.join(last_url_split[:-1])

        links_to_follow = [
            f"{url_prefix}/{page_num}" for page_num in
            range(1, last_url_index + 1)
        ]

        return links_to_follow