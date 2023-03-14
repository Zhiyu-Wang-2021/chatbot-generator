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
import webscraptool.get_valid_url as get_vaild_url
import os,signal,time,threading

def timeout_handler():
    # For Windows
    # send ctrl + c to prompt to terminate web scraping process
    #os.kill(os.getpid(), signal.CTRL_C_EVENT)
    #time.sleep(2)
    #os.kill(os.getpid(), signal.CTRL_C_EVENT)
    
    # For Linux or MacOS
    time.sleep(2)
    # send to shutdown(for linux)
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(2)
    os.kill(os.getpid(), signal.SIGINT)

class Tool(Abstract_Tool):
    def __init__(self) -> None:
        super().__init__()
        self.mainsite = ''
        self.url_dict = []

    def setup(self, link) -> None:
        # timer for method to terminate scraping process when it gets stuck(take too long) due to some error
        timer = threading.Timer(1000.0, timeout_handler)
        timer.start()

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

        # if time is not out we need to cancel the timer
        timer.cancel()
        self.url_dict = results
           
    def crawl_url_by_dictionary(self, dict_name):
        page_dictionary1 = {'general_info':['contact',
                            'contact-us/',
                            'our-services/our-hospitals/university-college-hospital',
                            'about-us/contact-us/',
                            'practice-information/contact-us/',
                            'about-us/contact/location/',
                            'about-us/contact/contact-telephone-numbers/',
                            'contact/location/',
                            'contact/contact-telephone-numbers/',
                            'contact1.aspx',
                            'how-to-find-us/',
                            'find-us',
                            'contact-us/?practice-selected=practice-2',
                            'contact-us/?practice-selected=practice-1',
                            'contact-us/?practice-selected=practice-3',
                            'page1.aspx?p=3&pr=F83624&t=1&high=opening',
                            'contact-us/contact-details/',
                            'opening-times/',
                            'about-us/opening-hours/',
                            'opening-hours',
                            'practice-information/opening-hours/'
                    ]}
        # check if input dict_name is valid
        if not len(page_dictionary1.get(dict_name)) > 0:
            return []
        elif not type(dict_name) == str:
            return []
        return get_vaild_url.run(self.mainsite, page_dictionary1[dict_name])
    

    def filter_url(self, keywords, blacklist_keywords) -> list:
        result = []
        # add homepage
        result.append({'title':'', 'url':'https://' + self.mainsite, 'keyword':''})
        
        # check if keyword is in title
        for url in self.url_dict:
            for keyword in keywords:

                if url['title'] is not None and keyword in url['title']:
                    # check black list
                    blacklist_flag = 0

                    for blacklist_keyword in blacklist_keywords:

                        if blacklist_keyword in url['title']:  
                            blacklist_flag = 1     
                    if blacklist_flag == 0:            
                        result.append({'title':url['title'], 'url':url['url'], 'keyword':keyword})
        
        return result
    
    def scrape_text(self, filtered_urls) -> dict:
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append({'text':item['text']})

        for link in filtered_urls:
            # give 45 seconds for each url
            timer = threading.Timer(45.0, timeout_handler)
            timer.start()

            dispatcher.connect(crawler_results, signal=signals.item_scraped)
            process = CrawlerProcess(get_project_settings())
            process.crawl(Scrape_Text, url=link['url'])
            process.start()

            # the script will fixed twisted error(work around scrapy block us from restart)
            import sys
            del sys.modules['twisted.internet.reactor']
            from twisted.internet import reactor
            from twisted.internet import default
            default.install()   
            timer.cancel()


        if len(filtered_urls) != 0:
            return {'text':results}
        
        # return null if no url crawled
        return {'text':results}
    
    def filter_text(self, content_dict, category) -> dict:
        categories = {'':0, 'openingtime':1,'address':2,'phonenumber':3}
        i = categories.get(category)
        result = []

        if i == 0:
            pass

        else:
            # combined and filtering content
            for j in content_dict['text']:
                temp = []

                if i == 1:
                    temp = get_openingtime.run(j['text'])
                    print(temp)
                    if temp is not None:
                        result = result + temp

                if i == 2:
                    temp = get_addr.run(j['text'])
                    print(temp)
                    if temp is not None:
                        result = result + temp

                if i == 3:
                    temp = get_phone_num.run(j['text'])
                    print(temp)
                    if temp is not None:
                        result = result + temp

        print('-------------------no-filtered-result----------------')
        print(result)
        if i == 1:
            result = filter_content.openingtime(result)
        elif i == 2:
            result = filter_content.addr(result)
        elif i == 3:
            result = filter_content.phonenumber(result)
                
        return {'filtered_text': result}
