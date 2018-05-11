# -*- coding:utf-8 -*-
import torch
import os
import json
import numpy as np
from PIL import Image
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from torch import nn, optim
from torchvision import datasets, transforms

with open('E:\hao.shen\Projects\FontConfusion\char_map.txt', 'r') as f:
    content = f.readlines()
    char_map = json.loads(content[0])
    r_char_map = {}
    for item in char_map.items():
        r_char_map.update({str(item[1]): item[0]})

def default_loader(path):
    return Image.open(path).convert('L')

class MyDataset(Dataset):
    def __init__(self, path, transform=None, target_transform=None, loader=default_loader):
        imgs = []
        files = os.listdir(path)
        for file in files:
            fp = path + '/' + file
            _label = file.split('_')[0]
            try:
                label = char_map[_label]
            except KeyError:
                continue
            imgs.append((fp, label))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        fp, label = self.imgs[index]
        img = self.loader(fp)
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.imgs)

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Sequential(torch.nn.Conv2d(1, 32, 3, 1, 1), torch.nn.ReLU(), torch.nn.MaxPool2d(2))
        self.conv2 = torch.nn.Sequential(torch.nn.Conv2d(32, 64, 3, 1, 1), torch.nn.ReLU(), torch.nn.MaxPool2d(2))
        self.conv3 = torch.nn.Sequential(torch.nn.Conv2d(64, 64, 3, 1, 1), torch.nn.ReLU())
        self.dense = torch.nn.Sequential(torch.nn.Linear(64*7*7, 256), torch.nn.ReLU(), torch.nn.Linear(256, 3512))

    def forward(self, x):
        conv1_out = self.conv1(x)
        conv2_out = self.conv2(conv1_out)
        conv3_out = self.conv3(conv2_out)
        res = conv3_out.view(conv3_out.size(0), -1)
        out = self.dense(res)
        return out



def pred(pred_path, batch_size=64):
    data_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])  # -0.5 & /0.5   3 channel: transforms.Normalize([a, b,c], [d, e, f])

    test_dataset = MyDataset(path=pred_path, transform=data_tf)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model = Net()
    model.load_state_dict(torch.load('E:\\hao.shen\\Projects\\FontConfusion\\params3.pkl'))
    model.eval()
    correct_dict = {}
    for data in test_loader:
        img, label = data
        label = torch.LongTensor([int(x) for x in label])
        with torch.no_grad():
            img = Variable(img)  # Forward without caching
            label = Variable(label)
            out = model(img)
            _, pred = torch.max(out, 1)
            correct_dict.update(dict(zip([chr(int(r_char_map[str(x.item())])) for x in label], [chr(int(r_char_map[str(y.item())])) for y in pred])))
    with open('E:\\hao.shen\\Projects\\FontConfusion\\newmap\\new_char_map.txt', 'w') as f:
        correct_dict[u'服'] = '司'
        f.write(json.dumps(correct_dict))



if __name__ == '__main__':
    pred('tyc_chars')
