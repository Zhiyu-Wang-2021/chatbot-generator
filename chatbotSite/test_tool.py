def filter_text(content_dict) -> dict:
        categories = {'':0, 'openingtime':1,'address':2,'phonenumber':3}
        i = categories.get(content_dict['category'])
        result = {}

        if i == 0:
            result = ''

        if i == 1:
            result = 1
            result = 1

        if i == 2:
            result = 2
            result = 2

        if i == 3:
            result = 3
            result = 3

        return {'category': content_dict['category'], 'filtered_text': result}

a = {'category': 'openingtime', 'text':'fucktou'}
print(filter_text(a))