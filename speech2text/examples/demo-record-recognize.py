import os
from speech2text.models.conv import GatedConv
from speech2text.config import pretrained_model_path
from examples import recordaudio

model = GatedConv.load(os.path.join('..',pretrained_model_path))
record("../data_aishell/output.wav", time=5)  # modify time to how long you want

text = model.predict("../data_aishell/output.wav")

print("")
print("识别结果:")
print(text)
