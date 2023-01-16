import os
import sys
workingdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, workingdir)
import url_extractor
import get_addr
import get_openingtime
import get_phone_num
import os
import match_content
import json_formatter
import json
import filter_content

# www.gosh.nhs.uk
# www.whitelodgemedicalpractice.nhs.uk

# www.therossingtonpractice.nhs.uk
# www.oakleymedicalpractice.nhs.uk

# several clinic
# www.clackmannanandkincardine.scot.nhs.uk
# www.theweardalepractice.nhs.uk

# workingdir is needed as we may run the code from other folder
workingdir = os.path.dirname(os.path.abspath(__file__))
website_url = 'www.whitelodgemedicalpractice.nhs.uk'
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
filter_keywords = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour']
not_empty = url_extractor.filter_url(dir, filter_keywords)
if not_empty:
    url_extractor.get_text_from_filtered_url(workingdir + '/url_filtered_list.txt',workingdir + '/content.txt')
    get_openingtime.run(workingdir + '\\' + 'openingtimepage.json')



# get data from contact page
filter_keywords = ['Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact']
not_empty = url_extractor.filter_url(dir, filter_keywords)

if not_empty:
    url_extractor.get_text_from_filtered_url(workingdir + '/url_filtered_list.txt', workingdir + '/content.txt')
    get_addr.run(workingdir + '\\' + 'contactpage.json')
    get_openingtime.run(workingdir + '\\' +  'openingtimepage.json')
    # don't need to filter we can delete it later if phone number is already in address file
    get_phone_num.run(workingdir + '\\' + 'phone.json')
    



url_extractor.get_text('http://'+ website_url + '/')
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
        'phone':load1,
        'openingtimepage':load2,
        'contactpage':load3
}


with open(workingdir + '\\' + 'result.json', 'w') as f:
    json.dump(res, f)

# remove duplicates
filter_content.run()