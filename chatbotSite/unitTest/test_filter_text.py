#from webscraptool.get_openingtime import run
import os,sys,unittest
sys.path.append(os.curdir + '/chatbotSite')
from webscraptool import match_content

# run command
# coverage run --branch -m unittest chatbotSite/unitTest/test_filter_text.py
class TestWebscraptool(unittest.TestCase):
    def test_match_postcode(self):
        input = ''' 
                105-109 Chase Side
                Enfield
                EN2 6NL
                '''
        expected_ans = 'EN2 6NL'
        res = match_content.match_postcode(input)
        self.assertEqual(res, expected_ans)

    # 2 postcode(should only return first one)
    def test_match_postcode2(self):
        input = ''' 
                105-109 Chase Side
                Enfield
                EN2 6NL
                N1 9JP
                '''
        expected_ans = 'EN2 6NL'
        res = match_content.match_postcode(input)
        self.assertEqual(res, expected_ans)

    # everything in one line
    def test_match_postcode3(self):
        input = ''' 
                134 Askew Road, Shepherds Bush, London, W12 9BP
                '''
        expected_ans = 'W12 9BP'
        res = match_content.match_postcode(input)
        self.assertEqual(res, expected_ans)

    # failed
    def test_match_postcode3_failed(self):
        input = ''' 
                134 Askew Road, Shepherds Bush, London
                '''
        expected_ans = ''
        res = match_content.match_postcode(input)
        self.assertEqual(res, expected_ans)

    # wrong numebr given
    def test_match_phonenum(self):
        input = ''' 
                    1234567890
                '''
        expected_ans = False
        res = match_content.match_phonenumber(input)
        self.assertEqual(res, expected_ans)

    # correct numebr given
    def test_match_phonenum2(self):
        input = ''' 
                    +44 (0)20 7405 9200
                '''
        expected_ans = True
        res = match_content.match_phonenumber(input)
        self.assertEqual(res, expected_ans)

    def test_match_phonenum_content(self):
        input = ''' 
                Great Ormond Street Hospital for Children NHS Foundation Trust
                Great Ormond Street
                London WC1N 3JH

                Phone: +44 (0)20 7405 9200
                '''
        expected_ans = '+44 (0)20 7405 9200'
        res = match_content.match_phonenumber_content(input)
        self.assertEqual(res, expected_ans)

    # return the first phone num appear in the context
    def test_match_phonenum_content2(self):
        input = ''' 
                Great Ormond Street Hospital for Children NHS Foundation Trust
                Great Ormond Street
                London WC1N 3JH

                Phone: +44 (0)20 7405 9200
                020 7405 9200
                '''
        expected_ans = '+44 (0)20 7405 9200'
        res = match_content.match_phonenumber_content(input)
        self.assertEqual(res, expected_ans)
    
    # failed
    def test_match_phonenum_content3_failed(self):
        input = ''' 
                Great Ormond Street Hospital for Children NHS Foundation Trust
                Great Ormond Street
                London WC1N 3JH

                Phone:
                '''
        expected_ans = None
        res = match_content.match_phonenumber_content(input)
        self.assertEqual(res, expected_ans)

    # return all the phone number
    def test_match_phonenum_it(self):
        input = ''' 
                            phone:+44 (0)20 7405 9200
                            appointment:020 7829 8880
                            our contact:020 7405 9200
                        '''
        expected_ans = '+44 (0)20 7405 9200020 7829 8880020 7405 9200'
        ms = match_content.match_phonenumber_it(input)
        combined = ''

        combined = combined + ms.next().raw_string
        combined = combined + ms.next().raw_string
        combined = combined + ms.next().raw_string
        res = combined

        self.assertEqual(res, expected_ans)

    def test_match_combined_spaces(self):
        input = 'a         a'
        expected_ans = 'a a'
        res = match_content.spaceReplace(input)
        self.assertEqual(res, expected_ans)

    def test_match_time_it(self):
        input = '18:00 random    19:00  random  20:00'
        expected_ans = '18:0019:0020:00'
        ms = match_content.match_time_it(input)
        combined = ''
        for m in ms:
            combined = combined + str(m.group())
        res = combined
        self.assertEqual(res, expected_ans)
    
    # no match
    def test_match_time_it_failed(self):
        input = '1800 random    1900  random  2000'
        expected_ans = ''
        ms = match_content.match_time_it(input)
        combined = ''
        for m in ms:
            combined = combined + str(m.group())
        res = combined
        self.assertEqual(res, expected_ans)

    # check if xx:xx format of time can be matched
    def test_match_time(self):
        input = '18:00 random    19:00  random  20:00'
        expected_ans = True
        res = match_content.match_time(input)
        self.assertEqual(res, expected_ans)

    # checked xxpm,xxam format can be matched
    def test_match_time2(self):
        input = 'random text   11am random text'
        expected_ans = True
        res = match_content.match_time(input)
        self.assertEqual(res, expected_ans)

    # checked xxpm,xxam format can be matched
    def test_match_time3_fail_case(self):
        input = 'random text   11 arandom textm'
        expected_ans = False
        res = match_content.match_time(input)
        self.assertEqual(res, expected_ans)