# -*- coding:utf -*-
import requests
import re
import os
from urllib.request import urlretrieve

path = os.path.join(os.getcwd(), 'woff')
if not os.path.exists(path):
    os.mkdir(path)

def request_get(url):
    headers = {}
    headers['headers'] = {
        # 'Accept':'*/*',
        # 'Accept-Encoding':'gzip, deflate, sdch',
        # 'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'close',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    return requests.get(url, **headers)

def downwoff():
    url = 'https://sh.tianyancha.com/search'
    r = request_get(url)
    font_url = re.findall(r'(https://static\.tianyancha.com/fonts-styles/css/.*/)font\.css', r.text)[0] + 'tyc-num.woff'
    font_url = font_url.replace('css', 'fonts')
    urlretrieve(font_url, path + '\\tyc-num.woff')
    tag = font_url[49: -13].replace('/', '_')
    return tag

downwoff()