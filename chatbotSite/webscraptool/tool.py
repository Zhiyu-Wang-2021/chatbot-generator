from webscraptool.abstract_tool_template import Abstract_Tool
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from webscraptool.url_crawler.url_crawler.spiders.crawl_url import Url_Crawler
from webscraptool.get_text.get_text.spiders.get_text import Scrape_Text
from scrapy.crawler import CrawlerProcess

import webscraptool.get_addr as get_addr
import webscraptool.get_openingtime as get_openingtime
import webscraptool.get_phone_num as get_phone_num

import webscraptool.filter_content as filter_content


class Tool(Abstract_Tool):
    def __init__(self) -> None:
        super().__init__()
        self.mainsite = ''
        self.url_dict = []

    def setup(self, link) -> None:
        self.mainsite = link
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        process = CrawlerProcess(get_project_settings())
        process.crawl(Url_Crawler, url=self.mainsite)
        process.start()

        # the script will fixed twisted problem
        import sys
        del sys.modules['twisted.internet.reactor']
        from twisted.internet import reactor
        from twisted.internet import default
        default.install()
        # the script will block here until the crawling is finished

        self.url_dict = results

    def filter_url(self, keywords, affixs, category) -> list:
        result = []

        # check if keyword is in title
        for url in self.url_dict:
            for keyword in keywords:
                if url['title'] is not None and keyword in url['title']:
                    result.append({'title':url['title'], 'url':url['url'], 'category':category, 'keyword':keyword})

        return result
    
    def scrape_text(self, filtered_urls) -> dict:

        results = []

        # I don't know why but only list can be used here.
        # If you use string you will get empty result...
        def crawler_results(signal, sender, item, response, spider):
            results.append(item['text'])

        for url in filtered_urls:
            dispatcher.connect(crawler_results, signal=signals.item_scraped)
            # remove 'http://' or scrapy can not recognized the link
            url_replaced = url['url'].replace('http://', '')
            process = CrawlerProcess(get_project_settings())
            process.crawl(Scrape_Text, url=url_replaced)
            process.start()

            # the script will fixed twisted error
            import sys
            del sys.modules['twisted.internet.reactor']
            from twisted.internet import reactor
            from twisted.internet import default
            default.install()   
        
        r = ''
        for result in results:
            r = r + result
        if len(filtered_urls) != 0:
            return {'category':filtered_urls[0]['category'], 'text':r}

        # return null if no url crawled
        return {'category':'none', 'text':r}
    
    def filter_text(self, content_dict) -> dict:
        categories = {'none':0, 'openingtime':1,'address':2,'phonenumber':3}
        i = categories.get(content_dict['category'])
        result = {}

        if i == 0:
            result = 'null'

        if i == 1:
            result = get_openingtime.run(content_dict['text'])
            result = filter_content.openingtime(result)

        if i == 2:
            result = get_addr.run(content_dict['text'])
            result = filter_content.addr(result)

        if i == 3:
            result = get_phone_num.run(content_dict['text'])
            result = filter_content.phonenumber(result)

        return {'category': content_dict['category'], 'filtered_text': result}
