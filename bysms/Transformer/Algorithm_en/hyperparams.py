class Hyperparams:
    # data
    source_train = 'Corpus/english1w.txt'
    target_train = 'Corpus/chinese_out.txt'
    source_test = 'Corpus/test_english.txt'
    target_test = 'Corpus/test_chineseout.txt'
    
    # training
    batch_size = 32 # alias = N
    lr = 0.0001 # learning rate.
    logdir = 'logdir' # log directory
    
    # model
    maxlen = 30 # Maximum number of words in a sentence. alias = T.
    min_cnt = 20 # words whose occurred less than min_cnt are encoded as <UNK>.
    hidden_units = 512 # alias = C
    num_blocks = 6 # number of encoder/decoder blocks
    num_epochs = 20 # traversal time
    num_heads = 8
    dropout_rate = 0.1
    sinusoid = False # select embedding method
    
    
    
    
 
