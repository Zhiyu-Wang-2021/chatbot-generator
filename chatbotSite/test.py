# test for new code
from webscraptool.tool import Tool
def get_answer(url):
    filter_keywords = ['Opening Hour', 'Opening Times', 'Opening times', 'Opening hour', 'opening times', 'opening hour']
    tool = Tool()
    # tool.setup(url)
    # a = tool.filter_url(filter_keywords, [], 'openingtime')
    uuu = [{'category':'openingtimes','url':'https://www.whitelodgemedicalpractice.nhs.uk/practice-information/opening-hours/'}]
    return tool.scrape_text(uuu)

print(get_answer('www.whitelodgemedicalpractice.nhs.uk'))


