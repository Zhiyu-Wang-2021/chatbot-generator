import json
import os

import get_addr
import get_openingtime
import get_phone_num
import json_formatter
import url_extractor

# www.gosh.nhs.uk
# www.whitelodgemedicalpractice.nhs.uk

# www.therossingtonpractice.nhs.uk
# www.oakleymedicalpractice.nhs.uk

# several clinic
# www.clackmannanandkincardine.scot.nhs.uk
# www.theweardalepractice.nhs.uk


website_url = 'www.therossingtonpractice.nhs.uk'
dir = './url_crawler/outputfile.json'
# about us/contact us/opening hour/opening times


url_extractor.crawl(website_url)
url_extractor.extract_url(dir)


# remove previous result
if os.path.exists('phone.json'):
    os.remove('phone.json')

if os.path.exists('contactpage.json'):
    os.remove('contactpage.json')

if os.path.exists('openingtimepage.json'):
    os.remove('openingtimepage.json')

# create outputfile
# f1 = open('phone.json', 'x', encoding='utf-8')
# f2 = open('contactpage.json', 'x', encoding='utf-8')
# f3 = open('openingtimepage.json', 'x', encoding='utf-8')

f1 = open('phone.json', 'r', encoding='utf-8')
f2 = open('contactpage.json', 'r', encoding='utf-8')
f3 = open('openingtimepage.json', 'r', encoding='utf-8')


# output things extract from different webpage to corresponding txt file

# get data from opening hour page
filter_keywords = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour']
not_empty = url_extractor.filter_url(dir, filter_keywords)
if not_empty:
    url_extractor.get_text_from_filtered_url('./url_filtered_list.txt','./content.txt')
    get_openingtime.run('openingtimepage.json')



# get data from contact page
filter_keywords = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact']
not_empty = url_extractor.filter_url(dir, filter_keywords)

if not_empty:
    url_extractor.get_text_from_filtered_url('./url_filtered_list.txt','./content.txt')
    get_addr.run('contactpage.json')
    get_openingtime.run('openingtimepage.json')
    # don't need to filter we can delete it later if phone number is already in address file
    get_phone_num.run('phone.json')


url_extractor.get_text('http://'+ website_url + '/')
get_openingtime.run('openingtimepage.json')
get_phone_num.run('phone.json')
get_addr.run('contactpage.json')


# concat lists in json file together
json_formatter.concat_json('openingtimepage.json')
json_formatter.concat_json('phone.json')
json_formatter.concat_json('contactpage.json')

file1 = open('phone.json')
file2 = open('openingtimepage.json')
file3 = open('contactpage.json')
load1 = json.load(file1)
load2 = json.load(file2)
load3 = json.load(file3)

res = {
    'phone':load1,
    'openingtimepage':load2,
    'contactpage':load3
}

print(res)

with open('result.json', 'w') as f:
    json.dump(res, f)