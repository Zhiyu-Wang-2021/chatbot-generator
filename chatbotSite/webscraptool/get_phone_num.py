# get phone number
# work flow:
# 1.read sentence from nlu
# 2.match and check if phone number exists in text then try to get one sentences/word before
# critical situation: have multiple places of the practice(differet number for different location)
# https://www.dorkingmedicalpractice.nhs.uk/practice-information/contact-us/
# possible work around:do it in get_addr just find 4 phrases/sentences after 

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SyntaxOptions, SyntaxOptionsTokens
# check phone number and postcode
import webscraptool.match_content as match_content

import env

def run(txt):
    # do not accept empty txt
    if txt == '':
        return []
    # 1.ibm nlu extract every phrases and sentences
    apikey = env.ibm_api_key
    apiurl = env.ibm_api_endpoint
    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(apiurl)



    # only get sentences
    response = natural_language_understanding.analyze(
        text=txt,
        features=Features(
        syntax=SyntaxOptions(
            sentences=True,
            ))).get_result()


    # 2.match and check if phone number exists in text then try to get one sentences/word before
    dict = response
    d_pre = {} # contain previous iterated dict 
    data_extracted = ''
    cur_index = 0
    phone_nums_dict = []

    for d in dict['syntax']['sentences']:
        # only phone number and related content filter out postcode
        if match_content.match_phonenumber(d['text']): 
            # remove whitespace for api to recognize
            # text_no_whitespace = str(d_pre['text']).replace(' ','')

            # if validation.is_valid_postcode(text_no_whitespace):
            if match_content.match_postcode(d_pre['text']):
                phone_nums_dict.append({
                    'title':'',
                    'num':d['text'],
            })
               # data_extracted = data_extracted + d['text'] + '\n'
            else:
                phone_nums_dict.append({
                    'title': d_pre['text'],
                    'num':d['text'],
                })
               # data_extracted = data_extracted + d_pre['text'] + '\n' + d['text'] + '\n'
        d_pre = d
        cur_index = cur_index + 1
    # f.write('\n')
    # f.write(data_extracted)
    # if dict not empty write to json
    return phone_nums_dict

