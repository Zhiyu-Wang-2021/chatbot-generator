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
    opening_hours_list = original
    title_blacklist = []
    opening_hours_filtered =['']

    for opening_hours in opening_hours_list:
        if opening_hours['title'] not in title_blacklist:
            title_blacklist.append(opening_hours['title'])
            opening_hours_filtered[0] = opening_hours_filtered[0] + '\n' + opening_hours['title'] +\
            opening_hours['time']

    # Put the opening_hours together

    return opening_hours_filtered

def phonenumber(original):
    # ------------------------------------filter phonenum-----------------------------------------------
    phonenum_list = original
    filter_phonenum = []

    for phone_num in phonenum_list:
        if phone_num['num'] not in filter_phonenum:
            filter_phonenum.append(phone_num['num'])

        
    return filter_phonenum

