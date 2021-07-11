#  * @Author: Ruochen Xue
#  * @Date:   2020-07-01 15:57:29
#  * @Last Modified by: Ruochen Xue
#  * @Last Modified time: 2020-07-01 20:57:29
import jieba

# Make Chinese word segmentation of sentences
def seg_depart(sentence):
    # Chinese word segmentation for each line in the document
    print("doing word segmentation")
    sentence_depart = jieba.cut(sentence.strip())
    outstr = ''
    for word in sentence_depart:
        if word != '\n':
            outstr += word
            outstr += " "
    return outstr

# Give the document path
filename = "Corpus/test_chinese.txt"
outfilename = "Corpus/test_chineseout.txt"
inputs = open(filename, 'r', encoding='UTF-8')
outputs = open(outfilename, 'w', encoding='UTF-8')

# Write the output to out.txt
for line in inputs:
    line_seg = seg_depart(line)
    outputs.write(line_seg + '\n')
outputs.close()
inputs.close()
print("word segmentation successfully！！！")