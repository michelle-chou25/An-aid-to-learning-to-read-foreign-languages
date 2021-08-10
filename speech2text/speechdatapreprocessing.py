#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import re
import joblib
import librosa
import torch
import wave
import numpy as np
import pandas as pd
from tqdm import tqdm
import random
from random import shuffle


# In[7]:


train_path_dir = '/home/nz32/speech2text/aishell/data_aishell/wav/train'
dev_path_dir = '/home/nz32/speech2text/aishell/data_aishell/wav/dev'
#数据预处理
train_files_path = []
dev_files_path = []

# 把所有train文件的名字放在装文件的list里
def recur_train(rootdir):
    for root, dirs, files in tqdm(os.walk(rootdir)):
        for file in files:
            if 'DS_Store' in file:
                continue
            train_files_path.append(os.path.join(root,file))
        for dir in dirs:
            recur_train(dir)
            
# 把所有dev文件的名字放在目录的list里
def recur_dev(rootdir):
    for root, dirs, files in tqdm(os.walk(rootdir)):
        for file in files:
            if 'DS_Store' in file:
                continue
            dev_files_path.append(os.path.join(root,file))
        for dir in dirs:
            recur_dev(dir)
            
recur_train(train_path_dir)
recur_dev(dev_path_dir)


# In[17]:


print('train_files_path len:', len(train_files_path))
print('dev_files_path len:', len(dev_files_path))
all_files_path = train_files_path+dev_files_path
print('all files len: ', len(all_files_path))


# In[15]:


# 读取transcript，处理成字典形式{'BAC009S0002W0125': '各地政府便纷纷跟进'}
_d={}
with open('/home/nz32/speech2text/aishell/data_aishell/transcript/aishell_transcript_v0.8.txt') as f:
    data = f.readlines()
    for i in tqdm(data):
        k,v = re.split('\s+', i, 1)
        _d[k.strip()] = v.replace('\n','').replace('\t','').replace(' ','')


# In[ ]:





# In[ ]:





# In[30]:


# 把wav文件与transcript对齐
res_train = []
for file in tqdm(train_files_path):
    file_name = file.split('/')[-1][:-4] # 从list末尾反向截取到导数第四个元素之间'BAC009S0016W0295'
    if file_name in _d:
        res_train.append((file, _d[file_name]))
        
res_dev =[]
for file in tqdm(dev_files_path):
    file_name = file.split('/')[-1][:-4]
    if file_name in _d:
        res_dev.append((file, _d[file_name]))
        


# In[38]:


all_words = list(set(''.join([v for v in _d.values()]))) #构造包含全部transcript中汉字的字典
all_words = ['_'] + all_words[:27] + [' '] + all_words[27:]


# In[41]:


len(all_words)


# In[45]:


pd.DataFrame(res_train).to_csv('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/train.index', index=False, header =None)
pd.DataFrame(res_dev).to_csv('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/dev.index', index=False, header =None)


# In[50]:


joblib.dump(all_words, 'labels.gz')


# In[51]:


with open('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/train.index') as f:
    idx = f.readlines()
idx = [x.strip().split(",", 1) for x in idx]


# In[53]:





# In[56]:


# test dump result
# all_words = joblib.load('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/labels.gz')
# len(res_train)
# train_pd = pd.DataFrame(res_train)
# train_pd


# In[57]:


all_words


# In[58]:





# In[59]:





# In[60]:





# In[ ]:




