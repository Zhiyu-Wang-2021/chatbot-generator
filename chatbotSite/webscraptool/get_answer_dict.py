
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
import threading
import os
import signal
import time


def timeout_handler():
    # send ctrl + c to prompt to terminate web scraping process
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    time.sleep(2)
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    time.sleep(2)
    # send to shutdown(for linux)
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(2)
    os.kill(os.getpid(), signal.SIGINT)

    


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

    filter_keywords1 = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour',\
                        'Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact','contact']
    filter_keywords2 = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact','contact','Contact us : University College London Hospitals NHS Foundation Trust']
    filter_keywords3 = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact','contact']
    
    # timer for method to terminate scraping process when it gets stuck(take too long) due to some error
    timer = threading.Timer(100.0, timeout_handler)
    timer.start()

    openingtime_url = []
    address_url = []
    phonenumber_url = []
    openingtime_text = {}
    address_text = {}
    phonenumber_text = {}

    try:
        tool = Tool()
        tool.setup(url)
        time.sleep(5)
        print('\n\n\nfiltering url...\n\n\n')
        openingtime_url = tool.filter_url(keywords=filter_keywords1, affixs=[], category='openingtime')
        address_url = tool.filter_url(keywords=filter_keywords2, affixs=[], category='address')
        phonenumber_url = tool.filter_url(keywords=filter_keywords3, affixs=[], category='phonenumber')

    finally:
        # if time is not out we need to cancel the timer
        timer.cancel()

    time.sleep(3)
    print('\n\n\nscraping text...\n\n\n')

    # if the process go over 30 sec then stop text scraping process 
    timer = threading.Timer(30.0, timeout_handler)
    timer.start()
    try:
        openingtime_text = tool.scrape_text(openingtime_url)
        time.sleep(1)
    finally:
        timer.cancel()

    timer = threading.Timer(30.0, timeout_handler)
    timer.start()
    try:
        address_text = tool.scrape_text(address_url)
        time.sleep(1)
    finally:
        timer.cancel()

    timer = threading.Timer(30.0, timeout_handler)
    timer.start()
    try:
        phonenumber_text = tool.scrape_text(phonenumber_url)
        time.sleep(1)
    finally:
        timer.cancel()


    time.sleep(3)
    print('\n\n\nfiltering text...\n\n\n')

    max_connection_attempt = 10
    connection_attempt = 0
    filtered_phonenumber_text = []
    filtered_openingtime_text = []
    filtered_address_text = []
    appointment_text = []
    # try to reconnect to ibm if failed connection due to internet problem
    while(connection_attempt < max_connection_attempt):
        try:
            filtered_phonenumber_text = tool.filter_text(phonenumber_text)['filtered_text']
            filtered_openingtime_text = tool.filter_text(openingtime_text)['filtered_text']
            filtered_address_text = tool.filter_text(address_text)['filtered_text']
            connection_attempt = 10
            break
        except Exception as e:
            print(e)
            print('an error occur, try to restart scraping process...')
            time.sleep(1)
            connection_attempt = connection_attempt + 1

    connection_attempt = 0
    # try to reconnect to ibm if failed connection due to internet problem
    while(connection_attempt < max_connection_attempt):
        try:
            appointment_text = bingGetAnswer.get_bing_result(url, 'how to make an appointment?')
            connection_attempt = 10
            break
        except Exception as e:
            print(e)
            print('an error occur, try to restart bing search process...')
            time.sleep(1)
            connection_attempt = connection_attempt + 1

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
    print(str(openingtime_url))
    return {
        'phone': filtered_phonenumber_text,
        'openingtimepage':filtered_openingtime_text,
        'contactpage': filtered_address_text,
        'appointment': appointment_text
    }


