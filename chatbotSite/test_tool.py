from webscraptool.tool import Tool
from webscraptool.get_phone_num import run
tool = Tool()
a = [{'title': '', 'url': 'https://www.gosh.nhs.uk', 'keyword': ''}, {'url':'https://www.gosh.nhs.uk/about-us/contact-us/'}]
t = tool.scrape_text(a)
#filtered_address_text = tool.filter_text(t,category='address')['filtered_text']
#print(filtered_address_text)
print(len(t['text']))
print('\n\n\n')
a = run(str(t['text'][1]['text']))
print(a)

