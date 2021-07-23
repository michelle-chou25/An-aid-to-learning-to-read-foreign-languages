import requests
from bs4 import BeautifulSoup
import re
import lxml
req = requests()
url='https://zhuanlan.zhihu.com/p/336698982'
req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36")
req.add_header("GET",url)
req.add_header("Host")
req.add_header("Referer",)

res=requests.get(url) #requests模块会自动解码来自服务器的内容，可以使用res.encoding来查看编码
try:
    print(res.text)
except ConnectionError:
    print("Connection refused")

# res.encoding='utf-8'
html=res.content.decode('utf-8')
bs = BeautifulSoup(html, "lxml")
#a = bs.select('p')
a = bs.find_all('p')


