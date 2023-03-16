# get address workflow:
# 1.get the position of postcode in the content.txt
# 2.1 try to get address before or after postcode as the address is always next to postcode
# 2.2 postcode is always at the end of the address and the first line will be street/road/side
# 2.3 read until keyword is detected
# keyword:
# street/road/side/Court/Place/Avenue/Lane/Common/Hall/Hill/Hoo/Gardens/College/Drive/Ward/Close/Centre/Oval/Grove
# practice/Surgery/Medical/Hospital/Heath


# check post code    
import webscraptool.match_content as match_content
from webscraptool.tokenizer import tokenization

def run(txt):
    # ibm nlu extract every phrases and sentences
    response = tokenization(txt)
    if response == '':
        return []

    # 1.try to locate the index of postcode
    sentences_dict = response
    cur_index = 0
    start_pos = [] # starting position of postcode

    for d in sentences_dict['syntax']['sentences']:
        postcode =  match_content.match_postcode(str(d['text']))
        if postcode:
            print(str(d['text']))
            start_pos.append(cur_index)        

        cur_index = cur_index + 1


    # 2.read everything before postcode until keyword is detected
    # keyword from about 100 nhs trust practice:
    # street/road/side/Court/Place/Avenue/Lane/Common/Hall/Hill/Hoo/Gardens/College/Drive/Ward/Close/Centre/Oval/Grove
    # practice/Surgery/Medical/Hospital/Health

    # check if keywords exists
    # True:in / False:not in
    def check_keywords(text):    
        keywords = [
                    'Street', 'Road', 'Side', 'Court', 'Place', 
                    'Avenue', 'Lane', 'Common', 'Hall', 'Hill', 
                    'Hoo', 'Gardens', 'College', 'Drive', 'Ward',
                    'Close', 'Centre', 'Oval', 'Grove',
                    'Practice', 'Surgery', 'Medical', 'Hospital', 'Health'
                    ]
        for keyword in keywords:
            if keyword in text:
                return True
        return False

    # a list of address and postcode store in dictionary
    addr_dict = [] 
    print('start:')
    print(start_pos)
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
        
        # how many item we have already checked
        item_checked = 0
        item_checked_limit = 4
        while(True):
            if cur_pos >= 0:
                cur_text = sentences_dict['syntax']['sentences'][cur_pos]['text']

            if check_keywords(cur_text):
                # print('keyword detected!!')
                addr_text = addr_text + cur_text  + '\n'

                # we need to check another more sentence just in case they also put the name of hospital in
                cur_text = sentences_dict['syntax']['sentences'][cur_pos-1]['text']

                # make sure no copyright text so no '©' sign
                if check_keywords(cur_text) and '©' not in cur_text:
                    end_flag = True
                    addr_text = addr_text + cur_text  + '\n'
                else:
                    end_flag = True
                    break
            # remove if it is a postcode
            elif match_content.match_postcode(cur_text) and cur_pos >= 0:
                item_checked = item_checked + 1
                cur_pos = cur_pos - 1
            # we already checked enough item,so we do not go further
            elif item_checked > item_checked_limit :
                # the address should be here with postcode but the address does not contain a keyword we have
                if len(sentences_dict['syntax']['sentences'][pos]['text']) > 12:
                    addr_text = sentences_dict['syntax']['sentences'][pos]['text']
                # make sure not out of range
                elif pos > 1:
                    addr_text = sentences_dict['syntax']['sentences'][pos]['text'] + \
                                sentences_dict['syntax']['sentences'][pos-1]['text'] + \
                                sentences_dict['syntax']['sentences'][pos-2]['text']
                cur_pos = 0
                end_flag = True
                break   
            elif cur_pos >= 0:
                item_checked = item_checked + 1
                addr_text = addr_text + cur_text  + '\n'
                cur_pos = cur_pos - 1
            # if we did not detect any keyword even till the end of the page
            elif cur_pos < 0:
                # does not only contains postcode in this sentence
                # the address should be here with postcode but the address does not contain a keyword we have
                if len(sentences_dict['syntax']['sentences'][pos]['text']) > 12:
                    addr_text = sentences_dict['syntax']['sentences'][pos]['text']
                # make sure not out of range
                elif pos > 1:
                    addr_text = sentences_dict['syntax']['sentences'][pos]['text'] + \
                                sentences_dict['syntax']['sentences'][pos-1]['text'] + \
                                sentences_dict['syntax']['sentences'][pos-2]['text']
                
                cur_pos = 0
                end_flag = True
                break               
            
            #   if everything is finished then quit
            if end_flag :
                break

                
        print(pos)
        addr_dict.append({
                'postcode':sentences_dict['syntax']['sentences'][pos]['text'], # the sentence contains postcode
                'address':addr_text,
                'contact':contact_text
        })

    # output to json if dict not empty


    return addr_dict