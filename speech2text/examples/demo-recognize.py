# coding: utf-8
import os
import sys

# sys.path.append('需要作为模块引入的路径')
# 添加当前路径的前一级文件作为源文件夹
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
# text = model.predict(r"../../speech2text/data_aishell/BAC009S0765W0131.wav")
text = model.predict(r'D:\CS5014\An-aid-to-learning-to-read-foreign-languages\speech2text\data_aishell\BAC009S0901W0151.wav')


print("")
print("识别结果:")
print(text)
