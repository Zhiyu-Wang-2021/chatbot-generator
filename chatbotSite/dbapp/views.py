from bson import ObjectId
from bson.json_util import dumps
from django.shortcuts import HttpResponse
import json
from dialogJson.answers import Answers
from dialogJson.dialog_json import DialogJson
from dialogJson.template_json import template as dialog_json_template
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from env import password
from webscraptool.get_answer_dict import get_dummy_answer, get_answer

USE_DUMMY_DATA = False

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
        try:
            data["answers"] = get_answer(data["url"])
        except IndexError:
            print('index error')
    print(data)
    ans = Answers(data)

    template = dialog_json_template

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
            elif node_title == "Appointment Info":
                template["dialog_nodes"][index]["output"]["generic"][0]["values"][0]["text"] = ans.get_appointment_info()
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
