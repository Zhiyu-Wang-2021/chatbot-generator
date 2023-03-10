# command:
# scrapy crawl crawl_url -a url=www.gosh.nhs.uk
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Url_Crawler(CrawlSpider):
    name = 'crawl_url'
    
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )
    
    # delay and change user agent to bypass firewall
    custom_settings = {
        #'DOWNLOAD_DELAY': 1, # 1-3 seconds of delay
        #'RANDOMIZE_DOWNLOAD_DELAY': True,
        'USER_AGENT' : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        }
    
    # allow passing url as an attribute through command line
    def __init__(self, url=None, *args, **kwargs):
        super(Url_Crawler, self).__init__(*args, **kwargs)
        self.start_urls = [f'http://{url}/']
        self.allowed_domains = [f'{url}']
        self.links = []
#why cannot get uclh contactpage???
    def parse_item(self, response):
        if 'depth' in response.meta: depth = response.meta['depth']
        # only follow 4 layers of link and exit so as to avoid crawling to much links
        if depth > 4: raise scrapy.exceptions.CloseSpider(reason='maximum depth reached!')
        # if len(self.links) > 100: raise scrapy.exceptions.CloseSpider(reason='maximum length reached!')
        item = {}
        item['title'] = response.css('title::text').get()
        item['url'] = response.request.url
        self.links.append(item)
        yield item
