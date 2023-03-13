import env
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SyntaxOptions

def tokenization(txt):
    if txt == '':
        return ''
    
    try:
        apikey = env.IBM_NLU_API_KEY
        apiurl = env.IBM_NLU_URL
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
    except Exception as e:
        print(e)
        return ''
    
    return response
