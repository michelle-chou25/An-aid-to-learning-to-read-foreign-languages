from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import joblib
from feature import *

# dataset definition
class MASRDataset(Dataset):
    def __init__(self, index_path, labels_path):
        with open(index_path) as f:
            idx = f.readlines()
        idx = [x.strip().split(",", 1) for x in idx]
        self.idx = idx
        labels = joblib.load(labels_path)
        self.labels = dict([(labels[i], i) for i in range(len(labels))])
        self.labels_str = labels

    # get a row at an index
    def __getitem__(self, index):
        wav, transcript = self.idx[index]
        # wav = load_audio(wav)
        spect = spectrogram(wav)
        transcript = list(filter(None, [self.labels.get(x) for x in transcript]))

        return spect, transcript

    def __len__(self):
        return len(self.idx)


def _collate_fn(batch):
    def func(p):
        return p[0].size(1)

    batch = sorted(batch, key=lambda sample: sample[0].size(1), reverse=True)
    longest_sample = max(batch, key=func)[0]
    freq_size = longest_sample.size(0)
    minibatch_size = len(batch)
    max_seqlength = longest_sample.size(1)
    inputs = torch.zeros(minibatch_size, freq_size, max_seqlength)
    input_lens = torch.IntTensor(minibatch_size)  # 创建一个minibatchsize * 1大小的int张量
    target_lens = torch.IntTensor(minibatch_size)
    targets = []
    for x in range(minibatch_size):
        sample = batch[x]
        tensor = sample[0]  # 当前batch的行数
        target = sample[1]  # 当前batch的列数
        seq_length = tensor.size(1)  # tensor的列数
        inputs[x].narrow(1, 0, seq_length).copy_(tensor)
        input_lens[x] = seq_length
        target_lens[x] = len(target)
        targets.extend(target)
    targets = torch.IntTensor(targets)
    return inputs, targets, input_lens, target_lens


class MASRDataLoader(DataLoader):
    def __init__(self, *args, **kwargs):
        super(MASRDataLoader, self).__init__(*args, **kwargs)
        self.collate_fn = _collate_fn

