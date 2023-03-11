# 1. ibm nlu extract every phrases and sentences
# 2. find the location where a time(e.g.18:00) is given then match one word/sentence before the time
# 3. read before the first time period until keyword is detected as there is always a title on the front
# this part will handle the problem of multiple surgery and filter out Consultation Consulting
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SyntaxOptions, SyntaxOptionsTokens
# check phone number and postcode
import webscraptool.match_content as match_content

import env

def run(txt):

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


    # 2.match one word/sentence before the time
    dict = response
    d_pre = {} # contain previous iterated dict 
    data_extracted = ''
    cur_index = 0
    starting_pos = []

    for d in dict['syntax']['sentences']:
        
        try:
            # some do not have 'text' attribute
            match = match_content.match_time(str(d['text']))

            if match: 
                starting_pos.append(cur_index)
                data_extracted = data_extracted + d_pre['text'] + '\n' + d['text'] + '\n'
        except:
            pass
        d_pre = d
        cur_index = cur_index + 1
    # print(data_extracted)

    # 3.1 locate the first time period(e.g. Monday) and separate them into different list
    # using starting position to locate the title
    # [67, 69, 71, 73, 75, 84, 86, 88, 90, 92, 100, 102, 108]
    # pattern:67+2 69+2 71+2 73+2 75  ! starting a new series 84, 86....


    group_starting_pos = []  # the starting of a group of date
    split_group_pos = []

    # locate the starting pos of each sequence
    for i in range(0, len(starting_pos)):
        if i - 1 >= 0:
            if starting_pos[i] - starting_pos[i - 1] == 2 or starting_pos[i] - starting_pos[i - 1] == 1:
                pass
            else:
                group_starting_pos.append(i)
        # first starting pos
        else:
            group_starting_pos.append(i)
    # print(starting_pos)
    # print(group_starting_pos)

    # split the list by the starting pos
    for i in range(0, len(group_starting_pos)):
        # only one sequence of time
        if len(group_starting_pos) == 1:
            split_group_pos.append(starting_pos)
            break

        if i + 1 < len(group_starting_pos):
            split_group_pos.append(starting_pos[group_starting_pos[i]:group_starting_pos[i + 1]])
        # end of the list
        elif i + 1 == len(group_starting_pos):
            split_group_pos.append(starting_pos[group_starting_pos[i]:])

    # print(split_group_pos)


    # 3.2 read until keyword is detected as there is always a title on the front and filter out the unwilling content
    keyword = ['Opening Times', 'Opening Hours', 'Practice', 'Surgery', 'Medical', 'Hospital', 'Health']
    disallow = ['Consultation', 'Consulting', 'Dr', 'Nurse', 'ANP', 'Assistant']

    # filter content by keyword
    def check_disallow(pos):
        #input the starting pos of group of time
        end_flag = 0
        count = 0
        while(True):
            count = count + 1

            if end_flag == 1:
                break

            # first recognize title containing consultation time(filter it)
            for x in range(0, len(disallow)):
                if disallow[x] in dict['syntax']['sentences'][pos - count]['text']:
                    return True

            # if no disallow check if the title contains keywords()
            for x in range(0, len(keyword)):
                if keyword[x] in dict['syntax']['sentences'][pos - count]['text']:
                    end_flag = 1
                    break
        
        # retun the position of the title if no disallow keyword recognized
        return pos - count + 1
                        
    filtered_group = [] # after filteration by disallow keyword
    title_pos = [] # postion of the title

    for i in range(0, len(split_group_pos)):
        if type(check_disallow(split_group_pos[i][0])) is int:
            title_pos.append(check_disallow(split_group_pos[i][0]))
            filtered_group.append(split_group_pos[i])

    # print(filtered_group)
    print(title_pos)
    print(filtered_group)
    ## print every thing
    cur_index = 0
    openingtime_dict = []


    print('--------opening hour---------------')
    for sequence_pos in filtered_group:
        title = ''
        time_sequence = ''

        # first iteration of for loop
        title = dict['syntax']['sentences'][title_pos[cur_index]]['text']

        # same title name which means they belongs to same surgery
        # it happens in situation like this(closed will break the pattern)       
        # Monday	8:00-18:00	8:00-14:00
        # Tuesday	closed
        # Wednesday	8:00-12:00	8:00-18:00

        # read time period from start to end
        for x in range(sequence_pos[0] - 1, sequence_pos[-1] + 1):
            time_sequence = time_sequence + dict['syntax']['sentences'][x]['text'] + '\n'

    
        # also do not do title read when the time period is given in a sentence
        # only one is in the list but really long which means it is a sentence
        if len(sequence_pos) == 1 and len(time_sequence)>45:
            openingtime_dict.append({
                    'title':'',
                    'time':time_sequence,
            })
            print('\n' + time_sequence)
        else:
            openingtime_dict.append({
                    'title':title,
                    'time':time_sequence,
            })
            print(title + '\n' + time_sequence)

        cur_index = cur_index + 1

    return openingtime_dict

    
