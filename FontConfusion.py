# -*- coding:utf-8 -*-
from ExptPng import ExptPng
from CharOCR import pred
from urllib.request import urlretrieve
from CorrectHtml import correctHtml

def fontconfusion(font_url):
    path = 'E:/hao.shen/Projects/FontConfusion/woff/tyc-num.woff'
    # urlretrieve(font_url, 'E:\\hao.shen\\Projects\\FontConfusion\\woff\\tyc-num.woff')
    ExptPng(path).main()
    pred('E:\hao.shen\Projects\\FontConfusion\\tyc_chars')
    print('生成new_char_map')
    # correctHtml(tag)

if __name__ == '__main__':
    url = u'https://static.tianyancha.com/fonts-styles/fonts/53/5339147f/tyc-num.woff'
    fontconfusion(url)
