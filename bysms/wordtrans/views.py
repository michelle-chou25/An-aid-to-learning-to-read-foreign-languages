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
# from fake_useragent import UserAgent
import urllib.request
import ssl
import random
from hashlib import md5

ssl._create_default_https_context = ssl._create_stdlib_context

# Set your own appid/appkey.
appid = '20210625000871960'
appkey = '0QMEkNIdfW2LudZqhD4U'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'auto' # 自动检测语种
to_lang = 'en'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
baiduUrl = endpoint + path


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


# word translation function, support both traditional and simplified Chinese
def word(request):
    if request.method == "POST":
        req = json.loads(request.body)
        url = req['word']
        print(url)
        # tell an url from characters
        if re.match(r'^https?:/{2}\w.+$', url):
            print("This looks like a valid url.")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/51.0.2704.63 Safari/537.36'}
            req = urllib.request.Request(url=url, headers=headers)
            res = urllib.request.urlopen(req)
            data = res.read()
            data = data.decode('utf-8')

            bs = BeautifulSoup(data, "lxml")
            info_temp = bs.select('p', limit=1000)  # 提取网页文字中的前500个字符
            infoStr = ''
            for item in info_temp:
                if item.text:
                    infoStr = infoStr + item.text
            # call baidu translate API
            # Send request
            query = infoStr[0:500]
            salt = random.randint(32768, 65536)
            sign = make_md5(appid + query + str(salt) + appkey)

            # Build request
            baiduHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
            baiduPayload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
            r = requests.post(baiduUrl, params=baiduPayload, headers=baiduHeaders)
            result = r.json()

            tempResult = ''
            for item in result['trans_result']:
                tempResult = tempResult + item['dst']

            data = {"content": infoStr, "definitions": tempResult}
            return JsonResponse({"status": 200, "data": data, "msg": "url is translated successfully."})
        else:
            word = req.get("word")
            for ch in word:
                if u'\u4e00' <= ch <= u'\u9fff':  # Chinese
                    result = C2ecol.objects.filter(traditional=word)
                    if not result:
                        print("result: ", result)
                        result = C2ecol.objects.filter(simplified=word)
                        if not result:  # translation not found
                            result = compose.get(word)  # call paragraph translation model of English->Chinese
                            return JsonResponse({"status": 200, "data": result, "msg": "chinese sentence query runs successfully."})
                        else:
                            data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                    'definitions': result[0].definitions[0],"content":word}
                            return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
                    else:
                        data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                'definitions': result[0].definitions[0],"content":word}
                        return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
                else:  # English
                    result = compose.get_en(word)  # call paragraph translation model of Chinese->English
                    return JsonResponse({"status": 200, "data": result, "msg": "sentence query runs successfully."})

def index(request):
    return render(request, 'index.html')

