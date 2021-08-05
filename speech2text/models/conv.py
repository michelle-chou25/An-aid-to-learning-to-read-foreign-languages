import torch
import torch.nn as nn
from torch.nn.utils import weight_norm
from .base import MASRModel
import feature

# 单个卷积层
class ConvBlock(nn.Module):
    def __init__(self, conv, p):
        super().__init__()
        self.conv = conv
        nn.init.kaiming_normal_(self.conv.weight)  # 用kaiming正态分布初始化卷积层参数
        self.conv = weight_norm(self.conv)  # a reparameterization method，加速网络收敛
        # 激活函数1维GLU  是Relu激活单元：(X * W + b)，加上一个Sigmoid激活单元：O(X * V + c)构成的gate unit
        # 详解见肖桐的书9.3.3
        self.act = nn.GLU(1)
        self.dropout = nn.Dropout(p, inplace=True)  # 每次都随机让一些神经元不参与运算，也就是达到局部连接的作用, dropout设为0.3到0.5

    def forward(self, x): # 传播
        x = self.conv(x)
        x = self.act(x)
        x = self.dropout(x)
        return x


# 门控卷积神经网络,inherit from MASRModel,rewrite predict()
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
        modules.append(ConvBlock(nn.Conv1d(20, 500, 48, 2, 97), 0.2)) # 输入层

        # 隐藏层，3×3，这是最小的能够捕获像素八邻域信息的尺寸。
        # 有更多的非线性（更多层的非线性函数，使用了3个非线性激活函数），使得判决函数更加具有判决性。
        # 可以表达出输入数据中更多个强力特征，使用的参数也更少。
        for i in range(7):
            modules.append(ConvBlock(nn.Conv1d(in_channels=250, out_channels=500, kernel_size=7, stride=1), p=0.3))

        modules.append(ConvBlock(nn.Conv1d(250, 2000, 32, 1), 0.5))

        modules.append(ConvBlock(nn.Conv1d(1000, 2000, 1, 1), 0.5))

        modules.append(weight_norm(nn.Conv1d(1000, output_units, 1, 1))) # 输出层

        self.cnn = nn.Sequential(*modules)

    def forward(self, x, lens):  # -> B * V * T
        x = self.cnn(x)
        for module in self.modules():
            if type(module) == nn.modules.Conv1d:
                lens = (
                    lens - module.kernel_size[0] + 2 * module.padding[0]
                ) // module.stride[0] + 1
        return x, lens

    def predict(self, path):
        self.eval()
        # wav = feature.load_audio(path)
        # spec = feature.spectrogram(wav)
        spec = feature.spectrogram(path)
        spec.unsqueeze_(0) # 维数扩张
        x_lens = spec.size(-1)  # MFCC特征的列数
        out = self.cnn(spec) # 声学模型的结果:音素
        out_len = torch.tensor([out.size(-1)])  # 音素的列数
        text = self.decode(out, out_len)
        self.train()
        return text[0]
