# coding: utf-8

# import librosa
# import numpy as np
# import torch
# import wave
# import soundfile as sf
#
# #  语音数据集预处理，
# # 首尾端的静音切除，降低对后续步骤造成的干扰，静音切除的操作一般称为VAD。
# # 声音分帧，也就是把声音切开成一小段一小段，每小段称为一帧，使用移动窗函数来实现，不是简单的切开，各帧之间一般是有交叠的。
# sample_rate = 16000
# window_size = 0.02
# window_stride = 0.01
# n_fft = int(sample_rate * window_size)
# win_length = n_fft
# hop_length = int(sample_rate * window_stride)
# window = "hamming"
#
# # 把wav文件转为ndarray，然后获取短时傅里叶变换后的振幅
# def load_audio(wav_path, normalize=True):  # -> numpy array
#     with wave.open(wav_path) as wav:
#         wav = np.frombuffer(wav.readframes(wav.getnframes()), dtype="int16")
#         wav = wav.astype("float")
#     if normalize:  # 让均值为0，方差为1
#         return (wav - wav.mean()) / wav.std()
#     else:
#         return wav
#
#
# # 返回wav文件傅里叶变换后的振幅
# def spectrogram(wav, normalize=True):
#     """ 短时傅里叶变换， 返回复数矩阵使得D(f, t)
#     复数的实部：np.abs(D(f, t))频率的振幅
#     复数的虚部：np.angle(D(f, t))频率的相位
#     """
#     D = librosa.stft(
#         wav, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window
#     )  # n_fft：FFT窗口大小，n_fft=hop_length+overlapping
#     # hop_length：帧移，如果未指定，则默认win_length / 4。
#     # win_length：每一帧音频都由window（）加窗。窗长win_length，然后用零填充以匹配N_FFT。默认win_length=n_fft。
#
#     spec, phase = librosa.magphase(D) # 返回振幅，相位
#     spec = np.log1p(spec) # 对振幅平滑处理
#     spec = torch.FloatTensor(spec) # 把振幅矩阵转换为torch张量，运行在cpu上，如果要运行在GPU上，改为torch.cuda.FloatTensor(spec)
#
#     if normalize:
#         spec = (spec - spec.mean()) / spec.std()
#
#     return spec
from librosa.feature import mfcc
import librosa
import numpy as np
import torch

def spectrogram(path, normalize=True):
    wav, sr = librosa.load(path, sr=None)
    spec = mfcc(wav, sr)  # 提取MFCC特征
    # np.log1p(spec)
    # spec = np.log1p(spec)  # 对MFCC平滑处理
    # spec = torch.FloatTensor(spec)  # 
    spec = torch.cuda.FloatTensor(spec) # 把MFCC矩阵转换为torch张量，运行在gpu上，如果要运行在cpu上，改为torch.FloatTensor(spec)
    if normalize:
        spec = (spec - spec.mean()) / spec.std()
    return spec