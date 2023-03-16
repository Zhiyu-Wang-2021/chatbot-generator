import os,sys,unittest
sys.path.append(os.curdir + '/chatbotSite')
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from webscraptool.url_crawler.url_crawler.spiders.crawl_url import Url_Crawler
from webscraptool.get_text.get_text.spiders.get_text import Scrape_Text
from scrapy.crawler import CrawlerProcess

import webscraptool.get_valid_url as get_valid_url
import os,signal,time,threading
# run command
# coverage run --branch -m unittest chatbotSite/unitTest/test_webcrawling_scraping.py
# you also need to use this command to start our local scrapy test website
# 1.go to the target folder of our test local html website(/unittestwebsite)
# 2.run this command
# python -m http.server 8000 --bind 127.0.0.1

class TestWebscraptool(unittest.TestCase):
    def test_url_crawl(self):
        results = []
        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)
        process = CrawlerProcess(get_project_settings())
        process.crawl(Url_Crawler, url='127.0.0.1:8000')
        process.start()

        # the script will fixed twisted problem
        import sys
        del sys.modules['twisted.internet.reactor']
        from twisted.internet import reactor
        from twisted.internet import default
        default.install()
        # the script will block here until the crawling is finished

        # should stop at page4 due to depth limit we set
        expected_ans = [{'title': 'page1', 'url': 'http://127.0.0.1:8000/page1.html'},
                {'title': None, 'url': 'http://127.0.0.1:8000/page2.html'}, 
                {'title': None, 'url': 'http://127.0.0.1:8000/page3.html'}, 
                {'title': None, 'url': 'http://127.0.0.1:8000/page4.html'}]
        res = results
        self.assertEqual(res, expected_ans)

    def test_get_text(self):

        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append({'text':item['text']})


        dispatcher.connect(crawler_results, signal=signals.item_scraped)
        process = CrawlerProcess(get_project_settings())
        process.crawl(Scrape_Text, url='http://127.0.0.1:8000/scrape.html')
        process.start()

        # the script will fixed twisted error(work around scrapy block us from restart)
        import sys
        del sys.modules['twisted.internet.reactor']
        from twisted.internet import reactor
        from twisted.internet import default
        default.install()

        res = results
        expected_ans = [{'text': 'scrapeme\nscrapeme\n'}]
        self.assertEqual(res, expected_ans)

    def test_get_valid_url(self):
        page_dictionary1 = {'general_info':['contact',
                            'contact-us/',
                            'about-us/contact-us/',
                            'practice-information/contact-us/'
                    ]}
        expected_ans = [{'url': 'http://127.0.0.1:8000/contact'}]
        res = get_valid_url.run('127.0.0.1:8000',page_dictionary1['general_info'])
        self.assertEqual(res, expected_ans)

    def test_get_valid_url_empty_input(self):
        page_dictionary1 = {'general_info':['contact',
                            'contact-us/',
                            'about-us/contact-us/',
                            'practice-information/contact-us/'
                    ]}
        expected_ans = []
        res = get_valid_url.run('',page_dictionary1['general_info'])
        self.assertEqual(res, expected_ans)

    def test_get_valid_url_wrong_input(self):
        page_dictionary1 = {'general_info':['contact',
                            'contact-us/',
                            'about-us/contact-us/',
                            'practice-information/contact-us/'
                    ]}
        expected_ans = []
        res = get_valid_url.run('http://127.0.0.1:8000/',page_dictionary1['general_info'])
        self.assertEqual(res, expected_ans)