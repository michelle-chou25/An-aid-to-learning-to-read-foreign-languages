import re
import requests
from django.shortcuts import render
from .models import C2ecol
from Algorithm import word_seg
from Transformer import compose
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json


# translate
# def trasnlate(request):
#     if request.method == 'POST':
#         req = json.loads(request.body)
#         #distinguish if the input is url or paragraph
#         if re.match(r'^http(s)?:/{2}\w.+$', req):
#             print("This looks like a valid url.")
#             #TODO: grasp content rom the url
#             res = requests.get(req)
#             print(res.encoding)
#             content = res.text
#
#         else:
#             content = req
#
#
#






# word translation function, support both traditional and simplified Chinese
def word(request):
    if request.method == "POST":
        req = json.loads(request.body)
        word = req.get("word")
        result = C2ecol.objects.filter(traditional=word)
        if not result:
            result = C2ecol.objects.filter(simplified=word)
            if not result: # translation not found
                result = compose.get(word)
                return JsonResponse({"status":200,"data": result, "msg":"sentence query runs successfully."})
            else:
                data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                        'definitions': result[0].definitions[0]}
                return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
        else:
            data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                    'definitions': result[0].definitions[0]}
            return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})

def index(request):
    return render(request, 'index.html')

