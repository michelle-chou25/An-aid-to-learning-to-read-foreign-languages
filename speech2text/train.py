import torch
import torch.nn as nn
import data
from models.conv import GatedConv
from tqdm import tqdm
from decoder import GreedyDecoder
from torch.nn import CTCLoss
import torch.nn.functional as F
import joblib
from tensorboardX import SummaryWriter
from config import TRAIN_PATH, DEV_PATH, LABEL_PATH


import os
# gpu_list = '2,3'
# os.environ["CUDA_VISIBLE_DEVICES"] = gpu_list
torch.cuda.empty_cache()
torch.cuda.memory_summary(device=None, abbreviated=False)
def train(
    model,
    epochs=100,
    batch_size=64,
    train_index_path=TRAIN_PATH,
    dev_index_path=DEV_PATH,
    labels_path=LABEL_PATH,
    learning_rate=0.6,
    momentum=0.8,
    max_grad_norm=0.2,
    weight_decay=0,
    tensorboard = True
):
    #  visualize log
    if tensorboard:
        writer = SummaryWriter()
    train_dataset = data.MASRDataset(train_index_path, labels_path)
    # batchs = (len(train_dataset) + batch_size - 1) // batch_size #计算有多少个batch需要训练
    
    dev_dataset = data.MASRDataset(dev_index_path, labels_path)
    # train_dataloader = data.MASRDataLoader(
    #     train_dataset, batch_size=batch_size, num_workers=0
    # )
    train_dataloader_shuffle = data.MASRDataLoader(
        train_dataset, batch_size=batch_size, num_workers=0, shuffle=True
    )
    test_dataloader = data.MASRDataLoader(
        dev_dataset, batch_size=batch_size, num_workers=0
    )
    parameters = model.parameters()
    # define the optimization。SGD
    optimizer = torch.optim.SGD(
        parameters,
        lr=learning_rate,
        momentum=momentum,
        nesterov=True,
        weight_decay=weight_decay, #权重衰减
    )
    ctcloss = CTCLoss()
    # lr_sched = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.985)

    gstep = 0
    # enumerate epochs
    for epoch in range(epochs):
        epoch_loss = 0
        train_dataloader = train_dataloader_shuffle
        train_steps = len(train_dataloader)
        # lr_sched.step()
        # 每个epoch需要一个内部回路来反向传播求梯度，更新参数
        for step, (x, y, x_lens, y_lens) in enumerate(train_dataloader):
            x = x.cuda()
            out, out_lens = model(x, x_lens)
            out = out.transpose(0, 1).transpose(0, 2)
            # loss=ctcloss(input=out, target=y, input_lengths=out_lens, target_lengths=y_lens)
            loss = ctcloss(out, y, out_lens, y_lens) #知道当前loss是多少
            
            #  backward propagation and optimizer
            optimizer.zero_grad() #将梯度清0，避免使用的grad和上一个mini batch有关
            #  反向传播更新梯度
            loss.backward() 
            #  梯度截断，将梯度约束在某一个区间之内，防止梯度爆炸
            #  在训练的过程中，在优化器更新之前进行梯度截断操作。
            nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm) 
            optimizer.step() #更新参数
            epoch_loss += loss.item()
            gstep += 1
            print(
                "[{}/{}][{}/{}]\tLoss = {}".format(
                    epoch + 1, epochs, step+1, int(train_steps), loss.item()
                )
            )
            if tensorboard:
                writer.add_scalar("loss/step", loss.item(), gstep)

        # epoch_loss = epoch_loss / batchs # get average ctcloss for the current epoch
        
        cer = eval(model, test_dataloader) # get cer of current epoch
        epoch_loss/=train_steps
        print("Epoch {}: Loss= {}, CER = {}".format(epoch, epoch_loss, cer))
        # cer and loss visulization
        if tensorboard:
            writer.add_scalar("cer/epoch", cer, epoch+1)
            writer.add_scalar("loss/epoch", loss, epoch+1)
        if (epoch+1) % 5 == 0:
            torch.save(model, "pretrained/model_{}.pth".format(epoch)) # 每隔5个epoch保存一个预训练模型

def eval(model, dataloader): # model: GLU CNN
    model.eval() #用于测试合和预测， 为了排除BN和Dropout对测试影响
                # 将model改为eval模式后，BN的参数固定，并采用之前训练好的全局的mean和std
    decoder = GreedyDecoder(dataloader.dataset.labels_str) # 贪婪搜索解码，只匹配最大概率
    cer = 0  # 字符错误率
    print("decoding")
    with torch.no_grad(): # 用于停止autograd的工作， 
                        #更进一步加速和节省gpu空间（因为不用计算和存储梯度），
                        # # 从而可以更快计算，也可以跑更大的batch来测试
        for i, (x, y, x_lens, y_lens) in tqdm(enumerate(dataloader)):
            x = x.cuda()
            outs, out_lens = model(x, x_lens) # x卷积后的结果
            outs = F.softmax(outs, 1)
            outs = outs.transpose(1, 2) # transpose dim1 and dim 2
            ys = []
            offset = 0
            for y_len in y_lens:
                ys.append(y[offset : offset + y_len])
                offset += y_len
            out_strings, out_offsets = decoder.decode(outs, out_lens)
            y_strings = decoder.convert_to_strings(ys) #解码后的text
            #zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
            for pred, truth in zip(out_strings, y_strings): 
                trans, ref = pred[0], truth[0]
                cer += decoder.cer(trans, ref) / float(len(ref)) # get character error rate by calculating Levenshtein distance
        cer /= len(dataloader.dataset)
    model.train()
    return cer


if __name__ == "__main__":
    vocabulary = joblib.load(LABEL_PATH) # vocabulary：训练集中的全部汉字
    vocabulary = "".join(vocabulary)
    model = GatedConv(vocabulary)
    model.cuda() # 把模型从CPU迁移到GPU上
    train(model)
    # model.to_train()
    # model.fit()
