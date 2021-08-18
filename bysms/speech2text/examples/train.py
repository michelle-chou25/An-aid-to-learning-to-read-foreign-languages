from . import _init_path
from speechmodels.conv import GatedConv

model = GatedConv.load("pretrained/gated-conv.pth")

model.to_train()

model.fit("train.manifest", "train.manifest")
