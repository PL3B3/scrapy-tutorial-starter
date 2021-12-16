import scrapy
from itemloaders import ItemLoader
from tutorial.items import ForumPost, get_end_of_url
from tutorial.utils import split_url

class ForumSpider(scrapy.Spider):
    name = "quake"

    start_urls = ['https://www.quakeworld.nu/forum']

    def parse(self, response, **kwargs):
        yield from response.follow_all(
            css='a.forumname',
            callback=self.parse_forum
        )
    

    # Example url: https://www.quakeworld.nu/forum/63/north-american-qw
    # Follows up on all pages of this forum
    def parse_forum(self, response, **kwargs):
        yield from response.follow_all(
            self.get_links_from_navbar(response, False), 
            callback=self.parse_forum_page
        )
    
    
    # Example url: https://www.quakeworld.nu/forum/63/north-american-qw/page/2
    # Follows links to threads on this forum page
    def parse_forum_page(self, response, **kwargs):
        yield from response.follow_all(
            css='a.forumname-read', 
            callback=self.parse_thread
        )


    # Example url: https://www.quakeworld.nu/forum/topic/7310/gaming-monitor
    # Follows navbar links to all pages in thread
    def parse_thread(self, response, **kwargs):
        yield from response.follow_all(
            self.get_links_from_navbar(response, False), 
            callback=self.parse_thread_page
        )



    # Example url: https://www.quakeworld.nu/forum/topic/7310/gaming-monitor
    # yields post items
    def parse_thread_page(self, response, **kwargs):
        (forum_id, thread_id) = tuple([
            get_end_of_url(nav_url)
            for nav_url in
            response.css('div.forumnav a.forumbread::attr(href)').getall()[1:]
        ])

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
            post_loader.add_value(
                'text',
                full_post.css('div.forumpost-body div.row div.cell:first-child > div').xpath('./text() | .//*[not(@class=\'bb-code\')]/text()')
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
            #     'post_position_in_thread',
            #     'a.forumlink::text'
            # )
            post_loader.add_value(
                'forum_id',
                forum_id
            )
            post_loader.add_value(
                'thread_id',
                thread_id
            )

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