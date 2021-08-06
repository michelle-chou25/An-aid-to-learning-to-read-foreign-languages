from tqdm import tqdm
import pyaudio
import wave

#This function is used to record user's audio input and save it as output.wav
#



#  停止说话时停止录音
from tqdm import tqdm
import pyaudio
import wave
import numpy as np
from scipy import fftpack

#This function is used to record user's audio input and save it as output.wav
#
def record_audio(wave_out_path, threshold=7000):
    CHUNK = 1024  #chunk size
    FORMAT = pyaudio.paInt16 # number of bits
    CHANNELS = 2  # number of channels
    RATE = 44100  # sample rate: times of sampling in each second
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    print("* start recording")
    frames = []
    stopflag = 0
    stopflag2 = 0
    while True:
        data=stream.read(CHUNK)
        wf.writeframes(data)
        rt_data = np.frombuffer(data, np.dtype('<i2')) # convert input stream to ndarray, return type is int16
        #  Fourier transform, get grequency distribution of input steam
        fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=False)
        fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1] #取振幅绝对值列表的前一半
        # 测试阈值，输出值用来判断阈值
        # print(sum(fft_data) // len(fft_data))
        #
        if sum(fft_data) // len(fft_data) > threshold:  #
            stopflag += 1
        else:
            stopflag2 += 1
        oneSecond = int(RATE/CHUNK)
        if (stopflag2 + stopflag) > oneSecond:  # silence time is larger than one second
            if stopflag2 > oneSecond//3*2:
                break
            else:
                stopflag2 = 0
                stopflag = 0
        print("* done recording")
        frames.append(data)
    # wf.writeframes(b''.join(frames))
    # print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()


record_audio("output.wav", threshold=7000)
