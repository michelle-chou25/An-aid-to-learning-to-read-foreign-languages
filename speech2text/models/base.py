# coding: utf-8
import torch
import torch.nn as nn

# ASR 基类
class MASRModel(nn.Module):
    def __init__(self, **config):
        super().__init__()
        self.config = config

    @classmethod
    def load(cls, path): # load model
        # m = torch.load(path, map_location=torch.device('cpu'))
        m = torch.load(path)
        # state_dict = package["state_dict"]
        # config = package["config"]
        # m = cls(**config)
        # m.load_state_dict(package)
        return m

    def to_train(self):
        from .trainable import TrainableModel

        self.__class__.__bases__ = (TrainableModel,)
        return self

    def predict(self, *args):
        raise NotImplementedError()

    # -> texts: list, len(list) = B

    def _default_decode(self, yp, yp_lens):  # yp：tensor of cnn's output， yp_lens：tensor's length
        idxs = yp.argmax(1) # find the maximum element in each column
        texts = []
        for idx, out_len in zip(idxs, yp_lens):
            idx = idx[:out_len]
            text = ""
            last = None
            for i in idx:
                if i.item() not in (last, self.blank):
                    text += self.vocabulary[i.item()]
                last = i
            texts.append(text)
        return texts

    def decode(self, *outputs):  # texts -> list of size B
        return self._default_decode(*outputs)
