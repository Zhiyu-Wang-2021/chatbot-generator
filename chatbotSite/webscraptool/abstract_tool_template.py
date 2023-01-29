from abc import ABC, abstractmethod


class Abstract_Tool(ABC):
    @abstractmethod
    def __init__(self) -> None:
        # self.mainsite
        # self.url_dict
        
        pass

    def setup(self) -> None:
        # crawl all the url -> store all url and their title in a dict
        # self.url_dict = [{title:title, url:url},...]
        # store main site in self.main_site
        pass

    def filter_url(self, keywords, affixs, category) -> list:
        # filter out url with specific keyword in title or specific affix
        # store filtered url in a dict 'self.filtered_url'
        # category is the type of information useful in latter process
        # e.g. if we need to get address the category should be filled in as 'address'
        # all the dict in the list should be as follow
        # [{'title','link','category','keyword','affix'},{},....]
        # all keywords should be as follow
        # ['keyword1', 'keyword2',.....]
        
        # ***note that check affix is not implemented yet


        pass

    def scrape_text(self, filtered_url) -> dict:
        # return empty if url is not filtered
        # scrape text from 'self.filtered_url' store as dictionary(content_dict)
        # return content_dict = {'category','text we scraped'}
        pass

    def filter_text(self, content_dict) -> None:
        # filter content by 'category'
        # return filtered_content_dict = {"category":"content"}
        pass