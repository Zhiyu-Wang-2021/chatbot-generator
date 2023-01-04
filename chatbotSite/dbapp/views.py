from django.shortcuts import HttpResponse
import json
from dialogJson.answers import Answers
from dialogJson.dialog_json import DialogJson
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test(request):
    data = json.loads(request.body)
    print(data)
    ans = Answers(data)

    dj = DialogJson(ans)
    test_obj = dj.get_json()
    return HttpResponse(json.dumps(test_obj))
