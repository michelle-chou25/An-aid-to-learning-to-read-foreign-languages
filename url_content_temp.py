import requests
from bs4 import BeautifulSoup
import re
import lxml
from fake_useragent import UserAgent

ua=UserAgent()
# print(ua.data_browsers)
req='https://zhuanlan.zhihu.com/p/336698982'
# get html
if re.match(r'^https?:/{2}\w.+$', req):
    print("This looks like a valid url.")
    headers={"User-Agent": ua.random}
    res=requests.get(req, headers=headers) #requests模块会自动解码来自服务器的内容，可以使用res.encoding来查看编码
    res.encoding='utf-8'
    try:
        a = res.text
    except ConnectionError:
        print("Connection refused")
    #get content
    # res.encoding='utf-8'
    html=res.content.decode('utf-8')
    bs = BeautifulSoup(html, "lxml")
    info_temp = bs.select('p', limit=500) #提取网页文字中的前1000个字符
    info=[]
    for item in info_temp:
        if item.text:
            info.append(item.text)
    print(info)

    # a = bs.find_all('p')
    # info = re.match("<([a-zA-Z]*)>\w*</\\1>", info)
    # print(info)


else:
    print("This looks invalid.")





