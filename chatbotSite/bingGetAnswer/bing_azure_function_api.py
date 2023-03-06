# ---------------------------bing api--------------------------------------
import requests
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna

def get_bing_result(domain_url, question):
    url = "https://bingaccessforwatson.azurewebsites.net/api/useQnA2ImproveAnswer"

    querystring = {"code":"41mEZaj2kjJphYWmK6eHPFzQwQHLiVyW61QpEvrpGUcbAzFuAwDC3w=="}


    payload = {
        "q": question,
        "site": 'https://' + domain_url
    }
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": "ef99b91a0209431cb66dd4d32a0b20c6"
    }
    
    try:
        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
        response_data = json.loads(response.text)
    except Exception as e:
        print(e)
        # can not read result from bing
        return ['Sorry, I am having difficulties finding related information on our website to answer your question.', 0]
    
    # # ans[ans_content, confidence_score]
    if response_data['answer'] != 'Sorry, I am having difficulties finding related information on our website to answer your question.':
        return [response_data['answer'],response_data['confidenceScore']]
    elif response_data['possibleAnswer'] != 'possibleAnswer':
        return [response_data['possibleAnswer'],response_data['confidenceScore']]
    
    return ['Sorry, I am having difficulties finding related information on our website to answer your question.', 0]

