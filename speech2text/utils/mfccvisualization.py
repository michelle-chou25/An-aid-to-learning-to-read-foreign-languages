#!/usr/bin/env python
# coding: utf-8

# In[11]:


with open('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/train.index', encoding='utf-8') as f:
    idx = f.readlines()
idx = [x.strip().split(",", 1) for x in idx]


# In[12]:


idx


# In[16]:


path=idx[0][0]
text=idx[0][1]


# In[17]:


path


# In[19]:


text


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import librosa.display
from librosa.feature import mfcc


# In[20]:


import librosa
import librosa.display
import matplotlib.pyplot as plt
y, sr = librosa.load(path)
plt.plot(y);
plt.title('Signal');
plt.xlabel('Time (samples)');
plt.ylabel('Amplitude');


# In[15]:


# y,sr=librosa.load(path,sr=None) #y是原始波形的时域序列


# In[ ]:


# Fourier transformation

# The audio signal consists of several single frequency sound waves. When sampling the signal over a period of time, we only capture the amplitude. Fourier transform is a mathematical formula that allows us to decompose a signal into a single frequency and frequency amplitude. In other words, it converts the signal from time domain to frequency domain. The result is called the spectrum.

# This is possible because each signal can be decomposed into a set of sine and cosine waves, which together are equal to the original signal. This is a famous theorem called Fourier theorem.

# Fast Fourier transform (FFT) is an algorithm that can effectively calculate Fourier transform. It is widely used in signal processing. I'll use this algorithm in the window clip of the sample audio.


# In[23]:


import numpy as np
n_fft = 2048
ft = np.abs(librosa.stft(y[:n_fft], hop_length = n_fft+1))
plt.plot(ft)
plt.title('Spectrum')
plt.xlabel('Frequency Bin')
plt.ylabel('Amplitude')


# In[ ]:


# # The spectrum can be regarded as a stack of FFT. 
# When the signal changes with time at different frequencies, this is a method to intuitively 
# represent the loudness or amplitude of the signal. 
# There are other details when calculating the spectrum. The y-axis is converted to a 
# logarithmic scale, and the color size is converted to decibels (the amplitude can 
#                                                                 be regarded as a logarithmic scale of the amplitude). This is because humans can only perceive a very small range of concentrated frequencies and amplitudes.


# In[24]:


spec = np.abs(librosa.stft(y, hop_length=512))
spec = librosa.amplitude_to_db(spec, ref=np.max)
librosa.display.specshow(spec, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')


# In[ ]:


Because humans do not perceive frequencies in a linear range. We are better at detecting low-frequency differences than high-frequency differences. For example, we can easily distinguish the difference between 500 Hz and 1000 Hz, but even if the distance between them is the same, it is difficult to distinguish the difference between 10000 Hz and 10500 Hz.
In 1937, Stevens, Volkmann and Newmann proposed a pitch unit to make an equal pitch distance sound equal to the audience. This is called the mel scale. We perform mathematical operations on the frequency to convert it to mel scale.


# In[ ]:


Mel spectrum is a spectrum whose frequency is converted to mel scale


# In[29]:


mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=1024)
mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
librosa.display.specshow(mel_spect, y_axis='mel', fmax=8000, x_axis='time')
plt.title('Mel Spectrogram')
plt.colorbar(format='%+2.0f dB')


# In[26]:





# In[31]:


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
    plt.xlabel('Time')
    plt.ylabel('MFCC Coefficient')
    plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    ax.set_xticks(np.arange(0, 13, 2), minor=False);
    plt.show()
    return path

# example
visulize(0)


# In[ ]:





# In[ ]:




