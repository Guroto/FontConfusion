# -*- coding:utf-8 -*-
import json
import re
from bs4 import BeautifulSoup
from DownWoff import request_get

def correctHtml():
    with open('newmap/{}.txt'.format('new_char_map'), 'r') as f:
        newmap = json.loads(f.readlines()[0])
    url = 'https://hangzhou.tianyancha.com/search/oc36-la3/p1'
    r = request_get(url)

    content = r.text
    soup = BeautifulSoup(content, 'lxml')
    tyc_nums = soup.find_all('text')
    for num in tyc_nums:
        print(num)
        num = num.text
        new_num = ''
        for char in num:
            try:
                _chr = newmap[char]
            except KeyError:
                _chr = char
            new_num += _chr
        print(new_num)

if __name__ == '__main__':
    correctHtml()