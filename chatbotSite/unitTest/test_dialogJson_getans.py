import os,sys,unittest
sys.path.append(os.curdir + '/chatbotSite')
from dialogJson.answers import Answers
import string

# run command
# coverage run --branch -m unittest chatbotSite/unitTest/test_dialogJson_getans.py
class TestWebscraptool(unittest.TestCase):
    def test_get_phoneinfo(self):
        input = {'answers':{
                        'phone': ['020 8363 4156'],
                        'openingtimepage':'',
                        'contactpage': '',
                        'appointment': ''
                            }}
        expected_ans = 'Please call us with this number:\n020 8363 4156'
        ans = Answers(input)
        res = ans.get_phone_info()
        self.assertEqual(res, expected_ans)

    def test_get_phoneinfo_emptyinput(self):
        input = {'answers':{
                        'phone': '',
                        'openingtimepage':'',
                        'contactpage': '',
                        'appointment': ''
                            }}
        ans = Answers(input)
        expected_ans = 'Sorry, I am not sure about this question based on the information on our website.'
        res = ans.get_phone_info()
        self.assertEqual(res, expected_ans)

    def test_get_hourinfo(self):
        input = {'answers':{
                        'phone': '',
                        'openingtimepage':['', {'title': 'Stanhope Health Centre', 'time': 'Today\n08:00\n-\n18:00\nThu 16 Mar\n08:00\n-\n18:00\nFri 17 Mar\n08:00\n-\n18:00\n'}, {'title': 'Wolsingham Surgery', 'time': 'Thu 16 Mar\n08:00\n-\n17:00\nFri 17 Mar\n08:30\n-\n12:30\n'}, {'title': "St John's Chapel Surgery", 'time': 'Today\n08:00\n-\n12:30\n'}],
                        'contactpage': '',
                        'appointment': ''
                            }}
        expected_ans = \
        '''
        Our trusts opens on:

        Stanhope Health Centre
        Today
        08:00
        -
        18:00
        Thu 16 Mar
        08:00
        -
        18:00
        Fri 17 Mar
        08:00
        -
        18:00

        Wolsingham Surgery
        Thu 16 Mar
        08:00
        -
        17:00
        Fri 17 Mar
        08:30
        -
        12:30

        St John's Chapel Surgery
        Today
        08:00
        -
        12:30
        '''
        ans = Answers(input)
        res = ans.get_hours_info()
        # we need to remove all the whitespace when comparing them
        self.assertEqual(expected_ans.translate({ord(c): None for c in string.whitespace}), 
                         res.translate({ord(c): None for c in string.whitespace})
                         )
        
    def test_get_hourinfo_emptyinput(self):
        input = {'answers':{
                        'phone': '',
                        'openingtimepage':[''],
                        'contactpage': '',
                        'appointment': ''
                            }}
        expected_ans = 'Sorry, I am not sure about this question based on the information on our website.'
        ans = Answers(input)
        res = ans.get_hours_info()
        # we need to remove all the whitespace when comparing them
        self.assertEqual(expected_ans, res)

    def test_get_hourinfo_Noneinput(self):
        input = {'answers':{
                        'phone': '',
                        'openingtimepage':None,
                        'contactpage': '',
                        'appointment': ''
                            }}
        expected_ans = 0
        ans = Answers(input)
        res = ans.length_of_hours_info()
        # we need to remove all the whitespace when comparing them
        self.assertEqual(expected_ans, res)

    def test_get_appointment(self):
        input = {'answers':{
                        'phone': '',
                        'openingtimepage':'',
                        'contactpage': '',
                        'appointment': ['this is appointment info',0.5]
                            }}
        expected_ans = 'this is appointment info'
        ans = Answers(input)
        res = ans.get_appointment_info()
        # we need to remove all the whitespace when comparing them
        self.assertEqual(expected_ans, res)

    # single clinic
    def test_get_addr(self):
        input = {'answers':{
                                'phone': '',
                                'openingtimepage':['', {'title': 'Sommers Town Medical Centre', 'time': 'Today\n08:00\n-\n18:00\nThu 16 Mar\n08:00\n-\n18:00\nFri 17 Mar\n08:00\n-\n18:00\n'}],
                                'contactpage': [{'postcode': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'address': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY\nSomers Town Medical Centre\n', 'contact': ''}],
                                'appointment': ''
                                    }}
        expected_ans = \
        '''
        We are at this address:
        Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY
        Somers Town Medical Centre
        Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY
        '''
        ans = Answers(input)
        res = ans.get_loc_info()
        self.assertEqual(expected_ans.translate({ord(c): None for c in string.whitespace}), 
                         res.translate({ord(c): None for c in string.whitespace})
                         )
        
    # multiple clinic
    def test_get_addr2(self):
        input = {'answers':{
                                'phone': '',
                                'openingtimepage':['', {'title': 'Sommers Town Medical Centre', 'time': 'Today\n08:00\n-\n18:00\nThu 16 Mar\n08:00\n-\n18:00\nFri 17 Mar\n08:00\n-\n18:00\n'}, {'title': 'Brunswick Medical Centre', 'time': 'Thu 16 Mar\n08:00\n-\n17:00\nFri 17 Mar\n08:30\n-\n12:30\n'}, {'title': "Kings Cross Surgery", 'time': 'Today\n08:00\n-\n12:30\n'}],
                                'contactpage': [{'postcode': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'address': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY\nSomers Town Medical Centre\n', 'contact': ''}, {'postcode': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY', 'address': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY\nKings Cross Surgery\n', 'contact': ''}, {'postcode': 'Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF', 'address': 'Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF\nBrunswick Medical Centre\n', 'contact': ''}],
                                'appointment': ''
                                    }}
        expected_ans = \
        '''
        We are at these addresses:
        Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY
        Somers Town Medical Centre
        Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY
        Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY
        Kings Cross Surgery
        Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY
        Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF
        Brunswick Medical Centre
        Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF
        '''
        ans = Answers(input)
        res = ans.get_loc_info()
        self.assertEqual(expected_ans.translate({ord(c): None for c in string.whitespace}), 
                         res.translate({ord(c): None for c in string.whitespace})
                         )
    # duplication of postcode sentence and address 
    def test_get_addr3(self):
        input = {'answers':{
                                'phone': '',
                                'openingtimepage':'',
                                'contactpage': [{'postcode': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'address': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'contact': ''}],
                                'appointment': ''
                                    }}
        expected_ans = \
        '''
        We are at this address:
        Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY
        '''
        ans = Answers(input)
        res = ans.get_loc_info()
        self.assertEqual(expected_ans.translate({ord(c): None for c in string.whitespace}), 
                         res.translate({ord(c): None for c in string.whitespace})
                         )      
        
    # duplication of postcode sentence and address(multiple clinic situation)
    def test_get_addr4(self):
        input = {'answers':{
                                'phone': '',
                                'openingtimepage':['', {'title': 'Sommers Town Medical Centre', 'time': 'Today\n08:00\n-\n18:00\nThu 16 Mar\n08:00\n-\n18:00\nFri 17 Mar\n08:00\n-\n18:00\n'}, {'title': 'Brunswick Medical Centre', 'time': 'Thu 16 Mar\n08:00\n-\n17:00\nFri 17 Mar\n08:30\n-\n12:30\n'}, {'title': "Kings Cross Surgery", 'time': 'Today\n08:00\n-\n12:30\n'}],
                                'contactpage': [{'postcode': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'address': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'contact': ''}, {'postcode': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY', 'address': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY', 'contact': ''}, {'postcode': 'Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF', 'address': 'Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF', 'contact': ''}],
                                'appointment': ''
                                    }}
        expected_ans = \
        '''
        We are at these addresses:
        Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY
        Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY
        Brunswick Medical Centre Brunswick Medical Centre, 39 Brunswick Square London, WC1N 1AF
        '''
        ans = Answers(input)
        res = ans.get_loc_info()
        self.assertEqual(expected_ans.translate({ord(c): None for c in string.whitespace}), 
                         res.translate({ord(c): None for c in string.whitespace})
                         )    

    # no input
    def test_get_addr_empty_input(self):
        input = {'answers':{
                                'phone': '',
                                'openingtimepage':['', {'title': 'Sommers Town Medical Centre', 'time': 'Today\n08:00\n-\n18:00\nThu 16 Mar\n08:00\n-\n18:00\nFri 17 Mar\n08:00\n-\n18:00\n'}, {'title': 'Brunswick Medical Centre', 'time': 'Thu 16 Mar\n08:00\n-\n17:00\nFri 17 Mar\n08:30\n-\n12:30\n'}, {'title': "Kings Cross Surgery", 'time': 'Today\n08:00\n-\n12:30\n'}],
                                'contactpage': '',
                                'appointment': ''
                                    }}
        expected_ans = 'Sorry, I am not sure about this question based on the information on our website.'
        ans = Answers(input)
        res = ans.get_loc_info()
        self.assertEqual(res,expected_ans)

    