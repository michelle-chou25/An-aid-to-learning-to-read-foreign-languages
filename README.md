# Project Title
An aid to learning to read foreign languages

# Project Description
The main content of this project is to build a simple Chinese-English translation web tool, which supports users to paste URL, extract paragraph text from it and translate automatically, users can also choose to paste the paragraph or word they want to translate manually. 

# Table of contents
Algorithm folder is to store different finished machine translation algoirthms.
Corpus folder is to store different corpura used in machine translation.
Demo_FrontEnd folder is used to make representation for demo.
bysms folder is to store the whole system embedded into Django framework.
database folder is to store the files related to databese format converting.
results folder is to store the evalution files for machine tranlation algoirthms.
speech2text folder is to store files related to speech recognition.
requirements file is to store all the packages and testing softwares needed to installed in the local computer.

# Installation
To use this project, first clone the repo on your device using the command below:

```git clone https://github.com/michelle-chou25/An-aid-to-learning-to-read-foreign-languages.git```

Then according to the requirements file to install packages and testing softwares.

Then using the command below (enter into bysms folder):

```cd /Users/username/VScodeProjects/ProjectName/bysms```

After the Django server part and MongoDB part start, input the URL http://127.0.0.1:8000/view/ in the browser

(the port number 8000 needs to be change into the default port number of the used computer).

Then the word query and sentence translation can be done in the FrontEnd part.

## Corpura
The Google Drive link for trained Machine Translation models are as follows: 
(Format: Corpus name_Algorithm name_Translation direction)
1.	Corpus1w_Transformer_Chinese-English:
https://drive.google.com/file/d/1-q6RZcZyxEBfXzOFnJkLRNIa9ctQLWMD/view?usp=sharing
2.	Corpus1w_Transformer_English-Chinese:
https://drive.google.com/drive/folders/13y7P1uFnKijU8BS1J2YOVH_QyaHD114o?usp=sharing
3.	Corpus1w_seq2seq+attention_Chinese-English:
https://drive.google.com/drive/folders/1-P3U4B7RNtwdeeM0KjpyfHB7Aji4s8nq?usp=sharing
4.	Corpus_education_Transformer_Chinese-English:
https://drive.google.com/drive/folders/1-R4lTnch3UEF_BQTAeUS74Yk9lSH5jIj?usp=sharing
5.	Seq2seq_testcorpus_ seq2seq+attention_Chinese-English:
https://drive.google.com/drive/folders/1UXjT5NN3JdNIImfNdWg3bHCXCNIPi9Ne?usp=sharing

## Requirement package
python 3.7.0

python packages:
pymongo 3.11.4
Django   3.2.5
django-cors-headers   3.7.0
mongoengine   0.23.1
fake-useragent 0.1.11
torch==1.8.1
Levenshtein==0.12.0
librosa==0.8.0
tensorboardX==2.1
ctcdecode==1.0.2
sounddevice==0.4.1
pyaudio==0.2.11
joblib==1.0.0
scipy          1.7.0

database:
mongodb    4.4.6

develop tools:
postman 8.7.0
HbuilderX 3.1.18
node.js v14.17.2
robot 3t 09

algorithm packages:
tensorflow 2.5.0
jieba 0.42.1
numpy 1.19.5
zhconv 1.4.1
tqdm 4.56.0
<<<<<<< Updated upstream
jieba 0.42.1
<<<<<<< HEAD



=======
>>>>>>> Stashed changes
=======
fake-useragent 0.1.11
torch==1.8.1
Levenshtein==0.12.0
librosa==0.8.0
tensorboardX==2.1
ctcdecode==1.0.2
sounddevice==0.4.1
pyaudio==0.2.11
joblib==1.0.0
<<<<<<< HEAD
scipy          1.7.0
=======
scipy                             1.7.0
>>>>>>> 11b5daca26962b7ec751b1586cecdcd7bdaf4b80
>>>>>>> main

# Contributors
Ruochen Xue 
Nanjun Zhou







