from django.shortcuts import render
from .models import C2ecol
from Transformer import compose
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json

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

