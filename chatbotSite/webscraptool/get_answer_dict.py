
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
import time

    


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

    # keyword list for general info page
    filter_keywords1 = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour',\
                        'Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact','contact']
    time.sleep(5)
    tool = Tool()
    tool.setup(url)
    print(tool.mainsite)
    print(type(tool.mainsite))
    time.sleep(5)
    print('\n\n\nfiltering url...\n\n\n')
    general_info_url = tool.crawl_url_by_dictionary('general_info')
    general_info_url += tool.filter_url(keywords=filter_keywords1)

    time.sleep(3)
    print('\n\n\nscraping text...\n\n\n')


    openingtime_text = tool.scrape_text(general_info_url)
    time.sleep(1)
    address_text = tool.scrape_text(general_info_url)
    time.sleep(1)
    phonenumber_text = tool.scrape_text(general_info_url)
    time.sleep(1)


    time.sleep(3)
    print('\n\n\nfiltering text...\n\n\n')

    filtered_phonenumber_text = tool.filter_text(phonenumber_text, category='phonenumber')['filtered_text']
    filtered_openingtime_text = tool.filter_text(openingtime_text, category='openingtime')['filtered_text']
    filtered_address_text = tool.filter_text(address_text,category='address')['filtered_text']


    appointment_text = bingGetAnswer.get_bing_result(url, 'how to make an appointment?')

    if len(appointment_text) == 0:
        appointment_text = ['Sorry, I am having difficulties finding related information on our website to answer your question.', 0]
    
    print('==================This is the answer=======================')
    print(str({
        'phone': filtered_phonenumber_text,
        'openingtimepage':filtered_openingtime_text,
        'contactpage': filtered_address_text,
        'appointment': appointment_text
    }))
    print('================================this is the filtered url')
    print(str(general_info_url))

    return {
        'phone': filtered_phonenumber_text,
        'openingtimepage':filtered_openingtime_text,
        'contactpage': filtered_address_text,
        'appointment': appointment_text
    }


