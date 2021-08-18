# coding: utf-8
import torch
import torch.nn as nn
import data
from speechmodels.conv import GatedConv
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
        tensorboard=True
):
    #  visualize log
    if tensorboard:
        writer = SummaryWriter()
    train_dataset = data.MASRDataset(train_index_path, labels_path)
    # batchs = (len(train_dataset) + batch_size - 1) // batch_size

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
        weight_decay=weight_decay,  # weight decay to avoid overfitting
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
        # update parameters by using backward propagation
        for step, (x, y, x_lens, y_lens) in enumerate(train_dataloader):
            x = x.cuda()
            out, out_lens = model(x, x_lens)
            out = out.transpose(0, 1).transpose(0, 2)
            # loss=ctcloss(input=out, target=y, input_lengths=out_lens, target_lengths=y_lens)
            loss = ctcloss(out, y, out_lens, y_lens)  # get the current loss

            #  backward propagation and optimizer
            # initialize the gradient as zero to avoid the gradient
            # it uses is related to the previous batch,
            optimizer.zero_grad()
            #  use backward to propagation update gradient
            loss.backward()
            #  clip fradient，The gradient is constrained in a certain interval to prevent the gradient explosion
            # Perform gradient truncation before optimizer update during training.
            nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()  # update parameters
            epoch_loss += loss.item()
            gstep += 1
            print(
                "[{}/{}][{}/{}]\tLoss = {}".format(
                    epoch + 1, epochs, step, int(train_steps), loss.item()
                )
            )
            if tensorboard:
                writer.add_scalar("loss/step", loss.item(), gstep)

        # epoch_loss = epoch_loss / batchs # get average ctcloss for the current epoch

        cer = eval(model, test_dataloader)  # get cer of current epoch
        epoch_loss /= train_steps
        print("Epoch {}: Loss= {}, CER = {}".format(epoch, epoch_loss, cer))
        # cer and loss visulization for current epoch
        if tensorboard:
            writer.add_scalar("cer/epoch", cer, epoch + 1)
            writer.add_scalar("loss/epoch", loss, epoch + 1)
        if (epoch + 1) % 5 == 0:
            torch.save(model, "pretrained/model_{}.pth".format(epoch))  # save a pretrained speechmodel every 5 epochs


def eval(model, dataloader):
    # eval() is used to testing and predicting, to avoid
    # the influence that batch normalization and dropout have on testing/predicting.
    # in evaluation speechmodel, BN is fixed, and the mean and std are those trained previously.
    model.eval()
    decoder = GreedyDecoder(dataloader.dataset.labels_str)
    cer = 0  # CER
    print("decoding")
    #  no_grad() stop auto_grad and save the GPU resource and speed up computing,
    #  therefore bigger batch is possible to use
    with torch.no_grad():
        for i, (x, y, x_lens, y_lens) in tqdm(enumerate(dataloader)):
            x = x.cuda()  # x is the result after conv
            outs, out_lens = model(x, x_lens)
            outs = F.softmax(outs, 1)  # conver outs to probability, dim=0, by column，dim=1 by rows
            outs = outs.transpose(1, 2)
            ys = []
            offset = 0
            for y_len in y_lens:
                ys.append(y[offset: offset + y_len])
                offset += y_len
            out_strings, out_offsets = decoder.decode(outs, out_lens)
            y_strings = decoder.convert_to_strings(ys)  # decoded text
            #  zip() is used to take the iteratable object as a parameter,
            #  package the corresponding elements in the object into tuples,
            #  and then return a list composed of these tuples.
            for pred, truth in zip(out_strings, y_strings):
                trans, ref = pred[0], truth[0]
                # get character error rate by calculating Levenshtein distance
                cer += decoder.cer(trans, ref) / float(len(ref))
        cer /= len(dataloader.dataset)
    model.train()
    return cer


if __name__ == "__main__":
    vocabulary = joblib.load(LABEL_PATH)  # vocabulary：all characters in corpus
    vocabulary = "".join(vocabulary)
    model = GatedConv(vocabulary)
    model.cuda()  # trasnfer speech model from CPU to GPU
    train(model)
    # speechmodel.to_train()
    # speechmodel.fit()
