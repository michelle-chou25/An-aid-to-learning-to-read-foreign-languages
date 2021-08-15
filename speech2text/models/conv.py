# coding: utf-8
import torch
import torch.nn as nn
from torch.nn.functional import hardtanh
from torch.nn.utils import weight_norm
from .base import MASRModel
import speech2text.feature
import speech2text.config

# conv unit
class ConvBlock(nn.Module):
    def __init__(self, conv, p):
        super().__init__()
        self.conv = conv
        nn.init.kaiming_normal_(self.conv.weight)  # initilize parameters by kaiming norm distribution
        self.conv = weight_norm(self.conv)  # a reparameterization to speed up the convergence
        # 1 dimentsion GLU, made from a Relu+Sigmoid
        self.act = nn.GLU(1)
        # self.act = nn.Hardtanh()
        #  randomly exclude some neurons from the computation, that is, to achieve local connection.
        self.dropout = nn.Dropout(p, inplace=True)

    def forward(self, x):  # propogation
        x = self.conv(x)
        x = self.act(x)
        x = self.dropout(x)
        return x


# GLU CNN,inherit from MASRModel,rewrite predict()
class GatedConv(MASRModel):
    """ This is a model between Wav2letter and Gated Convnets.
        The core block of this model is Gated Convolutional Network"""

    def __init__(self, vocabulary, blank=0, name="masr"):
        """ vocabulary : str : string of all labels such that vocaulary[0] == ctc_blank  """
        super().__init__(vocabulary=vocabulary, name=name, blank=blank)
        self.blank = blank
        self.vocabulary = vocabulary
        self.name = name
        output_units = len(vocabulary)
        modules = []
        modules.append(ConvBlock(nn.Conv1d(20, 500, 48, 2, 97), 0.2)) # input layer

        #  refers to image recogtion tasks, 3 × 3 is the smallest size that
        #  can capture pixels in its eight neighbor information.
        #     On the other hand, it has better nonlinearity here since more nonlinear activation functions are adopted,
        #     which makes the decision function more decisive. It can express more powerful features from the input data
        #     with less parameters.
        for i in range(7):
            modules.append(ConvBlock(nn.Conv1d(in_channels=250, out_channels=500, kernel_size=7, stride=1), p=0.3))

        modules.append(ConvBlock(nn.Conv1d(250, 2000, 32, 1), 0.5))

        modules.append(ConvBlock(nn.Conv1d(1000, 2000, 1, 1), 0.5))

        modules.append(weight_norm(nn.Conv1d(1000, output_units, 1, 1))) # output layer

        self.cnn = nn.Sequential(*modules)

    def forward(self, x, lens):  # -> B * V * T
        x = self.cnn(x)
        for module in self.modules():
            if type(module) == nn.modules.Conv1d:
                lens = (
                    lens - module.kernel_size[0] + 2 * module.padding[0]
                ) // module.stride[0] + 1
        return x, lens

    # prediction without language model
    def predict(self, path):
        self.eval()
        # wav = feature.load_audio(path)
        # spec = feature.spectrogram(wav)
        spec = speech2text.feature.spectrogram(path)
        spec.unsqueeze_(0) # dimension expansion
        x_lens = spec.size(-1)  # number of columns of MFCC
        out = self.cnn(spec) # out is the probabilities of each syllable
        out_len = torch.tensor([out.size(-1)])  # number of characters
        text = self.decode(out, out_len)
        self.train()
        return text[0]
