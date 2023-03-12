import re
import phonenumbers # check phone number

def spaceReplace(i):
    i = ' '.join(i.split())
    return i

def match_postcode(text):
    # input category:
    # 1.only contain postcode
    # 2.postcode and address are in one line
    # e.g.134 Askew Road, Shepherds Bush, London, W12 9BP
    # 3.other thing

    # need combine 2 spaces to 1 or regex can not recognize
    text = spaceReplace(text)
    # this regex is provided by UK government
    a=re.search(
        r'([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})',
        text)
    if a:
        # only match the first one as it commanly just contain one in single sentence
        return a.group()
    else:
        return ''

def match_phonenumber(text):
    # a phonenum is matched:return True else false
    for m in match_phonenumber_it(text):
        
        if m.start == 0 or m.start > 0:
            return True

    return False

def match_phonenumber_it(text):
    # return an iterable object of match result
    return phonenumbers.PhoneNumberMatcher(text, "GB")

def match_phonenumber_content(text):
    # mathch the first phone number appears in a given text
    a = match_phonenumber_it(text)
    for m in match_phonenumber_it(text):
        if m.start == 0 or m.start > 0:
            return text[m.start:m.end]
        else:
            return None

def match_time_it(text):
    # match time in sentences, if exists return an iterable object
    match=re.finditer(r'(\d+:\d{2})', text)
    if match:
        return match
    else:
        return ''

def match_time(text):
    # a time is matched:return True else false
    match1=re.search(r'(\d+:\d{2})', text)
    match2=re.search(r'(\d{1}am|\d{1}pm)', text)

    if match1:
        return True
    elif match2:
        return True
    else:
        return False    
