import json
import os
import sys
workingdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, workingdir)
import match_content

def addr(original):
    # -----------------------------filter addr by postcode--------------------------------------------
    # different addr has different postcode so filter addr by its postcode
    addr_list = original
    postcodes = []
    addr_filtered = []

    for addr in addr_list:
        postcode = match_content.match_postcode(addr['postcode'])

        if postcode != ''  and postcode not in postcodes:
            postcodes.append(match_content.match_postcode(addr['postcode']))
            addr_filtered.append(addr)

    return addr_filtered


def openingtime(original):
    # ------------------------------------filter opening time-----------------------------------------------
    # Load the JSON file
    data = original
    print(original)

    # Extract the opening hours from the 'time' field
    opening_hours = [item['time'] for item in data if item['title'] == 'Opening Hours']

    # Remove duplicates from the list
    opening_hours = list(set(opening_hours))

    # Put the opening_hours together

    return opening_hours

def phonenumber(original):
    # ------------------------------------filter phonenum-----------------------------------------------
    phonenum_list = original
    filter_phonenum = []

    for phone_num in phonenum_list:
        if phone_num['num'] not in filter_phonenum:
            filter_phonenum.append(phone_num['num'])

        
    return filter_phonenum

