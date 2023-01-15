from bson import ObjectId
from django.shortcuts import HttpResponse
import json
from dialogJson.answers import Answers
from dialogJson.dialog_json import DialogJson
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from env import password

client = MongoClient("mongodb+srv://csp_chatbot_db:" + password + "@csp-chatbot.jwqkx3s.mongodb.net/?retryWrites=true&w=majority")
dialog_db = client["dialog_json"]
dialog_collection = dialog_db['dialog_json']
website_collection = dialog_db["websites_to_dialogs"]


@csrf_exempt
def generate_json(request):  # POST - provide url and generate
    data = json.loads(request.body)
    print(data)  # only url and ref
    # use the webscraptool to get data from url
    data["answers"] = {
        'phone': [{
                'title': '', 'num': 'Tel: 01302 868421'
            }],
        'openingtimepage': [{
                'title': 'Opening Times',
                'time': 'Opening Times\nPlease note on two Wednesdays per month we close at 12:00 for training.\nMonday\n07.00 - 18:00\nTuesday\n08:00 - 20.30\nWednesday\n08:00 - 18:00\nThursday\n07:00 - 18:00\nFriday\n08:00 - 18:00\n'
            }],
        'contactpage': [{
                'postcode': 'Doncaster, DN11 0LP',
                'address': 'Rossington\nGrange Lane\nThe Rossington Practice\n',
                'contact': 'Doncaster, DN11 0LPTel: 01302 868421\n'
            }]
        }
    ans = Answers(data)

    dj = DialogJson(ans)
    dialog_json = dj.get_json()

    dialog_filter = {"_id": ObjectId(data["ref"])}
    new_values = {"$set": dialog_json}
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


def list_url(request):  # GET
    urls = website_collection.find({})
    return HttpResponse(urls)


@csrf_exempt
def del_json(request):  # DEL - delete all
    website_collection.delete_many({})
    deleted_count = dialog_collection.delete_many({}).deleted_count

    return HttpResponse("deleted " + str(deleted_count) + " JSONs")
