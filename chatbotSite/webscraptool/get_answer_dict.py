import json
import os, sys
import time

import webscraptool.get_addr as get_addr
import webscraptool.get_openingtime as get_openingtime
import webscraptool.get_phone_num as get_phone_num
import webscraptool.json_formatter as json_formatter
import webscraptool.url_extractor as url_extractor
import webscraptool.filter_content as filter_content

workingdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, workingdir)


# www.gosh.nhs.uk
# www.whitelodgemedicalpractice.nhs.uk - ok

# www.therossingtonpractice.nhs.uk
# www.oakleymedicalpractice.nhs.uk - ok

# several clinic
# www.clackmannanandkincardine.scot.nhs.uk
# www.theweardalepractice.nhs.uk


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
    website_url = url
    dir = workingdir + '\\url_crawler\\outputfile.json'
    # about us/contact us/opening hour/opening times

    url_extractor.crawl(website_url)
    url_extractor.extract_url(dir)

    # remove previous result
    if os.path.exists(workingdir + '\\' + 'phone.json'):
        os.remove(workingdir + '\\' + 'phone.json')

    if os.path.exists(workingdir + '\\' + 'contactpage.json'):
        os.remove(workingdir + '\\' + 'contactpage.json')

    if os.path.exists(workingdir + '\\' + 'openingtimepage.json'):
        os.remove(workingdir + '\\' + 'openingtimepage.json')

    # create outputfile
    f1 = open(workingdir + '\\' + 'phone.json', 'x', encoding='utf-8')
    f2 = open(workingdir + '\\' + 'contactpage.json', 'x', encoding='utf-8')
    f3 = open(workingdir + '\\' + 'openingtimepage.json', 'x', encoding='utf-8')

    f1 = open(workingdir + '\\' + 'phone.json', 'r', encoding='utf-8')
    f2 = open(workingdir + '\\' + 'contactpage.json', 'r', encoding='utf-8')
    f3 = open(workingdir + '\\' + 'openingtimepage.json', 'r', encoding='utf-8')

    # output things extract from different webpage to corresponding txt file

    # get data from opening hour page
    filter_keywords = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times',
                       'opening hour']
    not_empty = url_extractor.filter_url(dir, filter_keywords)
    if not_empty:
        url_extractor.get_text_from_filtered_url(workingdir + '/url_filtered_list.txt', workingdir + '/content.txt')
        get_openingtime.run(workingdir + '\\' + 'openingtimepage.json')

    # get data from contact page
    filter_keywords = ['Contact us', 'Contact Us', 'contact us', 'Contact-us', 'Contact-Us', 'contact-us', 'Contact']
    not_empty = url_extractor.filter_url(dir, filter_keywords)

    if not_empty:
        url_extractor.get_text_from_filtered_url(workingdir + '/url_filtered_list.txt', workingdir + '/content.txt')
        get_addr.run(workingdir + '\\' + 'contactpage.json')
        get_openingtime.run(workingdir + '\\' + 'openingtimepage.json')
        # don't need to filter we can delete it later if phone number is already in address file
        get_phone_num.run(workingdir + '\\' + 'phone.json')

    url_extractor.get_text('http://' + website_url + '/')
    get_openingtime.run(workingdir + '\\' + 'openingtimepage.json')
    get_phone_num.run(workingdir + '\\' + 'phone.json')
    get_addr.run(workingdir + '\\' + 'contactpage.json')

    # concat lists in json file together
    json_formatter.concat_json(workingdir + '\\' + 'openingtimepage.json')
    json_formatter.concat_json(workingdir + '\\' + 'phone.json')
    json_formatter.concat_json(workingdir + '\\' + 'contactpage.json')

    file1 = open(workingdir + '\\' + 'phone.json')
    file2 = open(workingdir + '\\' + 'openingtimepage.json')
    file3 = open(workingdir + '\\' + 'contactpage.json')
    load1 = json.load(file1)
    load2 = json.load(file2)
    load3 = json.load(file3)

    res = {
        'phone': load1,
        'openingtimepage': load2,
        'contactpage': load3
    }

    with open(workingdir + '\\' + 'result.json', 'w') as f:
        json.dump(res, f)

    # remove duplicates
    res = filter_content.run()

    print(res)

    return res


# get_answer('www.therossingtonpractice.nhs.uk')

