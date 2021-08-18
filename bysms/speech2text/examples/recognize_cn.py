# coding: utf-8
import os
import sys

# sys.path.append('需要作为模块引入的路径')
# 添加当前路径的前一级文件作为源文件夹
path = os.path.dirname(os.path.dirname(__file__))
print(path)
sys.path.append(path)
sys.path.append(os.getcwd())
sys.path.append("./")

from torch._C import import_ir_module
from speechmodels.conv import GatedConv
from config import pretrained_model_path

# modify pretrained_model_path to relative path if don't want to have ".."
model = GatedConv.load(os.path.join('..', pretrained_model_path))
text = model.predict(r"../../speech2text/data_aishell/BAC009S0901W0151.wav")

print("")
print("recognized result:")
print(text)
