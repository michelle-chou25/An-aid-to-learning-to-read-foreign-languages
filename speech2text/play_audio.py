"""PyAudio Example: Play a WAVE file."""
import pyaudio
import wave
from tqdm import tqdm
def play_audio(wave_path):
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
    datas = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()
play_audio("output.wav")