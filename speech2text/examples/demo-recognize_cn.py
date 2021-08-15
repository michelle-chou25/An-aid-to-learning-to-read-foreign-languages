# coding: utf-8
import os
import sys
sys.path.append("..")
# from ..models.conv import GatedConv
# from ..config import pretrained_model_path
from speech2text.models.conv import GatedConv
from speech2text.config import pretrained_model_path

# modify pretrained_model_path to relative path if don't want to have ",,"
model = GatedConv.load(os.path.join('..', pretrained_model_path))
# text = model.predict("../data_aishell/BAC009S0765W0130.wav")
text = model.predict("../data_aishell/wav/test/S0764/BAC009S0764W0121.wav")

print("")
print("recognized result:")
print(text)
