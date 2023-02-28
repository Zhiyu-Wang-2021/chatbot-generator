
import time
import bingGetAnswer.bing_azure_function_api as bingGetAnswer


# www.gosh.nhs.uk
# www.whitelodgemedicalpractice.nhs.uk - ok

# www.therossingtonpractice.nhs.uk
# www.oakleymedicalpractice.nhs.uk - ok

# several clinic
# www.clackmannanandkincardine.scot.nhs.uk
# www.theweardalepractice.nhs.uk
from webscraptool.tool import Tool

def get_dummy_answer(url):
    website_url = url
    time.sleep(5)
    return {
        'phone': ['020 8363 4156'],
        'openingtimepage':
            ['Monday\n08:00-18:30\nTuesday\n08:00-18:30\nWednesday\n08:00-18:30\nThursday\n08:00-18:30\nFriday\n08:00-18:30\n'],
        'contactpage': [{'postcode': 'EN2 6NL', 'address': 'Enfield\n105-109 Chase Side\n', 'contact': ''}],
        'appointment': ["appointment dummy data", 0]
    }



def get_answer(url):
    filter_keywords1 = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour']
    filter_keywords2 = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact']
    filter_keywords3 = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact']
    
    tool = Tool()
    tool.setup(url)
    openingtime_url = tool.filter_url(keywords=filter_keywords1, affixs=[], category='openingtime')
    address_url = tool.filter_url(keywords=filter_keywords2, affixs=[], category='address')
    phonenumber_url = tool.filter_url(keywords=filter_keywords3, affixs=[], category='phonenumber')
    openingtime_text = tool.scrape_text(openingtime_url)
    address_text = tool.scrape_text(address_url)
    phonenumber_text = tool.scrape_text(phonenumber_url)
    
    
    return {
        'phone': tool.filter_text(phonenumber_text)['filtered_text'],
        'openingtimepage':tool.filter_text(openingtime_text)['filtered_text'],
        'contactpage': tool.filter_text(address_text)['filtered_text'],
        'appointment': bingGetAnswer.get_bing_result(url, 'how do I make an appointment?')
    }


