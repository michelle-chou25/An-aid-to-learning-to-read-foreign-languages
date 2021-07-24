import codecs
import os
import jieba
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import zhconv

from .Algorithm.hyperparams import Hyperparams as hp
from .Algorithm.data_load import load_cn_vocab, load_en_vocab
from .Algorithm.train import Graph

model_dir = 'Transformer/model/'


def eval(Source): 
    # load graph
    g = Graph(is_training=False)
    print("Graph loaded")
    
    # acquire the terminal input
    # Source = input("please input a sentence:")
    Fan = zhconv.convert(Source, 'zh-hans')

    sentence_depart = jieba.cut(Fan)
    outstr = ''
    for word in sentence_depart:
        if word != '\n':
            outstr += word
            outstr += " "
    
    # add index
    cn2idx, idx2cn = load_cn_vocab()
    en2idx, idx2en = load_en_vocab()
    outstr = [cn2idx.get(word, 1) for word in (outstr + u" </S>").split()]
    # print(len(outstr))

    # Pad
    if hp.maxlen-len(outstr) >= 0:      
        X = np.lib.pad(outstr, [0, hp.maxlen-len(outstr)], 'constant', constant_values=(0, 0)).reshape(1,30)
        # print(X)
    else:
        print("translation fail")
    
    # Start session 
    with g.graph.as_default():    
        sv = tf.train.Supervisor()
        with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            ## restore parameters
            sv.saver.restore(sess, tf.train.latest_checkpoint(model_dir))
            print("Restored!")
              
            ## Get model name
            mname = open(model_dir + '/checkpoint', 'r').read().split('"')[1] # model name
             
            ## Inference                  
            preds = np.zeros((1, hp.maxlen), np.int32)
            for j in range(hp.maxlen):
                _preds = sess.run(g.preds, {g.x: X, g.y: preds})
                preds[:, j] = _preds[:, j]
            # print(preds)
            # print(type(preds))
            for pred in preds:
                got = " ".join(idx2en[idx] for idx in pred).split("</S>")[0].strip()
                return got
                # print("- source: " + Source +"\n")
                # print("- got: " + got + "\n")

def get(input_sentence):
    tf.reset_default_graph()
    output_sentence = eval(input_sentence)
    return output_sentence
# if __name__ == '__main__':
#     eval()
#     print("Done")
    
    