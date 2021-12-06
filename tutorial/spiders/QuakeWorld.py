import scrapy
from itemloaders import ItemLoader
from tutorial.items import ForumPost

class ForumSpider(scrapy.Spider):
    name = "quake"

    start_urls = ['https://www.quakeworld.nu/forum']

    def parse(self, response, **kwargs):
        yield from response.follow_all(
            css="td.forumlist a.forumname::attr(href)",
            callback=self.print_title
        )
    
    """
    Example url: https://www.quakeworld.nu/forum/6
    Gathers links to threads, callbacks to parse_thread
    """
    def parse_forum(self, response, **kwargs):
        forum_url = response.request.url
        thread_titles = response.css('a.forumname-read')
        
        yield {
            'title': thread_titles[0].css('::text').get(),
            'url': forum_url
        }

        thread_urls = []

    """
    Example url: https://www.quakeworld.nu/forum/topic/7310/gaming-monitor

    """
    def parse_thread(self, response, **kwargs):
        yield from response.follow_all(
            self.get_links_from_navbar(response, False), 
            callback=self.parse_page
        )


    """
    Example url: https://www.quakeworld.nu/forum/topic/7310/gaming-monitor
    """
    def parse_page(self, response, **kwargs):
        full_posts = response.css("div.forumpost-0, div.forumpost-1")

        for full_post in full_posts:
            post_loader = ItemLoader(item=ForumPost(), selector=full_post)
            post_loader.add_css(
                'post_id',
                '::attr(id)'
                )
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
            # post_loader.add_css(
            #     'thread',

            # )
            # post_loader.add_css(
            #     'thread_id',
            #     'div.col_forum + div a.forumlink::text'
            # )

            post_item = post_loader.load_item()

            yield post_item


    def print_title(self, response, **kwargs):
        # self.logger.info('printing title')
        forum_url = response.request.url
        yield {
            'title': response.css("title::text").get(),
            'url': forum_url
        }

    def get_links_from_navbar(self, response, exclude_first=True):
        urls = response.css(
            "div > div > div.table span:last-child::attr(onclick)"
        )

        last_url = urls[-1].get().split('\'')[1] # split on quote mark to get url
        last_url_split = last_url.split('/') # split url to get index
        last_url_index = int(last_url_split[-1])
        url_prefix = '/'.join(last_url_split[:-1])

        start_url_index = 2 if exclude_first else 1

        links_to_follow = [
            f"{url_prefix}/{page_num}" for page_num in
            range(start_url_index, last_url_index + 1)
        ]

        return links_to_follow