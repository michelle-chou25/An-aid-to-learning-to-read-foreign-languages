import os
import sys
from speech2text.examples.recordaudio import record_audio
from speech2text.models.conv import GatedConv
from speech2text.config import pretrained_model_path

sys.path.append("..")
model = GatedConv.load(os.path.join('..', pretrained_model_path))
record_audio("../data_aishell/output.wav", record_second=5) # modify time to how long you want
print("Recognizing...")
text = model.predict("../data_aishell/output.wav")

print("")
print("识别结果:")
print(text)
