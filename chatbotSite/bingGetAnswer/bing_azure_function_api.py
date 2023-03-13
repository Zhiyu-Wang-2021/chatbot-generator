# ---------------------------bing api--------------------------------------
import requests
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna
import env

def get_bing_result(domain_url, question):
    url = env.BING_AZURE_FUNC_URL

    payload = {
        "q": question,
        "site": 'https://' + domain_url
    }
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": env.BING_API_KEY,
    }
    
    # try to reconnect to bing if failed connection due to internet problem
    connection_attempt = 0
    max_connection_attempt = 5

    while(connection_attempt < max_connection_attempt):
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            response_data = json.loads(response.text)
            connection_attempt = 5
            response.close()
            break
        except Exception as e:
            print(e)
            print('something went wrong with bing api,try to resend request...')
            connection_attempt += 1
            if connection_attempt == 5:
                response.close()
                print('something went wrong with bing api,maximum retry reached!')
                return ['Sorry, I am having difficulties finding related information on our website to answer your question.', 0]
            # can not read result from bing

    # ans[ans_content, confidence_score]
    if response_data['answer'] != 'Sorry, I am having difficulties finding related information on our website to answer your question.' \
        and response_data['answer'] != 'No possible answer':
        return [response_data['answer'],response_data['confidenceScore']]
    elif response_data['possibleAnswer'] != 'possibleAnswer' and response_data['possibleAnswer'] != 'No possible answer':
        return [response_data['possibleAnswer'],response_data['confidenceScore']]

    return ['Sorry, I am having difficulties finding related information on our website to answer your question.', 0]

