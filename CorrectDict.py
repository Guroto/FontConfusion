# -*- coding:utf-8 -*-
import numpy as np
import os
from PIL import Image
import json

path = os.path.join(os.getcwd(), 'newmap')
if not os.path.exists(path):
    os.mkdir(path)

chars3724 = os.listdir('chars3724')
chars3724_dict = {}
for file in chars3724:
    img = Image.open('chars3724/' + file)
    pixmap = []
    for x in range(28):
        for y in range(28):
            pixmap.append(img.getpixel((x, y)))
    pixmap_np = np.array(pixmap)
    chars3724_dict.update({file: pixmap_np})

tyc_chars = os.listdir('tyc_chars')
tyc_dict = {}

for file in tyc_chars:
    img = Image.open('tyc_chars/' + file)
    pixmap = []
    for x in range(28):
        for y in range(28):
            pixmap.append(img.getpixel((x,y)))
    pixmap_np = np.array(pixmap)
    tyc_dict.update({file: pixmap_np})

correct_dict = {}
for item in tyc_dict.items():
    tyc_chr = item[0]
    min_compare = float('inf')
    train_chr = ''
    for item_train in chars3724_dict.items():
        compare = np.fabs(item_train[1] - item[1])
        min_compare = min(np.std(compare), min_compare)
        if min_compare == np.std(compare):
            train_chr = item_train[0]
    correct_dict.update({tyc_chr[:-4]: train_chr[:-4]})

def dump_correct_dict(tag):
    with open(path +'\\{}.txt'.format(tag), 'w') as f:
        f.write(json.dumps(correct_dict))