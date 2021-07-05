# -*- coding: utf-8 -*-
#/usr/bin/python2

class Hyperparams:
    # data
    source_train = 'Corpus/chinese_out.txt'
    target_train = 'Corpus/english1w.txt'
    source_test = 'corpora/tst2013.vi'
    target_test = 'corpora/tst2013.en'
    source_test1 = 'corpora/tst1.vi'
    target_test1 = 'corpora/tst2.en'
    
    # training
    batch_size = 32 # alias = N
    lr = 0.0001 # learning rate.
    logdir = 'logdir' # log directory
    
    # model
    maxlen = 10 # 每句话长度
    min_cnt = 20 # 出现次数过少会显示 <UNK>.
    hidden_units = 512 # alias = C
    num_blocks = 6 # 层数
    num_epochs = 20 # 遍历次数
    num_heads = 8
    dropout_rate = 0.1
    sinusoid = False # 选择嵌入方式
    
    
    
    
 
