import speech_recognition
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
import calendar, time, os, sys
# from speech2text.models.conv import GatedConv
# from speech2text.config import pretrained_model_path
# from torch._C import import_ir_module



ssl._create_default_https_context = ssl._create_stdlib_context

# Set your own appid/appkey.
appid = '20210625000871960'
appkey = '0QMEkNIdfW2LudZqhD4U'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'auto'  # 自动检测语种
to_lang = 'en'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
baiduUrl = endpoint + path
wit_key = "OLY5OPYPMITJBN6Z7T2ERSL3MOQHFTJV"


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


# word translation function, support both traditional and simplified Chinese
def word(request):
    if request.method == "POST":
        req = json.loads(request.body)
        url = req['word']
        print(url)
        # tell an url from a paragraph / sentence
        if re.match(r'^https?:/{2}\w.+$', url):
            print("This looks like a valid url.")
            # id = req.get("id")
            # if id == "mainButton1":
            #         from_lang = "zh"
            #         to_lang = "en"
            # else:
            #     from_lang = "en"
            #     to_lang="zh"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/51.0.2704.63 Safari/537.36'}
            req = urllib.request.Request(url=url, headers=headers)
            res = urllib.request.urlopen(req)
            data = res.read()
            data = data.decode('utf-8')
            # 打印抓取的内容
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
            return JsonResponse({"status": 200, "data": data, "msg": "url translation runs successfully."})
        else:
            word = req.get("word")
            id = req.get("id")
            print(id)
            print(word)
            for ch in word:
                #     if u'\u4e00' <= ch <= u'\u9fff': #如果word中存在中文
                if id == "mainButton1" and u'\u4e00' <= ch <= u'\u9fff':  # 如果source为Chinese且源语言有中文
                    result = C2ecol.objects.filter(traditional=word)
                    if not result:
                        result = C2ecol.objects.filter(simplified=word)
                        if not result:  # translation not found
                            result = compose.get(word)
                            return JsonResponse(
                                {"status": 200, "data": result, "msg": "chinese sentence query runs successfully."})
                        else:
                            data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                    'definitions': result[0].definitions[0]}
                            return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
                    else:
                        data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                'definitions': result[0].definitions[0]}
                        return JsonResponse({"status": 200, "data": data, "msg": "word query runs successfully."})
                if id == "mainButton2" and (
                        u'\u0041' <= ch <= u'\u005a' or u'\u0061' <= ch <= u'\u007a'):  # 如果source为English且源语言有英文
                    result = C2ecol.objects.filter(definitions=word)
                    if not result:
                        result = compose.get_en(word)
                        return JsonResponse({"status": 200, "data": result, "msg": "sentence query runs successfully."})
                    else:
                        data = {"simplified": result[0].simplified, "pinyin": result[0].pinyin,
                                'definitions': result[0].definitions[0]}
                        return JsonResponse({"status": 200, "data": data, "msg": "english word query runs successfully."})
                else:
                    return JsonResponse({"status": 200, "data": word, "msg": "translate failed"})

# speech recognition
def recognize(requests):
    if requests.method == "POST":
        try:
            info_str=""
            type = requests.GET.get('type',1)
            f =requests.FILES.get("audio", None)
            ts = calendar.timegm(time.gmtime())
            filePath = os.path.join('./static/video/',str(ts)+'_'+f.name+'.wav')
            with open(filePath,'wb') as fp:
                for part in f.chunks():
                    fp.write(part)
            print(type)
            if type == '1':
                print("Chinese")

                # add the path of its uppper directory to path
                # os.path.join(os.getcwd(), "../..")
                # sys.path.append('..')
                # # 添加当前路径的前一级文件作为源文件夹,需要作为模块引入的路径
                # path = os.path.dirname(os.path.dirname(__file__))
                # print(path)
                # sys.path.append(path)
                #
                # # modify pretrained_model_path to relative path if don't want to have ",,"
                # # model = GatedConv.load(os.path.join('..', pretrained_model_path))
                # model=GatedConv.load(os.path.join('..', pretrained_model_path))
                # # model = GatedConv.load(r"D:\CS5014\An-aid-to-learning-to-read-foreign-languages\bysms\speech2text\pretrained\model_99.pth")
                # info_str = model.predict(filePath)

                # Using Google API
                r = speech_recognition.Recognizer()
                harvard = speech_recognition.AudioFile(filePath)
                with harvard as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.record(source)
                text = r.recognize_google(audio_data=audio, language="cmn-Hans-CN", show_all=True)
                info_str = text['alternative'][0]
                print("recognized result: ", info_str)
            else:
               print("English")
               r = speech_recognition.Recognizer()
               harvard = speech_recognition.AudioFile(filePath)
               with harvard as source:
                   r.adjust_for_ambient_noise(source, duration=0.5)
                   audio = r.record(source)
                # 用witAI识别
               # info_str = r.recognize_wit(audio_data=audio, key=wit_key)
               # print("recognized result: ", info_str)
                # 用google识别
               text = r.recognize_google(audio_data=audio, language="en-US", show_all=True)
               info_str = text['alternative'][0]
            data = {"content": info_str, "definitions": ""}
            return JsonResponse({"status": 200, "data": data, "msg": "speech recognized successfully."})
        except Exception as e:
            print(e)
            return JsonResponse({'Recognized text': '', 'code': 600, 'message': 'error occurs！'})

def index(request):
    return render(request, 'index.html')

