__mtime__= '20210318'
import torch
import feature
from models.conv import GatedConv
import torch.nn.functional as F
from ctcdecode import CTCBeamDecoder
from config import lm_path, pretrained_model_path

alpha = 0.8
beta = 0.3
cutoff_top_n = 40
cutoff_prob = 1.0
beam_width = 32
num_processes = 4
blank_index = 0

model = GatedConv.load(pretrained_model_path)
model.eval()

# 束搜索解码
decoder = CTCBeamDecoder(
    model.vocabulary,
    lm_path, #语言模型
    alpha,
    beta,
    cutoff_top_n,
    cutoff_prob,
    beam_width,
    num_processes,
    blank_index,
)


def translate(vocab, out, out_len):
    return "".join([vocab[x] for x in out[0:out_len]])


def predict(f):
    # wav = feature.load_audio(f)
    # spec = feature.spectrogram(wav)
    spec = feature.spectrogram(f)
    spec.unsqueeze_(0) #维数加1
    with torch.no_grad(): # 不求导， 暂时不追踪网络参数中的导数的目的，达到冻解网络的目的
        y = model.cnn(spec) # 得到声学模型识别后的音素的张量
        y = F.softmax(y, 1) #转为概率
    y_len = torch.tensor([y.size(-1)]) # tensor张量的列数
    y = y.permute(0, 2, 1)  # B * T * V
    print("decoding")
    out, score, offset, out_len = decoder.decode(y, y_len)
    return translate(model.vocabulary, out[0][0], out_len[0][0])

if __name__ == '__main__':
    #传入wav录音文件识别文本
    text = predict("data_aishell/BAC009S0765W0130.wav")
    print(text)