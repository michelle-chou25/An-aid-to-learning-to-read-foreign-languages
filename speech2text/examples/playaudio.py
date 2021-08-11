"""PyAudio Example: Play a WAVE file."""
# coding: utf-8
import pyaudio
import wave
from tqdm import tqdm

def play_audio(wave_path):
    """
    This function is to play
    """
    CHUNK = 1024
    wf = wave.open(wave_path, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # read data
    data = wf.readframes(CHUNK)
    # play stream (3)
    frames = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        frames.append(data)
    for d in tqdm(frames):
        stream.write(d)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()
play_audio("../data_aishell/output.wav")


# speech recognition
import speech_recognition as sr
say = 'say something more than 5 words'
r = sr.Recognizer()

harvard = sr.AudioFile('output.wav')
with harvard as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.record(source)
test = r.recognize_google(audio_data=audio, language="cmn-Hans-CN", show_all=True)
# test = r.recognize_google(audio_data=audio, language="en-US", show_all=True)
print(test)

flag = False
for t in test['alternative']:
    print(t)
    if say in t['transcript']:
        flag = True
        break
if flag:
    print('Bingo')