import os,sys,unittest
sys.path.append(os.curdir + '/chatbotSite')
from webscraptool import get_phone_num
from webscraptool import get_openingtime
from webscraptool import get_addr
# run command
# coverage run --branch -m unittest chatbotSite/unitTest/test_getanswer.py
class TestWebscraptool(unittest.TestCase):
    def test_get_phonenum(self):
        input = '''
                Contact Us
                White Lodge Medical Practice
                105-109 Chase Side
                Enfield
                EN2 6NL

                020 8363 4156

                Out of hours: 111
        '''
        expected_ans = [{'title':'','num':'020 8363 4156'}]
        res = get_phone_num.run(input)
        self.assertEqual(res, expected_ans)

    # phonenum with some label before it
    def test_get_phonenum2(self):
        input = '''
                Contact Us
                White Lodge Medical Practice
                105-109 Chase Side
                Enfield
                EN2 6NL

                phone:
                020 8363 4156

                Out of hours: 111
        '''
        expected_ans = [{'num':'020 8363 4156','title':'phone:'}]
        res = get_phone_num.run(input)
        self.assertEqual(res, expected_ans)

    # multiple phonenum
    def test_get_phonenum3(self):
        input = '''
                Contact Us
                White Lodge Medical Practice
                105-109 Chase Side
                Enfield
                EN2 6NL
                phone:
                020 8363 4156

                fax:
                020 8363 4156

                Out of hours: 111
        '''
        expected_ans = [{'title':'phone:','num':'020 8363 4156'},{'title':'fax:','num':'020 8363 4156'}]
        res = get_phone_num.run(input)
        self.assertEqual(res, expected_ans)

    def test_get_phonenum_empty_input(self):
        input = ''
        expected_ans = []
        res = get_phone_num.run(input)
        self.assertEqual(res, expected_ans)

    # single clinic situation(scrpaed from https://www.whitelodgemedicalpractice.nhs.uk/practice-information/opening-hours/)
    def test_get_openinghour(self):
        input = '''
        Tell us whether you accept cookies\nWe've put some small files called cookies on your device to make our site work. We would also like to use analytical cookies to understand how our site is used and improve user experience. Analytical cookies send information to Google Analytics.\nLet us know your preference. We will use a cookie to save your choice. Before you make your choice you can read more about our \ncookie policy\n.\nAccept all cookies\nSet cookie preferences\nSkip to content\nWhite Lodge Medical Practice\nHome\nGet Help\nOnline Requests\nTel\n020 8363 4156\n105-109 Chase Side\n\nEnfield\n\nEN2 6NL\n Map\nCQC\n Inspected and Rated\nGood\nWe are currently \nopen.\nView all opening hours\nPractice Information \nNew Patient Registration\nGP Extended Access Service\nFriends & Family Test \nSite Map\nSite Credits\nPrivacy Statement\nDisclaimer\nCopyright\nAccessibility\nCookie Policy\nFootFall © Silicon Practice 2023\nHome\nGet Help\nOnline Requests\nSearch the website: \nSearch\nWhite Lodge Medical Practice\nBack\nOpening Hours\nWe are currently \nopen.\nMonday\n08:00-18:30\r\nTuesday\n08:00-18:30\r\nWednesday\n08:00-18:30\r\nThursday\n08:00-18:30\r\nFriday\n08:00-18:30\nSaturday\nClosed\nSunday\nClosed\nOut of Hours Service\nNHS 111\nIf you require medical assistance outside normal practice hours, please contact the NHS 111 service by calling 111. The service is open 24 hours a day, 7 days a week and all calls to the service are free. If you contact the service, you may be;\nGiven telephone advice\nAsked to attend a local Out of hours centre for a consultation\nReferred to a local Accident and Emergency department, or\nOffered a home visit by a deputising Doctor\nIn a Emergency\nIn the event of a medical emergency, please call 999 immediately to contact the ambulance service.\nYou have an unread news item \n(1)\nPractice Relocation\nWe are relocating to 105-109 Chase Side, Enfield, EN2 6NL on the 13th of December 2021\nImportant -\nThe Extended Access service is available for prebooked appointments only and will run on weekday evenings 6:30-8pm, Saturdays 8am-8pm and Sundays 8am-8pm. The service has both GPs ... \nFind out more\nDismiss\nClose\nPhone\n            \nTel\n020 8363 4156\nLocation\n            \n105-109 Chase Side\n\nEnfield\n\nEN2 6NL\n Map\nMessage\n          
      \nNews\n                                        \n                                            \n1\n
        '''
        expected_ans = [{'title': 'Opening Hours', 'time': 'Monday\n08:00-18:30\nTuesday\n08:00-18:30\nWednesday\n08:00-18:30\nThursday\n08:00-18:30\nFriday\n08:00-18:30\n'}, {'title': '', 'time': 'Important -\nThe Extended Access service is available for prebooked appointments only and will run on weekday evenings 6:30-8pm, Saturdays 8am-8pm and Sundays 8am-8pm.\n'}]
        res = get_openingtime.run(input)
        self.assertEqual(res, expected_ans)

    # several clinic situation(text is scraped from https://www.theweardalepractice.nhs.uk/opening-hours)
    def test_get_openinghour2(self):
        input = '''
Skip to main\n\r\n                    The Weardale Practice\r\n                \nMenu\n Home\n\r\n\r\n\r\n                                My GP Health Record Login\r\n                            \n\r\n\r\n\r\n                                eConsult\r\n                            \n\r\n\r\n\r\n                            
    Practice News\r\n                            \n\r\n\r\n\r\n                                Appointments\r\n                            \n\r\n\r\n\r\n                                Prescriptions \r\n                   
         \n\r\n\r\n\r\n                                New Patients\r\n                            \n\r\n\r\n\r\n                                Practice Staff\r\n                            \n\r\n\r\n\r\n                 
               Contact us\r\n                            \n\r\n\r\n\r\n                                Find us\r\n                            \n \r\n        Language\n\r\n\r\n\r\n                                Practice News\r\n                            \n\r\n\r\n\r\n                                Prescriptions \r\n             
               \n\r\n\r\n\r\n                                Appointments\r\n                            \n\r\n\r\n\r\n                                eConsult\r\n                            \n\r\n\r\n\r\n                 
               New Patients\r\n                            \n\r\n\r\n\r\n                                My Patient Record\r\n                            \n\r\n\r\n\r\n                                Services\r\n          
                  \n\r\n\r\n\r\n                                Health Advice\r\n                            \n\r\n\r\n\r\n                                Health Campaigns\r\n                            \n\r\n\r\n\r\n                                About Us \r\n                            \n\r\n\r\n\r\n                             
   Our Staff\r\n                            \n\r\n\r\n\r\n                                Patient Participation Group\r\n                            \n\r\n\r\n\r\n                                Opening Hours\r\n          
                  \n\r\n\r\n\r\n                                Contact us\r\n                            \n\r\n\r\n\r\n                                Feedback & Complaints\r\n                            \n\r\n\r\n\r\n                                Practice Policies\r\n                            \n Home\n\r\n\r\n\r\n            
                    My GP Health Record Login\r\n                            \n\r\n\r\n\r\n                    
            eConsult\r\n                            \n\r\n\r\n\r\n                                Practice News\r\n                            \n\r\n\r\n\r\n                                Appointments\r\n                 
           \n\r\n\r\n\r\n                                Prescriptions \r\n                            \n\r\n\r\n\r\n                                New Patients\r\n                            \n\r\n\r\n\r\n               
                 Practice Staff\r\n                            \n\r\n\r\n\r\n                                Contact us\r\n                            \n\r\n\r\n\r\n                                Find us\r\n              
              \n \r\n        Language\nMenu\n\r\n\r\n\r\n                                Practice News\r\n                            \n\r\n\r\n\r\n                                Prescriptions \r\n                        
    \n\r\n\r\n\r\n                                Appointments\r\n                            \n\r\n\r\n\r\n                                eConsult\r\n                            \n\r\n\r\n\r\n                            
    New Patients\r\n                            \n\r\n\r\n\r\n                                My Patient Record\r\n                            \n\r\n\r\n\r\n                                Services\r\n                     
       \n\r\n\r\n\r\n                                Health Advice\r\n                            \n\r\n\r\n\r\n                                Health Campaigns\r\n                            \n\r\n\r\n\r\n                
                About Us \r\n                            \n\r\n\r\n\r\n                                Our Staff\r\n                            \n\r\n\r\n\r\n                                Patient Participation Group\r\n                            \n\r\n\r\n\r\n                                Opening Hours\r\n                     
       \n\r\n\r\n\r\n                                Contact us\r\n                            \n\r\n\r\n\r\n                                Feedback & Complaints\r\n                            \n\r\n\r\n\r\n              
                  Practice Policies\r\n                            \nOpening Hours\nStanhope Health Centre\nToday\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t18:00\r\n\t\t\t\t\t\t\nThu 16 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t18:00\r\n\t\t\t\t\t\t\nFri 17 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t18:00\r\n\t\t\t\t\t\t\nSat 18 Mar\nClosed\nSun 19 Mar\nClosed\nMon 20 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t18:00\r\n\t\t\t\t\t\t\nTue 21 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t18:00\r\n\t\t\t\t\t\t\nWolsingham Surgery\nToday\nClosed\nThu 16 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t17:00\r\n\t\t\t\t\t\t\nFri 17 Mar\n\r\n\t\t\t\t\t\t\t08:30\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t12:30\r\n\t\t\t\t\t\t\nSat 18 Mar\nClosed\nSun 19 Mar\nClosed\nMon 20 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t17:00\r\n\t\t\t\t\t\t\nTue 21 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t12:30\r\n\t\t\t\t\t\t\nSt John's Chapel Surgery\nToday\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t12:30\r\n\t\t\t\t\t\t\nThu 16 Mar\nClosed\nFri 17 Mar\n\r\n\t\t\t\t\t\t\t08:00\r\n\t\t\t\t\t\t\t\n-\n\r\n\t\t\t\t\t\t\t12:30\r\n\t\t\t\t\t\t\nSat 18 Mar\nClosed\nSun 19 Mar\nClosed\nMon 20 Mar\nClosed\nTue 21 Mar\nClosed\n\r\n\r\nWhen We Are Closed\t\t\nIf you require treatment outside of our standard opening hours, \nplease call 111\n. If necessary you will be directed to the most appropriate service for your particular health care need and to a local hub that ensures that you see the most appropriate healthcare professional.\nPlease note\n\xa0you must call 111 to receive an appointment first, this is not a walk in service. A health care professional will arrange an appointment for you, if required, at the nearest possible location for you.\nPlease remember to call 111 for advice first. You will need an appointment to be seen out of hours.\nPlease only call 999 for life-threatening emergencies.\n\r\n\r\nNHS 111 Online\t\t\n111 online is a fast and convenient alternative to the 111 phone service and provides an option for people who want to access 111 digitally.\xa0\nYour needs will be assessed and you will be given advice about whether you need:\nTreat yourself at home\nGo to a Primary Care Centre\nIf you need face to face medical attention you may be asked to attend a Primary Care Centre.\nClick here to access\xa0\nNHS 111 online\n\xa0or call 111 to speak to a staff member.\nFurther Information\n\r\n\r\n\r\n                         
       Update you Patient Record\r\n                            \n\r\n\r\n\r\n                                GP Earnings\r\n                            \n\r\n\r\n\r\n                                Practice Policies\r\n                            \n\r\n\r\n\r\n                                Suggestions & Complaints\r\n           
                 \nSign in\n© 2023 FPM Group\nAccessibility\nCookie Policy\nData Processing Policy\nSitemap\n×\nTranslate this website with google\nThis website uses cookies\nWe use cookies to improve user experience. Choose what cookies you allow us to use. You can \nread more about our cookies\n before you choose.\nStrictly Neces
        '''
        expected_ans = [{'title': 'Stanhope Health Centre', 'time': 'Today\n08:00\n-\n18:00\nThu 16 Mar\n08:00\n-\n18:00\nFri 17 Mar\n08:00\n-\n18:00\n'}, {'title': 'Stanhope Health Centre', 'time': 'Mon 20 Mar\n08:00\n-\n18:00\nTue 21 Mar\n08:00\n-\n18:00\n'}, {'title': 'Wolsingham Surgery', 'time': 'Thu 16 Mar\n08:00\n-\n17:00\nFri 17 Mar\n08:30\n-\n12:30\n'}, {'title': 'Wolsingham Surgery', 'time': 'Mon 20 Mar\n08:00\n-\n17:00\nTue 21 Mar\n08:00\n-\n12:30\n'}, {'title': "St John's Chapel Surgery", 'time': 'Today\n08:00\n-\n12:30\n'}, {'title': "St John's Chapel Surgery", 'time': 'Fri 17 Mar\n08:00\n-\n12:30\n'}]
        res = get_openingtime.run(input)
        self.assertEqual(res, expected_ans)
    
    # one sequence of time
    def test_get_openinghour3(self):
        input = '''
        CQC Inspected and Rated
        Good
        We are currently open.
        View all opening hours

        View practice news 
        Practice Information 

        New Patient Registration

        Practice Relocation
        We are relocating to 105-109 Chase Side, Enfield, EN2 6NL on the 13th of December 2021
        GP Extended Access Service

        Friends & Family Test 

        Site Map Site Credits Privacy Statement Disclaimer Copyright Accessibility Cookie Policy
        FootFall © Silicon Practice 2023
        Hide
        HomeGet HelpOnline Requests
        Search the website:
        Search...
        
        Search
        White Lodge Medical Practice
        Back
        Opening Hours
        We are currently open.

        Monday	08:00-18:30
        Tuesday	08:00-18:30
        Wednesday	08:00-18:30
        Thursday	08:00-18:30
        Friday	08:00-18:30
        Saturday	Closed
        Sunday	Closed
        '''
        expected_ans = [{'title': 'Opening Hours', 'time': 'Monday\n08:00-18:30\nTuesday\n08:00-18:30\nWednesday\n08:00-18:30\nThursday\n08:00-18:30\nFriday\n08:00-18:30\n'}]
        res = get_openingtime.run(input)
        self.assertEqual(res, expected_ans)

    # no consulting time we only need opening hour
    def test_get_openinghour4(self):
        input = '''
        CQC Inspected and Rated
        Good
        We are currently open.
        View all opening hours

        View practice news 
        Practice Information 

        New Patient Registration

        Practice Relocation
        We are relocating to 105-109 Chase Side, Enfield, EN2 6NL on the 13th of December 2021
        GP Extended Access Service

        Friends & Family Test 

        Site Map Site Credits Privacy Statement Disclaimer Copyright Accessibility Cookie Policy
        FootFall © Silicon Practice 2023
        Hide
        HomeGet HelpOnline Requests
        Search the website:
        Search...
        
        Search
        White Lodge Medical Practice
        Back
        Consulting Times
        We are currently open.

        Monday	08:00-18:30
        Tuesday	08:00-18:30
        Wednesday	08:00-18:30
        Thursday	08:00-18:30
        Friday	08:00-18:30
        Saturday	Closed
        Sunday	Closed
        '''
        expected_ans = []
        res = get_openingtime.run(input)
        self.assertEqual(res, expected_ans)

    def test_get_openinghour_empty_input(self):
        input = ''
        expected_ans = []
        res = get_openingtime.run(input)
        self.assertEqual(res, expected_ans)

    # text scraped from https://www.whitelodgemedicalpractice.nhs.uk/practice-information/contact-us/
    def test_get_addr(self):
        input = '''
                White Lodge Medical Practice
                Back
                Contact Us
                White Lodge Medical Practice
                105-109 Chase Side
                Enfield
                EN2 6NL

                Phone: 020 8363 4156

                Out of hours: 111

                Find us
                '''
        expected_ans = [{'postcode': 'EN2 6NL', 'address': 'Enfield\n105-109 Chase Side\nWhite Lodge Medical Practice\n', 'contact': 'EN2 6NL\nPhone: 020 8363 4156\n'}]
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)
    
    # multiple address on a single webpage from www.theweardalepractice.nhs.uk/find-us
    def test_get_addr2(self):
        input = '''
        Skip to main\n\r\n                    The Weardale Practice\r\n                \nMenu\n Home\n\r\n\r\n\r\n                                My GP Health Record Login\r\n                            \n\r\n\r\n\r\n                                eConsult\r\n                            \n\r\n\r\n\r\n                            
    Practice News\r\n                            \n\r\n\r\n\r\n                                Appointments\r\n                            \n\r\n\r\n\r\n                                Prescriptions \r\n                   
         \n\r\n\r\n\r\n                                New Patients\r\n                            \n\r\n\r\n\r\n                                Practice Staff\r\n                            \n\r\n\r\n\r\n                 
               Contact us\r\n                            \n\r\n\r\n\r\n                                Find us\r\n                            \n \r\n        Language\n\r\n\r\n\r\n                                Practice News\r\n                            \n\r\n\r\n\r\n                                Prescriptions \r\n             
               \n\r\n\r\n\r\n                                Appointments\r\n                            \n\r\n\r\n\r\n                                eConsult\r\n                            \n\r\n\r\n\r\n                 
               New Patients\r\n                            \n\r\n\r\n\r\n                                My Patient Record\r\n                            \n\r\n\r\n\r\n                                Services\r\n          
                  \n\r\n\r\n\r\n                                Health Advice\r\n                            \n\r\n\r\n\r\n                                Health Campaigns\r\n                            \n\r\n\r\n\r\n                                About Us \r\n                            \n\r\n\r\n\r\n                             
   Our Staff\r\n                            \n\r\n\r\n\r\n                                Patient Participation Group\r\n                            \n\r\n\r\n\r\n                                Opening Hours\r\n          
                  \n\r\n\r\n\r\n                                Contact us\r\n                            \n\r\n\r\n\r\n                                Feedback & Complaints\r\n                            \n\r\n\r\n\r\n                                Practice Policies\r\n                            \n Home\n\r\n\r\n\r\n            
                    My GP Health Record Login\r\n                            \n\r\n\r\n\r\n                    
            eConsult\r\n                            \n\r\n\r\n\r\n                                Practice News\r\n                            \n\r\n\r\n\r\n                                Appointments\r\n                 
           \n\r\n\r\n\r\n                                Prescriptions \r\n                            \n\r\n\r\n\r\n                                New Patients\r\n                            \n\r\n\r\n\r\n               
                 Practice Staff\r\n                            \n\r\n\r\n\r\n                                Contact us\r\n                            \n\r\n\r\n\r\n                                Find us\r\n              
              \n \r\n        Language\nMenu\n\r\n\r\n\r\n                                Practice News\r\n                            \n\r\n\r\n\r\n                                Prescriptions \r\n                        
    \n\r\n\r\n\r\n                                Appointments\r\n                            \n\r\n\r\n\r\n                                eConsult\r\n                            \n\r\n\r\n\r\n                            
    New Patients\r\n                            \n\r\n\r\n\r\n                                My Patient Record\r\n                            \n\r\n\r\n\r\n                                Services\r\n                     
       \n\r\n\r\n\r\n                                Health Advice\r\n                            \n\r\n\r\n\r\n                                Health Campaigns\r\n                            \n\r\n\r\n\r\n                
                About Us \r\n                            \n\r\n\r\n\r\n                                Our Staff\r\n                            \n\r\n\r\n\r\n                                Patient Participation Group\r\n                            \n\r\n\r\n\r\n                                Opening Hours\r\n                     
       \n\r\n\r\n\r\n                                Contact us\r\n                            \n\r\n\r\n\r\n                                Feedback & Complaints\r\n                            \n\r\n\r\n\r\n              
                  Practice Policies\r\n                            \nFind us\nStanhope Health Centre \nDales Street\nStanhope\nBishop Auckland\nDL13 2XD\n 01388 528555\n 111 (Out of Hours)\nOpening Times\nToday\n\r\n08:00\t\t\t\t-\r\n18:00\t\t\nWolsingham Surgery \nMarket Place\nWolsingham\nBishop Auckland\nDL13 3AB\n 01388 528555\n 111 (Out of Hours)\nOpening Times\nToday\nClosed\nSt John's Chapel Surgery \nHood Street\nSt John's Chapel\nBishop Auckland\nDL13 1QW\n 01388 528555\n 111 (Out of Hours)\nOpening Times\nToday\n\r\n08:00\t\t\t\t-\r\n12:30\t\t\nContact Us\nLast Updated: 07/11/2019\nYour Details\n\r\n                                                Name\r\n\r\n                                                    \n*\n\r\n                                       
         Date of Birth\r\n\r\n                                                    \n*\n\r\n                    
                            Phone Number\r\n\r\n                                            \n\r\n             
                                   Email Address\r\n\r\n                                                    \n*\nYour Comment\n\r\n                                                Comments\r\n\r\n                           
                         \n*\n\r\n                                                This form collects your name, date of birth, email, other personal information and medical details. This is to confirm you are registered with the practice, to allow the practice team to contact you and also to update your medical records held by the practice and our partners in the NHS. Please read our Privacy Policy to discover how we protect and manage your submitted data. \r\n\r\n                                                    \n*\nI consent to the practice collecting and storing my data from this form.\nOops... There was an error contacting reCAPTCHA, Please try again.\n\r\n    This form is protected by reCAPTCHA and the Google\r\n    \nPrivacy Policy\n and\r\n    \nTerms of Service\n apply.\r\n\nSubmit Form\nFurther Information\n\r\n\r\n\r\n                                Update you Patient Record\r\n                            \n\r\n\r\n\r\n                                GP Earnings\r\n                            \n\r\n\r\n\r\n                                Practice Policies\r\n                      
      \n\r\n\r\n\r\n                                Suggestions & Complaints\r\n                            \nSign in\n© 2023 FPM Group\nAccessibility\nCookie Policy\nData Processing Policy\nSitemap\n×\nTranslate this website with google\nThis website uses cookies\nWe use cookies to improve user experience. Choose what cookies you allow us to use. You can \nread more about our cookies\n before you choose.\nStrictly Necessary\nPerformance\nTargeting\nFunctionality\nSave & Close\nAccept all\nDecline all\n
        '''
        expected_ans = [{'postcode': 'DL13 2XD', 'address': 'Bishop Auckland\nStanhope\nDales Street\nStanhope Health Centre\n', 'contact': 'DL13 2XD\n01388 528555\n'}, {'postcode': 'DL13 3AB', 'address': 'Bishop Auckland\nWolsingham\nMarket Place\nWolsingham Surgery\n', 'contact': 'DL13 3AB\n01388 528555\n'}, {'postcode': 'DL13 1QW', 'address': "Bishop Auckland\nSt John's Chapel\nHood Street\nSt John's Chapel Surgery\n", 'contact': 'DL13 1QW\n01388 528555\n'}]
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)

    # no keyword is detected:graysinnmedical.co.uk/contact/
    # they use Rd instead of road
    def test_get_addr3(self):
        input = '''
                HOME
                JOIN THE PRACTICE
                OUR SERVICES
                PATIENT ACCESS
                OPENING TIMES
                COVID-19
                PRESCRIPTIONS
                CONTACT
                SICK NOTE
                TV DOCTORS
                POLICIES
                OTHER PRACTICES
                EDUCATION
                HOW TO USE OUR SERVICE
                Contact
                Contact
                CONTACT US
                VISIT US
                77 Grays Inn Rd
                London
                WC1X 8TS
                HOW TO USE OUR SERVICE
                Contact
                Contact
                CONTACT US
                VISIT US
                '''
        expected_ans = [{'postcode': 'WC1X 8TS', 'address': 'WC1X 8TSLondon77 Grays Inn Rd', 'contact': ''}]
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)

    # from www.sohosquaregp.co.uk
    def test_get_addr4(self):
        input = '''
                CONTACT US
                We’re here for you when you need us! Call us to schedule an appointment, or send us an email and we’ll get back to you as soon as possible.
                random text
                1 Frith Street, London, W1D 3HZ
                article
                '''
        expected_ans = [{'postcode': '1 Frith Street, London, W1D 3HZ', 'address': '1 Frith Street, London, W1D 3HZ\n', 'contact': ''}]
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)

    # single line no keyword
    def test_get_addr5(self):
        input = '''
                1 Frith St, London, W1D 3HZ
                '''
        expected_ans = [{'postcode': '1 Frith St, London, W1D 3HZ', 'address': '1 Frith St, London, W1D 3HZ', 'contact': ''}]
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)

    # separate line no keyword
    def test_get_addr6(self):
        input = '''
                This is where we located
                1 Frith St
                London
                W1D 3HZ
                '''
        expected_ans = [{'postcode': 'W1D 3HZ', 'address': 'W1D 3HZLondon1 Frith St', 'contact': ''}]
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)

    def test_get_addr_empty_input(self):
        input = ''
        expected_ans = []
        res = get_addr.run(input)
        self.assertEqual(res, expected_ans)

