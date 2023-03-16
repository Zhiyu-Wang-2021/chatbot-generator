import os,sys,unittest
sys.path.append(os.curdir + '/chatbotSite')
from webscraptool import tokenizer
# run command
# coverage run --branch -m unittest chatbotSite/unitTest/test_tokenizer.py
input = '''
        After 118 years of residence in one of the oldest buildings in Enfield at 68 Silver Street, 
        dating back to the 16th century, in December 2021, we have moved to the modern health centre 
        at 105-109 Chase Side.

        We have been home to Doctors in Enfield for over a hundred years. 
        Since 1903, the practice has cared for a growing and ever-changing population. 
        Our Doctors, Nurses and Clinicians work together to deliver 
        a friendly, professional and efficient service to all our patients. 
        We aim to provide the highest standard of medical and pastoral care and encourage healthy living.

        We are a fully computerised practice. All consultations, medical histories, referrals 
        and test results are recorded on each person’s computer record, 
        together with clinical correspondence such as hospital letters.
        
        '''
expected_ans = True
res = tokenizer.tokenization(input)
print(res)
class TestWebscraptool(unittest.TestCase):
    def test_tokenizer_empty_input(self):
        input = ''
        expected_ans = ''
        res = tokenizer.tokenization(input)
        self.assertEqual(res, expected_ans)

    def test_tokenizer_too_short_input(self):
        input = 'I am'
        expected_ans = ''
        res = tokenizer.tokenization(input)
        self.assertEqual(res, expected_ans)

    def test_tokenizer_normal_input(self):
        input = '''
        After 118 years of residence in one of the oldest buildings in Enfield at 68 Silver Street, 
        dating back to the 16th century, in December 2021, we have moved to the modern health centre 
        at 105-109 Chase Side.

        We have been home to Doctors in Enfield for over a hundred years. 
        Since 1903, the practice has cared for a growing and ever-changing population. 
        Our Doctors, Nurses and Clinicians work together to deliver 
        a friendly, professional and efficient service to all our patients. 
        We aim to provide the highest standard of medical and pastoral care and encourage healthy living.

        We are a fully computerised practice. All consultations, medical histories, referrals 
        and test results are recorded on each person’s computer record, 
        together with clinical correspondence such as hospital letters.
        
        '''
        expected_ans = True
        res = tokenizer.tokenization(input)
        self.assertEqual(res!='', expected_ans)