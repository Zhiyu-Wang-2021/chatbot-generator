from bson import ObjectId
from bson.json_util import dumps
from django.shortcuts import HttpResponse
import json
from dialogJson.answers import Answers
from dialogJson.dialog_json import DialogJson
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from env import password
from webscraptool.get_answer_dict import get_dummy_answer, get_answer

USE_DUMMY_DATA = True

client = MongoClient("mongodb+srv://csp_chatbot_db:" + password + "@csp-chatbot.jwqkx3s.mongodb.net/?retryWrites=true&w=majority")
dialog_db = client["dialog_json"]
dialog_collection = dialog_db['dialog_json']
website_collection = dialog_db["websites_to_dialogs"]


@csrf_exempt
def generate_json(request):  # POST - provide url and generate
    data = json.loads(request.body)
    print(data)  # only url and ref
    # use the webscraptool to get data from url
    # {
    #     'phone': ['020 8363 4156'],
    #     'openingtimepage':
    #         ['Monday\n08:00-18:30\nTuesday\n08:00-18:30\nWednesday\n08:00-18:30\nThursday\n08:00-18:30\nFriday\n08:00-18:30\n'],
    #     'contactpage': [{'postcode': 'EN2 6NL', 'address': 'Enfield\n105-109 Chase Side\n', 'contact': ''}]
    # }
    if USE_DUMMY_DATA:
        data["answers"] = get_dummy_answer(data["url"])
    else:
        data["answers"] = get_answer(data["url"])
    ans = Answers(data)

    dj = DialogJson(ans)
    dialog_json = dj.get_json()

    dialog_filter = {"_id": ObjectId(data["ref"])}
    new_values = {"$set": dialog_json}
    dialog_collection.update_one(dialog_filter, new_values)

    return HttpResponse("success")


