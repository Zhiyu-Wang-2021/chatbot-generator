# command:
# scrapy crawl get_text -a url=https://www.gosh.nhs.uk/about-us/contact-us/
import scrapy
import re
import os

class PostSpider(scrapy.Spider):

    name = 'get_text'

    def __init__(self, url=None, *args, **kwargs):
        super(PostSpider, self).__init__(*args, **kwargs)

        self.start_urls = [f'{url}']

    def parse(self, response):
        filename = '../content.txt'
        l1 = response.selector.xpath('//body/descendant-or-self::*[not(self::script | self::style)]/text()').getall()
        content = ''

        for text in l1:
            if not str.isspace(text):
                content = content + text + '\n'

        f = open (filename, 'a', encoding='utf-8')
        f.write(content)
        f.close()
