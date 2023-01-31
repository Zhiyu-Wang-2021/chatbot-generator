
import time




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
        'contactpage': [{'postcode': 'EN2 6NL', 'address': 'Enfield\n105-109 Chase Side\n', 'contact': ''}]
    }



def get_answer(url):
    filter_keywords1 = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour']
    filter_keywords2 = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact']
    filter_keywords3 = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact']
    
    tool = Tool()
    tool.setup(url)
    a = tool.filter_url(keywords=filter_keywords1, affixs=[], category='openingtime')
    b = tool.filter_url(keywords=filter_keywords2, affixs=[], category='address')
    c = tool.filter_url(keywords=filter_keywords3, affixs=[], category='phonenumber')
    aaa = tool.scrape_text(a)
    bbb = tool.scrape_text(b)
    ccc = tool.scrape_text(c)
    
    
    return {
        'phone': tool.filter_text(ccc)['filtered_text'],
        'openingtimepage':tool.filter_text(aaa)['filtered_text'],
        'contactpage': tool.filter_text(bbb)['filtered_text']
    }


