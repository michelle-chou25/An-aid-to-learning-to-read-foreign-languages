"""PyAudio Example: Play a WAVE file."""
# coding: utf-8
# import pyaudio
# import wave
from tqdm import tqdm

# English speech recognition by using Google API
import speech_recognition as sr
# say = 'say something more than 5 words'
r = sr.Recognizer()

harvard = sr.AudioFile('../data_aishell/output.wav')
with harvard as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.record(source)
#Chinses
# test = r.recognize_google(audio_data=audio, language="cmn-Hans-CN", show_all=True)
#English
# google
# test = r.recognize_google(audio_data=audio, language="en-US", show_all=True)
# result = test['alternative'][0]
# witAI
wit_key = "OLY5OPYPMITJBN6Z7T2ERSL3MOQHFTJV"
result = r.recognize_wit(audio_data=audio, key=wit_key)

print("recognized result: ", result)

# flag = False
# for t in test['alternative']:
#     print(t)
#     if say in t['transcript']:
#         flag = True
#         break
# if flag:
#     print('Bingo')