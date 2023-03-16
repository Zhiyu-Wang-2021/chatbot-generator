import webscraptool.match_content as match_content
from difflib import SequenceMatcher

# filter duplicates

def check_keyword_openinghour(title):
    keywords = ['Opening Timings', 'Opening Times', 'Opening Hours', 'Practice', 'Surgery', 'Medical', 'Hospital', 'Health']
    
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
    blacklists = []
    # e.g.blacklist=[{'postcode':'N1 9JP','address':'200 Pentonville Road'},{...},...]
    addr_filtered = []

    for addr in addr_list:
        postcode = match_content.match_postcode(addr['postcode'])
        # should not contains https:// as some times it will match something in url
        # e.g.https://feedback.camdenccg.nhs.uk/north-central-london/3be45ae8/
        # 3be45ae8 is matched as postcode
        # should not be a relocating message/referral page
        if postcode != '' and 'https://' not in addr['address']\
            and 'relocating' not in addr['address'] and 'relocation' not in addr['address']\
            and 'Relocation' not in addr['address'] and 'Referral' not in addr['address']:
            
            # first iteration
            if blacklists == []:
                print('first')
                blacklists.append({'postcode':postcode, 'address':addr['address']})
                addr_filtered.append(addr)
            
            else:
                print(postcode)
                end_flag = 0
                for blacklist in blacklists:
                    if blacklist['postcode'] == postcode:
                        # calculte text similarity for address when postcode are same
                        m = SequenceMatcher(None, addr['address'], blacklist['address'])
                        similarity_limit = 0.66666
                        similarity_ratio = m.ratio()

                        if similarity_ratio > similarity_limit:
                            end_flag = 1
                        elif blacklists[-1] == blacklist:
                            blacklists.append({'postcode':postcode, 'address':addr['address']})
                            addr_filtered.append(addr)
                    else:
                        # no duplicate until last element
                        if blacklists[-1] == blacklist:
                            blacklists.append({'postcode':postcode, 'address':addr['address']})
                            addr_filtered.append(addr)

                    if end_flag == 1:
                        break

    return addr_filtered


def openingtime(original):
    # ------------------------------------filter opening time-----------------------------------------------
    opening_hours_list = original
    title_blacklist = []

    opening_hours_filtered =['']
    print(original)
    for opening_hours in opening_hours_list:
        if opening_hours['title'] not in title_blacklist and check_keyword_openinghour(opening_hours['title']):
            
            if opening_hours['title'] == '':
                pass
            else:
                title_blacklist.append(opening_hours['title'])
                opening_hours_filtered.append(opening_hours)

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