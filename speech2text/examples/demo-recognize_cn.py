# coding: utf-8
import os
import sys

# sys.path.append('the path needed to be imported as a modual')
# add the path of its uppper directory to path
path = os.path.dirname(os.path.dirname(__file__)) 
print(path)
sys.path.append(path)


from torch._C import import_ir_module
# from models.conv import GatedConv
# from config import pretrained_model_path
# sys.path.append(os.getcwd())
# from ..models.conv import GatedConv
# from ..config import pretrained_model_path
from speech2text.models.conv import GatedConv
# from speech2text import models
from speech2text.config import pretrained_model_path
# from models.conv import GatedConv
# from config import pretrained_model_path

# modify pretrained_model_path to relative path if don't want to have ",,"
model = GatedConv.load(os.path.join('..', pretrained_model_path))
text = model.predict("data_aishell/BAC009S0765W0130.wav")

print("")
print("recognized result:")
print(text)
