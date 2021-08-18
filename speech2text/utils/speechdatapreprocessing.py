# coding: utf-8

# In[1]:

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

# """
# This is used to extract the corresponding relationship between audio files and their text, dev_index is like:
# [['/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/dev/S0754/BAC009S0754W0292.wav',
#   '纽交所其后通过推特表示'],
#  ['/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/dev/S0754/BAC009S0754W0205.wav',
#   '日前国家发展改革委发出通知'],
#  ['/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/dev/S0754/BAC009S0754W0131.wav',
#   '自明年一月一日开始'],
#  ['/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/dev/S0754/BAC009S0754W0182.wav',
#   '美国养老类地产的潜力巨大'],
#  ['/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/dev/S0754/BAC009S0754W0256.wav',
#   '针对美联航的地面禁令才被取消']]
#
# labels.gz is like:
#   ['_',
#  '战',
#  '嵩',
#  '曰',
#  '彻',
#  '纾',
#  '慷',
#  '冥',
#  '返',
#  '诈']
# """
# ## 读取wav文件

# In[21]:


train_path_dir = '/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/train'
dev_path_dir = '/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/dev'
test_path_dir = '/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/wav/test'

# In[22]:


train_files_path = []
dev_files_path = []
test_files_path = []
def recur_train(rootdir):
    for root, dirs, files in tqdm(os.walk(rootdir)):
        for file in files:
            if 'DS_Store' in file:
                continue
            train_files_path.append(os.path.join(root,file))
        for dir in dirs:
            recur_train(dir)

def recur_dev(rootdir):
    for root, dirs, files in tqdm(os.walk(rootdir)):
        for file in files:
            if 'DS_Store' in file:
                continue
            dev_files_path.append(os.path.join(root,file))
        for dir in dirs:
            recur_dev(dir)

def recur_test(rootdir):
    for root, dirs, files in tqdm(os.walk(rootdir)):
        for file in files:
            # if 'DS_Store' in file:
            #     continue
            test_files_path.append(os.path.join(root,file))
        for dir in dirs:
            recur_test(dir)

recur_train(train_path_dir)
recur_dev(dev_path_dir)
recur_test(test_path_dir)
# wav_paths = [x for x in all_files_path if 'wav' in x]


# In[25]:


print('train_files_path len:', len(train_files_path))
print('dev_files_path len:', len(dev_files_path))
print('test_files_path len:', len(test_files_path))
all_files_path = train_files_path+dev_files_path+test_files_path


# In[26]:


print(len(all_files_path))
all_files_path


# ## readtranscript file

# In[110]:


#convert to dict type {'BAC009S0002W0122': '而对楼市成交抑制作用最大的限购'}


# In[27]:


_d = {}
with open('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/transcript/aishell_transcript_v0.8.txt', encoding='utf-8') as f:
    data = f.readlines()
    for i in tqdm(data):
        k, v = re.split('\s+', i, 1)
        _d[k.strip()] = v.replace('\n','').replace('\t','').replace(' ','')


# ## 生成train.index, dev.index和labels.gz三个文件

# In[29]:


res_train = []
for file in tqdm(train_files_path):
    file_name = file.split('/')[-1][:-4]
    if file_name in _d:
        res_train.append((file, _d[file_name]))
res_dev = []
for file in tqdm(dev_files_path):
    file_name = file.split('/')[-1][:-4]
    if file_name in _d:
        res_dev.append((file, _d[file_name]))

res_test = []
for file in tqdm(test_files_path):
    file_name = file.split('/')[-1][:-4]
    if file_name in _d:
        res_test.append((file, _d[file_name]))


# In[31]:


all_words = list(set(''.join([v for v in _d.values()])))
all_words = ['_'] + all_words[:27] + [' '] + all_words[27:]


# In[43]:


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

pd.DataFrame(res_train).to_csv('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/train.index',index=False,header=None)
pd.DataFrame(res_dev).to_csv('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/dev.index',index=False,header=None)
pd.DataFrame(res_test).to_csv('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/test.index',index=False,header=None)
joblib.dump(all_words, '/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/labels.gz')


# In[13]:


# #读取看看
# with open('data_aishell/train.index') as f:
#     idx = f.readlines()
# idx = [x.strip().split(",", 1) for x in idx]

# all_words = joblib.load('data_aishell/labels.gz')



