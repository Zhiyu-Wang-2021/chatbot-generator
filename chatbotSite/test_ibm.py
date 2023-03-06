from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SyntaxOptions, SyntaxOptionsTokens
# check phone number and postcode
import webscraptool.match_content as match_content

def run(txt):
    # 1.ibm nlu extract every phrases and sentences
    apikey = 'Iig5IogwUhp2dIo1FqAUEjkka7OoC42qXbWHWucIU9oU'
    apiurl = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2019387f-a518-46b0-aa72-ccc03cdf67c8'
    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(apiurl)



    # only get sentences
    response = natural_language_understanding.analyze(
        text=txt,
        features=Features(
        syntax=SyntaxOptions(
            sentences=True,
            ))).get_result()
    return(response)

print(run('''Extended Practice Opening Hours Appointments are available until 19:15 on Monday evenings and from 07:30 on Tuesday and Wednesday mornings. iHUB - GP Extended Hours Private Medical Examinations'''))