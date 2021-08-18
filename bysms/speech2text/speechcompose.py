from .speechmodels.conv import GatedConv
from .config import pretrained_model_path
from .feature import spectrogram
import torch
import os
import traceback

def get(path):
    try:
        # model=model=GatedConv.load(os.path.join('..speech2text.pretrained', pretrained_model_path))
        model = GatedConv.load(
            r"D:\CS5014\An-aid-to-learning-to-read-foreign-languages\bysms\speech2text\pretrained\model_99.pth")
        model.eval()
        # spec = feature.spectrogram(wav)
        spec = spectrogram(path)
        spec.unsqueeze_(0) # dimension expansion
        x_lens = spec.size(-1)  # number of columns of MFCC
        out = model.cnn(spec) # out is the probabilities of each syllable
        out_len = torch.tensor([out.size(-1)])  # number of characters
        text = model.decode(out, out_len)
        model.train()
        print("text: ", text)
        return text[0]
    except Exception as e:
        print(e)
        print(traceback.print_exc())

