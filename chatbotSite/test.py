from webscraptool.tool import Tool


# keyword list for general info page
filter_keywords1 = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour',\
                        'Contact us', 'Contact Us', 'contact us', 'Contact-us','Contact-Us','contact-us', 'Contact','contact']
tool = Tool()

print('\n\n\nfiltering url...\n\n\n')
#general_info_url = tool.crawl_url_by_dictionary('general_info')
#general_info_url = tool.filter_url(keywords=filter_keywords1)
tool.setup('127.0.0.1:8000')
general_info_url = [{'url':'http://127.0.0.1:8000/'}]
print(general_info_url)
text = tool.scrape_text(general_info_url)

print(text)