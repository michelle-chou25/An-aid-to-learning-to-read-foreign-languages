# coding: utf-8
import Levenshtein
import torch
from torch.functional import Tensor
import torch.nn as nn
import data
from .speechmodels.conv import GatedConv
from tqdm import tqdm
from .decoder import GreedyDecoder
from torch.nn import CTCLoss
import torch.nn.functional as F
import joblib
from tensorboardX import SummaryWriter
from .config import TRAIN_PATH, DEV_PATH, LABEL_PATH
import os
import sys
from torch._C import import_ir_module
# from speechmodels.conv import GatedConv
# from config import pretrained_model_path
sys.path.append(os.getcwd())
# from ..speechmodels.conv import GatedConv
# from ..config import pretrained_model_path
# from speech2text.speechmodels.conv import GatedConv
# from speech2text.config import pretrained_model_path
from speechmodels.conv import GatedConv
from config import pretrained_model_path
import random
import time



def validate(model,
    epochs=100,
    batch_size=128,
    valid_index_path=DEV_PATH,
    labels_path=LABEL_PATH,
    shuffle=True,
    num_workers=0,
    tensorboard=True
):
    
    if tensorboard:
        writer = SummaryWriter()
    # speechmodel = GatedConv.load(os.path.join('..', pretrained_model_path))
    valid_dataset=data.MASRDataset(valid_index_path, labels_path)
    valid_dataloader = data.MASRDataLoader(
        valid_dataset, batch_size, num_workers
    )
    decoder = GreedyDecoder(valid_dataloader.dataset.labels_str)
    

    with open('/home/nz32/git/An-aid-to-learning-to-read-foreign-languages/speech2text/data_aishell/dev.index', encoding="utf-8") as f:
        idx = f.readlines()
    idx = [x.strip().split(",", 1) for x in idx] 

    for epoch in range(epochs):
        print("validating......")
        random.shuffle(idx)
        cer=0
        for item in idx:
            file=item[0]
            true_text=item[1]
            preditct_text=model.predict(file)
            # get CER by calculating Levenshtein distance
            cer += decoder.cer(preditct_text, true_text) / float(len(true_text))
        cer/=len(valid_dataloader.dataset) 
        print("Epoch {}: , CER = {}".format(epoch, cer))
        if tensorboard:
            writer.add_scalar("cer/epoch", cer, epoch+1)
    print("Finished.")
        



if __name__ == "__main__":
    cuda_gpu = torch.cuda.is_available()
    torch.cuda.empty_cache()
    torch.cuda.memory_summary(device=None, abbreviated=False)
    vocabulary = joblib.load(LABEL_PATH) # vocabulary：训练集中的全部汉字
    vocabulary = "".join(vocabulary)
    model = GatedConv.load(os.path.join('..', pretrained_model_path))
    if cuda_gpu:
        model.cuda() # transfer speechmodel to GPU
    time1=time.time()
    validate(model)
    time2=time.time()
    t = time2-time1
    print('Validate dataset running time:  {:.0f}minutes {:.0f}seconds'.format( t // 60, t % 60))
        
