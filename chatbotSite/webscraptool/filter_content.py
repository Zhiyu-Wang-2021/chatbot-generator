import webscraptool.match_content as match_content
def check_keyword_openinghour(title):
    keywords = ['Opening Times', 'Opening Hours', 'Practice', 'Surgery', 'Medical', 'Hospital', 'Health']
    
    if title == '':
        return True
    
    for keyword in keywords:
        if keyword in title:
            return True
    
    return False

def addr(original):
    # -----------------------------filter addr by postcode--------------------------------------------
    # different addr has different postcode so filter addr by its postcode
    addr_list = original
    postcodes = []
    addr_filtered = []

    for addr in addr_list:
        postcode = match_content.match_postcode(addr['postcode'])

        if postcode != ''  and postcode not in postcodes and 'https://' not in addr['address']:
            postcodes.append(match_content.match_postcode(addr['postcode']))
            addr_filtered.append(addr)

    return addr_filtered


def openingtime(original):
    # ------------------------------------filter opening time-----------------------------------------------
    # Load the JSON file
    opening_hours_list = original
    title_blacklist = []

    opening_hours_filtered =['']
    print(original)
    for opening_hours in opening_hours_list:
        if opening_hours['title'] not in title_blacklist and check_keyword_openinghour(opening_hours['title']):
            
            if opening_hours['title'] == '':
                matches = match_content.match_time_it(opening_hours['title'])
                count_match = 0

                for match in matches:
                    count_match = count_match + 1

                # should not contains https:// as some times it will match something in url
                # e.g.https://feedback.camdenccg.nhs.uk/north-central-london/3be45ae8/
                if count_match>2 and 'https://' not in opening_hours['title']:  
                    opening_hours_filtered[0] = opening_hours_filtered[0] + '\n' + opening_hours['title'] +\
                    opening_hours['time']
            else:
                title_blacklist.append(opening_hours['title'])
                opening_hours_filtered[0] = opening_hours_filtered[0] + '\n' + opening_hours['title'] +\
                opening_hours['time']

    # Put the opening_hours together

    return opening_hours_filtered

def phonenumber(original):
    # ------------------------------------filter phonenum-----------------------------------------------
    phonenum_list = original
    filter_phonenum = [] # phone number and related text already get
    blacklist_phonenum = [] # phone number(only) already get 

    for phone_num in phonenum_list:
        cur_phonenum = match_content.match_phonenumber_content(phone_num['num'])
        success_flag = 1

        for blacklist in blacklist_phonenum:
            print(blacklist)
            print(cur_phonenum)
            # not the same e.g.020 7405 9200
            # not the same substring e.g. 020 7405 9200,+44 (0)20 7405 9200
            if (cur_phonenum.find(blacklist) != -1 or blacklist.find(cur_phonenum) != -1)\
                or (cur_phonenum.find(blacklist[1:]) != -1 or blacklist.find(cur_phonenum[1:]) != -1):
                success_flag = 0

        if success_flag == 1:
            filter_phonenum.append(phone_num['num'])
            blacklist_phonenum.append(cur_phonenum)

    return filter_phonenum