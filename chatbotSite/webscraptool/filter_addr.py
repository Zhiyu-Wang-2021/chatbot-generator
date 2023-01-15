import json
import match_content

result = open('result.json', 'r', encoding='utf-8')
addr_list = json.load(result)['contactpage']
postcodes = []
addr_filtered = []

print('\n\n\n\norg:',addr_list,'\n\n\n\n')

for addr in addr_list:
    postcode = match_content.match_postcode(addr['postcode'])

    if postcode != ''  and postcode not in postcodes:
        postcodes.append(match_content.match_postcode(addr['postcode']))
        addr_filtered.append(addr)

print('filtered:', addr_filtered)