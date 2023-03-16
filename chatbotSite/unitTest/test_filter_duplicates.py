import os,sys,unittest
sys.path.append(os.curdir + '/chatbotSite')
from webscraptool import filter_content
# run command
# coverage run --branch -m unittest chatbotSite/unitTest/test_filter_duplicates.py
class TestWebscraptool(unittest.TestCase):
    def test_filter_duplicate_phonenum(self):
        input = [{'num':'020 7704 2832'},{'num':'020 7704 2832'},{'num':'020 7704 2832'},{'num':'020 7405 9200'},{'num':'020 7405 9200'},{'num':'020 7405 9200'},{'num':'020 7405 9200'}]
        expected_ans = ['020 7704 2832', '020 7405 9200']
        res = filter_content.phonenumber(input)
        self.assertEqual(res, expected_ans)

    # phone num with region code 
    # e.g.+44 (0)20 7405 9200, 020 7405 9200 
    def test_filter_duplicate_phonenum2(self):
        input = [{'num':'+44 (0)20 7405 9200'},{'num':'020 7405 9200'}]
        expected_ans = ['+44 (0)20 7405 9200']
        res = filter_content.phonenumber(input)
        self.assertEqual(res, expected_ans)

    # same postcode same addr
    def test_filter_duplicate_addr(self):
        input = [{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''},{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''}]
        expected_ans = [{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''}]
        res = filter_content.addr(input)
        self.assertEqual(res, expected_ans)

    # same postcode different addr
    def test_filter_duplicate_addr2(self):
        input = [{'postcode': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'address': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY\nSomers Town Medical Centre\n', 'contact': ''},{'postcode': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY', 'address': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY\nKings Cross Surgery\n', 'contact': ''},{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''},{'postcode': '1 Frith St, London, W1D 3HZ', 'address': '1 Frith St, London, W1D 3HZ', 'contact': ''}]
        expected_ans = [{'postcode': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY', 'address': 'Somers Town Medical Centre Sommers Town Medical Centre, 77-83 Chalton Street London, NW1 1HY\nSomers Town Medical Centre\n', 'contact': ''},{'postcode': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY', 'address': 'Kings Cross Surgery 77 – 83 Chalton Street, NW1 1HY\nKings Cross Surgery\n', 'contact': ''},{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''}]
        res = filter_content.addr(input)
        self.assertEqual(res, expected_ans)
    
    # same addr(little different writing format) same postcode
    # street and st(abbr)
    def test_filter_duplicate_addr3(self):
        input = [{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''},{'postcode': '1 Frith St, London, W1D 3HZ', 'address': '1 Frith St, London, W1D 3HZ', 'contact': ''}]
        res = filter_content.addr(input)
        expected_ans = [{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ', 'contact': ''}]
        
        self.assertEqual(res, expected_ans)
    
    # scrape a link('3be45ae8' being recognized as postcode)
    # https://feedback.camdenccg.nhs.uk/north-central-london/3be45ae8/
    def test_filter_duplicate_addr4(self):
        input = [{'postcode': 'https://feedback.camdenccg.nhs.uk/north-central-london/3be45ae8/', 'address': 'https://feedback.camdenccg.nhs.uk/north-central-london/3be45ae8/', 'contact': ''}]
        res = filter_content.addr(input)
        expected_ans = []
        
        self.assertEqual(res, expected_ans)

    def test_filter_duplicate_opening(self):
        input = [{'title':'Opening Times','time':'''
                                    Monday	8:00am - 6:30pm
                                    Tuesday	8:00am - 6:30pm
                                    Wednesday	8:00am - 6:30pm
                                    Thursday	8:00am - 6:30pm
                                    Friday	8:00am - 6:30pm
                                    Saturday	9:00am - 1:00pm                           
                            '''},{'title':'Opening Times','time':'''
                                    Monday	8:00am - 6:30pm
                                    Tuesday	8:00am - 6:30pm
                                    Wednesday	8:00am - 6:30pm
                                    Thursday	8:00am - 6:30pm
                                    Friday	8:00am - 6:30pm
                                    Saturday	9:00am - 1:00pm                           
                            '''}]
        expected_ans = ['',{'title':'Opening Times','time':'''
                                    Monday	8:00am - 6:30pm
                                    Tuesday	8:00am - 6:30pm
                                    Wednesday	8:00am - 6:30pm
                                    Thursday	8:00am - 6:30pm
                                    Friday	8:00am - 6:30pm
                                    Saturday	9:00am - 1:00pm                           
                            '''}]
        res = filter_content.openingtime(input)
        self.assertEqual(res, expected_ans)

    # wrong information but contains a time in it
    def test_filter_duplicate_opening2(self):
        input = [{'title':'','time':'''
                            Air pollution levels added to patient's postcodes
                            16 Feb 2023, 6:15 a.m.

                            Air pollution levels for patient’s postcodes have been added to their medical records to help families understand the risk in their local area. 
                            
                            '''},{'title':'','time':'''
                            Air pollution levels added to patient's postcodes
                            16 Feb 2023, 6:15 a.m.

                            Air pollution levels for patient’s postcodes have been added to their medical records to help families understand the risk in their local area. 
                            
                            '''}]
        expected_ans = ['']
        res = filter_content.openingtime(input)
        self.assertEqual(res, expected_ans)

    # multiple clinic
    def test_filter_duplicate_opening3(self):
        input = [{'title':'Stanhope Health Centre','time':'''
                                    Today	08:00 - 18:00
                                    Wed 15 Mar	08:00 - 18:00
                                    Thu 16 Mar	08:00 - 18:00
                                    Fri 17 Mar	08:00 - 18:00
                                    Sat 18 Mar	Closed
                                    Sun 19 Mar	Closed
                                    Mon 20 Mar	08:00 - 18:00
                            
                            '''},{'title':'Wolsingham Surgery','time':'''
                                    Today	08:00 - 18:00
                                    Wed 15 Mar	08:00 - 18:00
                                    Thu 16 Mar	08:00 - 18:00
                                    Fri 17 Mar	08:00 - 18:00
                                    Sat 18 Mar	Closed
                                    Sun 19 Mar	Closed
                                    Mon 20 Mar	08:00 - 18:00                           
                            '''},{'title':'Stanhope Health Centre','time':'''
                                    Today	08:00 - 18:00
                                    Wed 15 Mar	08:00 - 18:00
                                    Thu 16 Mar	08:00 - 18:00
                                    Fri 17 Mar	08:00 - 18:00
                                    Sat 18 Mar	Closed
                                    Sun 19 Mar	Closed
                                    Mon 20 Mar	08:00 - 18:00
                            
                            '''}]
        expected_ans = ['',{'title':'Stanhope Health Centre','time':'''
                                    Today	08:00 - 18:00
                                    Wed 15 Mar	08:00 - 18:00
                                    Thu 16 Mar	08:00 - 18:00
                                    Fri 17 Mar	08:00 - 18:00
                                    Sat 18 Mar	Closed
                                    Sun 19 Mar	Closed
                                    Mon 20 Mar	08:00 - 18:00
                            
                            '''},{'title':'Wolsingham Surgery','time':'''
                                    Today	08:00 - 18:00
                                    Wed 15 Mar	08:00 - 18:00
                                    Thu 16 Mar	08:00 - 18:00
                                    Fri 17 Mar	08:00 - 18:00
                                    Sat 18 Mar	Closed
                                    Sun 19 Mar	Closed
                                    Mon 20 Mar	08:00 - 18:00                           
                            '''}]
        res = filter_content.openingtime(input)
        self.assertEqual(res, expected_ans)

    # title not in keyword
    def test_filter_duplicate_opening4(self):
        input = [{'title':'training','time':'''
                                    Today	08:00 - 18:00
                                    Wed 15 Mar	08:00 - 18:00
                                    Thu 16 Mar	08:00 - 18:00
                                    Fri 17 Mar	08:00 - 18:00
                                    Sat 18 Mar	Closed
                                    Sun 19 Mar	Closed
                                    Mon 20 Mar	08:00 - 18:00
                            
                            '''}]
        expected_ans = ['']
        res = filter_content.openingtime(input)
        self.assertEqual(res, expected_ans)