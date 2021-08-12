#!/usr/bin/env python
# coding: utf-8

# In[1]:


with open('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/train.index', encoding='utf-8') as f:
    idx = f.readlines()
idx = [x.strip().split(",", 1) for x in idx]


# In[8]:


idx


# In[10]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import librosa.display
from librosa.feature import mfcc


n_mfcc=20 # mfcc 保留20维
# 举例可视化mfcc图   
def visulize(index):
    path = idx[index][0]
    text = idx[index][1]
    print('Audio text: ', text)
    
    y,sr=librosa.load(path,sr=None) #y是原始波形的时域序列
    plt.figure(figsize=(12,3))
    librosa.display.waveplot(y,sr)
    plt.title('Raw Audio Signal')
    plt.xlabel('Time')
    plt.ylabel('Audio Amptitude')
#     plot.show()
    
    feature= mfcc(y,sr)
    print('Shape of MFCC:', feature.shape)
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(111)
    im = ax.imshow(feature, cmap=plt.cm.jet, aspect='auto')
    plt.title('Normalized MFCC')
    plt.ylabel('Time')
    plt.xlabel('MFCC Coefficient')
    plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    ax.set_xticks(np.arange(0, 13, 2), minor=False);
    plt.show()
    return path

# example
visulize(0)


# In[ ]:





# In[ ]:




