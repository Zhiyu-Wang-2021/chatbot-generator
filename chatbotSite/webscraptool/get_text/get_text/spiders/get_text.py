# command:
# scrapy crawl get_text -a url=https://www.gosh.nhs.uk/about-us/contact-us/
import scrapy
import re
import os

class Scrape_Text(scrapy.Spider):

    name = 'get_text'
    
    # change user agent to bypass firewall
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        }
    
    def __init__(self, url=None, *args, **kwargs):
        super(Scrape_Text, self).__init__(*args, **kwargs)
        # remove 'http://' prefix to avoid causing error
        self.start_urls = [f'{url}']

    def parse(self, response):
        l1 = response.selector.xpath('//body/descendant-or-self::*[not(self::script | self::style)]/text()').getall()
        content = ''
        item = {}
        
        for text in l1:
            if not str.isspace(text):
                content = content + text + '\n'


        yield {'text':content}
