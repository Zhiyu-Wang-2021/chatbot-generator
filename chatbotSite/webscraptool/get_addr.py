# get address workflow:
# 1.get the position of postcode in the content.txt
# 2.1try to get address before or after postcode as the address is always next to postcode
# 2.2postcode is always at the end of the address and the first line will be street/road/side
# 2.3read until keyword is detected
# keyword:
# street/road/side/Court/Place/Avenue/Lane/Common/Hall/Hill/Hoo/Gardens/College/Drive/Ward/Close/Centre/Oval/Grove
# practice/Surgery/Medical/Hospital/Heath


from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import EntitiesOptions,Features, KeywordsOptions, SyntaxOptions, SyntaxOptionsTokens
# check post code    
import webscraptool.match_content as match_content
import env

def run(txt):
    # do not accept empty txt
    if txt == '':
        return []
    # ibm nlu extract every phrases and sentences
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

    # 1.try to locate the index of postcode
    sentences_dict = response
    cur_index = 0
    start_pos = [] # starting position of postcode

    for d in sentences_dict['syntax']['sentences']:
        postcode =  match_content.match_postcode(str(d['text']))
        text_no_whitespace = str(d['text']).replace(' ', '')

    #    if validation.is_valid_postcode(text_no_whitespace):
    #        start_pos.append(cur_index)
    #    elif postcode and validation.is_valid_postcode(postcode.replace(' ', '')):
    #        start_pos.append(cur_index)
        if postcode:
            start_pos.append(cur_index)        

        cur_index = cur_index + 1


    # 2.read everything before postcode until keyword is detected
    # keyword from about 100 nhs trust practice:
    # street/road/side/Court/Place/Avenue/Lane/Common/Hall/Hill/Hoo/Gardens/College/Drive/Ward/Close/Centre/Oval/Grove
    # practice/Surgery/Medical/Hospital/Health

    # check if keywords exists
    # True:in/False:not in
    def check_keywords(text):    
        keywords = [
                    'Street', 'Road', 'Side', 'Court', 'Place', 
                    'Avenue', 'Lane', 'Common', 'Hall', 'Hill', 
                    'Hoo', 'Gardens', 'College', 'Drive', 'Ward',
                    'Close', 'Centre', 'Oval', 'Grove',
                    'Practice', 'Surgery', 'Medical', 'Hospital', 'Health'
                    ]
        for keyword in keywords:
            if keyword in cur_text:
                return True
        return False

    # a list of address and postcode store in dictionary
    addr_dict = [] 

    for pos in start_pos:
        cur_pos = pos
        addr_text = ''
        contact_text = ''
        end_flag = False

        # check if they put telephone number at the end of the location
        for i in range(1, 5):
            # usually in format tel:xxxxxx out of hour:xxxxxxx
            # if not at the end of the page then go forward 5 phrases to check if phone number exists 
            if len(sentences_dict['syntax']['sentences']) -1 >= cur_pos + i and\
                match_content.match_phonenumber(sentences_dict['syntax']['sentences'][cur_pos + i]['text']):

                # also get text one word before phonenum in order to get tag(e.g. tel:/out of hour:)
                contact_text = contact_text + sentences_dict['syntax']['sentences'][cur_pos + i - 1]['text']\
                            + '\n' + sentences_dict['syntax']['sentences'][cur_pos + i]['text'] + '\n'

        while(True):
            cur_text = sentences_dict['syntax']['sentences'][cur_pos]['text']
            # print(cur_text)

            if check_keywords(cur_text):
                # print('keyword detected!!')
                addr_text = addr_text + cur_text  + '\n'

                # we need to check another more sentence just in case they also put the name of hospital in
                cur_text = sentences_dict['syntax']['sentences'][cur_pos-1]['text']

                if check_keywords(cur_text):
                    end_flag = True
                    addr_text = addr_text + cur_text  + '\n'
                else:
                    end_flag = True
                    break
            # remove if it is a postcode
            # elif validation.is_valid_postcode(cur_text.replace(' ','')):
            elif match_content.match_postcode(cur_text):
                cur_pos = cur_pos - 1
            else:
                addr_text = addr_text + cur_text  + '\n'
                cur_pos = cur_pos - 1
            
            #   if everything is finished then quit
            if end_flag :
                break

                

        addr_dict.append({
                'postcode':sentences_dict['syntax']['sentences'][pos]['text'],
                'address':addr_text,
                'contact':contact_text
        })

    # output to json if dict not empty


        return addr_dict
#    for d in addr_dict:
#        f.write(d['address'] + d['postcode'] + '\n' + d['contact'])
#        print(d['address'],d['postcode'],'\n',d['contact'])
#        print('------------------------\n')

