from django.shortcuts import render
from .models import C2ecol
from Transformer import compose
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
import requests
from bs4 import BeautifulSoup
import re
import lxml
from fake_useragent import UserAgent

# word translation function, support both traditional and simplified Chinese
def word(request):
    if request.method == "POST":
        req = json.loads(request.body)
        # distinguish an url from a paragraph
        if re.match(r'^https?:/{2}\w.+$', req):
            print("This looks like a valid url.")
            ua = UserAgent(verify_ssl=False)
            headers = {"User-Agent": ua.random}
            res = requests.get(req, headers=headers)  # requests模块会自动解码来自服务器的内容，可以使用res.encoding来查看编码
            res.encoding = 'utf-8'
            try:
                a = res.text # test if get request is successfully
            except ConnectionError:
                print("Connection refused")
            # get content
            html = res.content.decode('utf-8')
            bs = BeautifulSoup(html, "lxml")
            info_temp = bs.select('p', limit=1000)  # 提取网页文字中的前1000个字符
            info = []
            for item in info_temp:
                if item.text:
                    info.append(item.text)
            #  TODO 把info回显到输入框
            #  TODO 调用百度API进行翻译

        else:
            word = req.get("word")
            for ch in word:
                if u'\u4e00' <= ch <= u'\u9fff':  # Chinese
                    result = C2ecol.objects.filter(traditional=word)
                    if not result:
                        result = C2ecol.objects.filter(simplified=word)
                        if not result: # translation not found
                            result = compose.get(word)  # call paragraph translation model of Chinese->English
                            return JsonResponse({"status":200,"data": result, "msg":"chinese sentence query runs successfully."})
                        else:
                            data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                    'definitions': result[0].definitions[0]}
                            return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
                    else:
                        data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                'definitions': result[0].definitions[0]}
                        return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
                else:  # English
                    result = compose.get_en(word)  # call paragraph translation model of English->Chinese
                    return JsonResponse({"status":200,"data": result, "msg":"sentence query runs successfully."})

def index(request):
    return render(request, 'index.html')

