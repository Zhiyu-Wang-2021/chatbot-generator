from bingGetAnswer.bing_azure_function_api import get_bing_result
domain_url = 'www.whitelodgemedicalpractice.nhs.uk'
question = 'how to make an appointment?'
print(get_bing_result(domain_url, question))

