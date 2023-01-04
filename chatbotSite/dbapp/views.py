from bson import ObjectId
from django.shortcuts import HttpResponse
import json
from dialogJson.answers import Answers
from dialogJson.dialog_json import DialogJson
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from env import password

client = MongoClient("mongodb+srv://csp_chatbot_db:" + password + "@csp-chatbot.jwqkx3s.mongodb.net/?retryWrites=true&w=majority")
db = client["dialog_json"]
dialog_collection = db['dialog_json']


@csrf_exempt
def generate_json(request):  # POST - provide answers and get the ref id of dialog json in the db
    data = json.loads(request.body)
    print(data)
    ans = Answers(data)

    dj = DialogJson(ans)
    dialog_json = dj.get_json()
    dialog_id = dialog_collection.insert_one(dialog_json).inserted_id
    return HttpResponse(dialog_id)


def get_json(request):  # GET - get by id
    dialog_id = request.GET.get('id', '')
    this_dialog = dialog_collection.find_one({"_id": ObjectId(dialog_id)})
    if this_dialog:
        del this_dialog['_id']
        return HttpResponse(str(this_dialog))
    else:
        return HttpResponse("Not found")


@csrf_exempt
def del_json(request):  # DEL - delete all
    deleted_count = dialog_collection.delete_many({}).deleted_count

    return HttpResponse("deleted " + str(deleted_count) + " JSONs")
