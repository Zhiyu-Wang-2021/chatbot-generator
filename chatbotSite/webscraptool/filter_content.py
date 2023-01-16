import json
import os
import sys
workingdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, workingdir)
import match_content

def run():
    # -----------------------------filter addr by postcode--------------------------------------------
    # different addr has different postcode so filter addr by its postcode
    result = open(workingdir + '\\' + 'result.json', 'r', encoding='utf-8')
    result_list = json.load(result)
    addr_list = result_list['contactpage']
    postcodes = []
    addr_filtered = []

    print('\n\n\n\norg:',addr_list,'\n\n\n\n')

    for addr in addr_list:
        postcode = match_content.match_postcode(addr['postcode'])

        if postcode != ''  and postcode not in postcodes:
            postcodes.append(match_content.match_postcode(addr['postcode']))
            addr_filtered.append(addr)

    print('filtered:', addr_filtered)


    # ------------------------------------filter opening time-----------------------------------------------
    # Load the JSON file
    with open(workingdir + '\\' + 'result.json', 'r') as f:
        data = json.load(f)

    # Extract the opening hours from the 'time' field
    opening_hours = [item['time'] for item in data['openingtimepage'] if item['title'] == 'Opening Hours']

    # Remove duplicates from the list
    opening_hours = list(set(opening_hours))

    # Put the opening_hours together
    print(opening_hours)

    # ------------------------------------filter phonenum-----------------------------------------------
    phonenum_list = result_list['phone']
    filter_phonenum = []

    for phone_num in phonenum_list:
        if phone_num['num'] not in filter_phonenum:
            filter_phonenum.append(phone_num['num'])
    print(filter_phonenum)

    # output everything to result_filtered.json
    res = {
            'phone':filter_phonenum,
            'openingtimepage':opening_hours,
            'contactpage':addr_filtered
    }
    with open(workingdir + '\\' + 'result_filtered.json', 'w') as f:
        json.dump(res, f)
        
    return res