@csrf_exempt
def generate_json_from_existing(request):  # POST - provide url and generate
    data = json.loads(request.body)
    print(data)  # only url and ref
    # use the webscraptool to get data from url
    # {
    #     'phone': ['020 8363 4156'],
    #     'openingtimepage':
    #         ['Monday\n08:00-18:30\nTuesday\n08:00-18:30\nWednesday\n08:00-18:30\nThursday\n08:00-18:30\nFriday\n08:00-18:30\n'],
    #     'contactpage': [{'postcode': 'EN2 6NL', 'address': 'Enfield\n105-109 Chase Side\n', 'contact': ''}]
    # }
    if USE_DUMMY_DATA:
        data["answers"] = get_dummy_answer(data["url"])
    else:
        data["answers"] = get_answer(data["url"])
    ans = Answers(data)

    template = {"intents": [{"intent": "ask_more_info", "examples": [{"text": "are there any more things to share"}, {"text": "can you describe more"}, {"text": "can you direct me to some links on your website?"}, {"text": "I need more information"}, {"text": "please give me more info"}], "description": ""}, {"intent": "hours_info", "examples": [{"text": "Are you open on Christmas' Day?"}, {"text": "Are you open on Saturdays?"}, {"text": "Are you open on Sundays?"}, {"text": "what are the hours of operation for your Montreal trust"}, {"text": "what are you hours of operation in Toronto"}, {"text": "What are your hours?"}, {"text": "What are your hours of operation?"}, {"text": "What days are you closed on?"}, {"text": "What time are you open until?"}, {"text": "When are you open"}, {"text": "When do you close"}, {"text": "When do you open"}], "description": "-"}, {"intent": "location_info", "examples": [{"text": "do you have a hospital in Montreal"}, {"text": "Give me a list of locations"}, {"text": "List of location"}, {"text": "list of your locations"}, {"text": "locations in America"}, {"text": "Locations in Canada"}, {"text": "What are your locations?"}, {"text": "What's the address of your Toronto trust?"}, {"text": "what's the address of your Vancouver trust?"}, {"text": "Where are you physically located?"}, {"text": "Where are your trusts?"}, {"text": "where is your Toronto trust?"}], "description": "-"}, {"intent": "phone_number", "examples": [{"text": "I want to call this trust"}, {"text": "phone number"}, {"text": "what is your telephone number"}, {"text": "what's the number of this trust"}, {"text": "which number should I call"}], "description": ""}], "entities": [{"entity": "specific_location", "values": [{"type": "synonyms", "value": "center", "synonyms": []}, {"type": "synonyms", "value": "department", "synonyms": []}, {"type": "synonyms", "value": "floor", "synonyms": []}, {"type": "synonyms", "value": "unit", "synonyms": []}, {"type": "synonyms", "value": "wing", "synonyms": []}], "fuzzy_match": True}], "metadata": {"api_version": {"major_version": "v2", "minor_version": "2018-11-08"}}, "webhooks": [{"url": "https://bingaccessforwatson.azurewebsites.net/api/useQnA2ImproveAnswer?code=41mEZaj2kjJphYWmK6eHPFzQwQHLiVyW61QpEvrpGUcbAzFuAwDC3w==", "name": "main_webhook", "headers": [{"name": "Ocp-Apim-Subscription-Key", "value": "ef99b91a0209431cb66dd4d32a0b20c6"}, {"name": "Content-Type", "value": "application/json"}]}], "dialog_nodes": [{"type": "standard", "title": "Anything else", "actions": [{"name": "main_webhook", "type": "webhook", "parameters": {"q": "<? input.text ?>", "site": "https://www.gosh.nhs.uk"}, "result_variable": "search_result"}], "metadata": {"_customization": {"mcr": True}}, "conditions": "anything_else", "dialog_node": "Anything else", "previous_sibling": "node_5_1677172471791", "disambiguation_opt_out": True}, {"type": "standard", "title": "Hours Info", "output": {"generic": [{"values": [{"text": "Our trusts opens on:\n\nMonday\n08:00-18:30\n\nTuesday\n08:00-18:30\n\nWednesday\n08:00-18:30\n\nThursday\n08:00-18:30\n\nFriday\n08:00-18:30"}], "response_type": "text", "selection_policy": "sequential"}]}, "conditions": "#hours_info && !@specific_location", "dialog_node": "Hours Info", "previous_sibling": "Location Info"}, {"type": "standard", "title": "Location Info", "output": {"generic": [{"values": [{"text": "We are at this address: Great Ormond Street Hospital Great Ormond Street London WC1N 3JH"}], "response_type": "text", "selection_policy": "sequential"}]}, "metadata": {"_customization": {"mcr": False}}, "conditions": "#location_info && !@specific_location", "dialog_node": "Location Info", "previous_sibling": "Welcome"}, {"type": "standard", "output": {"generic": [{"values": [{"text": "The following links may be helpful:"}, {"text": "<a href=\"<? $search_result.bingResults[0].url ?>\"><? $search_result.bingResults[0].name ?></a>"}, {"text": "<a href=\"<? $search_result.bingResults[1].url ?>\"><? $search_result.bingResults[1].name ?></a>"}, {"text": "<a href=\"<? $search_result.bingResults[2].url ?>\"><? $search_result.bingResults[2].name ?></a>"}], "response_type": "text", "selection_policy": "multiline"}]}, "parent": "Anything else", "context": {}, "conditions": "#ask_more_info", "dialog_node": "node_10_1677157030611"}, {"type": "standard", "title": "Phone Info", "output": {"generic": [{"values": [{"text": "Please call us with this number: 020 7405 9200"}], "response_type": "text", "selection_policy": "sequential"}]}, "conditions": "#phone_number && !@specific_location", "dialog_node": "node_5_1677172471791", "previous_sibling": "Hours Info"}, {"type": "response_condition", "output": {"generic": [{"values": [{"text": "<? $search_result.answer ?>"}], "response_type": "text", "selection_policy": "multiline"}]}, "parent": "Anything else", "conditions": "$search_result.confidenceScore > 0.43", "dialog_node": "response_1_1676646061220", "previous_sibling": "node_10_1677157030611"}, {"type": "response_condition", "output": {"generic": [{"values": [{"text": "Sorry, I am not sure about this question based on the information on our website."}], "response_type": "text", "selection_policy": "sequential"}]}, "parent": "Anything else", "conditions": "anything_else", "dialog_node": "response_1_1676646061565", "previous_sibling": "response_8_1677157989078"}, {"type": "response_condition", "output": {"generic": [{"values": [{"text": "I'm not very sure about this. But this link can be helpful: "}, {"text": "<a href=\"<? $search_result.bingResults[0].url ?>\"><? $search_result.bingResults[0].name ?></a>"}, {"text": "<? $search_result.bingResults[0].snippet ?>"}], "response_type": "text", "selection_policy": "multiline"}]}, "parent": "Anything else", "conditions": "$search_result.confidenceScore > 0.2", "dialog_node": "response_8_1677157989078", "previous_sibling": "response_1_1676646061220"}, {"type": "standard", "title": "Welcome", "output": {"generic": [{"values": [{"text": "Hello, how can I help you?"}], "response_type": "text", "selection_policy": "sequential"}]}, "conditions": "welcome", "dialog_node": "Welcome"}], "counterexamples": [], "system_settings": {"nlp": {"model": "latest"}, "off_topic": {"enabled": True}, "disambiguation": {"prompt": "Didyoumean:", "enabled": False, "randomize": True, "max_suggestions": 5, "suggestion_text_policy": "title", "none_of_the_above_prompt": "Noneoftheabove"}, "system_entities": {"enabled": True}, "human_agent_assist": {"prompt": "Didyoumean:"}, "spelling_auto_correct": True}, "learning_opt_out": False, "name": "GeneratedSkill", "language": "en", "description": ""}

    for index in range(len(template["dialog_nodes"])):
        try:
            node_title = template["dialog_nodes"][index]["title"]
            if node_title == "Anything else":
                template["dialog_nodes"][index]["actions"][0]["parameters"]["site"] = data["site"]
            elif node_title == "Hours Info":
                template["dialog_nodes"][index]["output"]["generic"][0]["values"][0]["text"] = ans.get_hours_info()
            elif node_title == "Phone Info":
                template["dialog_nodes"][index]["output"]["generic"][0]["values"][0]["text"] = ans.get_phone_info()
            elif node_title == "Location Info":
                template["dialog_nodes"][index]["output"]["generic"][0]["values"][0]["text"] = ans.get_loc_info()
        except KeyError:
            print("KeyError with this node: " + str(index))
    print(template)

    dialog_filter = {"_id": ObjectId(data["ref"])}
    new_values = {"$set": template}
    dialog_collection.update_one(dialog_filter, new_values)

    return HttpResponse("success")


@csrf_exempt
def register_url(request):  # POST - register an url into the database
    data = json.loads(request.body)
    print(data)

    dialog_id = dialog_collection.insert_one({}).inserted_id
    website_collection.insert_one({
        "dialog_ref": dialog_id,
        "url": data["url"]
    })

    return HttpResponse(dialog_id)


def get_json(request):  # GET - get by id
    dialog_id = request.GET.get('id', '')
    this_dialog = dialog_collection.find_one({"_id": ObjectId(dialog_id)})
    if this_dialog:
        del this_dialog['_id']
        return HttpResponse(json.dumps(this_dialog))
    else:
        return HttpResponse("Not found")


@csrf_exempt
def list_url(request):  # GET
    urls = website_collection.find({})
    return HttpResponse(dumps(urls))


@csrf_exempt
def del_json(request):  # DEL - delete all
    website_collection.delete_many({})
    deleted_count = dialog_collection.delete_many({}).deleted_count

    return HttpResponse("deleted " + str(deleted_count) + " JSONs")
