from abc import ABC, abstractmethod


class Abstract_Tool(ABC):
    @abstractmethod
    def __init__(self) -> None:
        # self.mainsite
        # self.url_dict
        
        pass

    def setup(self, link) -> None:
        # crawl all the url -> store all url and their title in a dict
        # self.url_dict = [{title:title, url:url},...]
        # store main site in self.main_site
        # link - format of input:www.{nhs_trust_name}.nhs.uk
        # (just do not include 'http:// /')
        pass

    def crawl_url_by_dictionary(self, dict_name):
        # check if the location in dictionary exists in the given domain
        # this can crawl url without using scrapy as it sometimes 'miss' information
        # did not find a way to fix it so this function can be a complement part for webscraping and filtering url
        # select which dict to use by dict_name
        pass

    def filter_url(self, keywords) -> list:
        # filter out url with specific keyword in title or specific affix
        # store filtered url in a dict 'self.filtered_url'
        # e.g. if we need to get address the category should be filled in as 'address'
        # all the dict in the list should be as follow
        # [{'title','link','keyword'},{},....]
        # all keywords should be as follow
        # ['keyword1', 'keyword2',.....]
        pass

    def scrape_text(self, filtered_url) -> dict:
        # return empty if url is not filtered
        # scrape text from 'self.filtered_url' store as dictionary(content_dict)
        # return content_dict = {'text':'text from page 1'},{'text':'text from page 2'},...
        pass

    def filter_text(self, content_dict, category) -> dict:
        # filter content by 'category'
        # remove duplication
        # return filtered_content_dict = {"content"}
        pass