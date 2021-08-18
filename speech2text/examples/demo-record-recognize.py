import os
import sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
sys.path.append(os.getcwd())
sys.path.append("./")

from recordaudio import record_audio
from models.conv import GatedConv
from config import pretrained_model_path

sys.path.append("..")
model = GatedConv.load(os.path.join('..', pretrained_model_path))
record_audio("../data_aishell/output.wav", record_second=5) # modify time to how long you want
print("Recognizing...")
text = model.predict("../data_aishell/output.wav")

print("")
print("Rercognized result:", text)
