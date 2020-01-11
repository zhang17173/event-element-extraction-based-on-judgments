import os
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

LTP_DATA_DIR = "~/ltp_data_v3.4.0"  # ltp模型目录的路径，根据实际情况修改
cws_path = "~/ltp-3.4.0/bin/examples"  # ltp二进制可执行文件目录路径
temp_path = "./temp.txt"  # 临时文件路径

# 词性标注模型
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径
postagger = Postagger()  # 初始化词性标注实例
postagger.load(pos_model_path)  # 加载模型

# 命名实体识别模型
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径
recognizer = NamedEntityRecognizer()  # 初始化命名实体识别实例
recognizer.load(ner_model_path)  # 加载模型


def spn(input):
    '''对文本进行分词、词性标注、命名实体识别'''
    # 写入临时文件用以分词
    f = open(temp_path, "w", encoding="utf-8")
    f.write(input)
    f.close()
    # 使用编译好的LTP可执行程序进行分词，而不是直接调用pyltp的接口
    command1 = "cd " + cws_path
    command2 = "./cws_cmdline --threads 24 --input " + \
        temp_path + " --segmentor-lexicon dict"
    f_words = os.popen(command1 + "&&" + command2)
    words = f_words.read().strip("\n").split("\t")
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    return zip(words, postags, netags)


f_output = open("02分词、词性标注、命名实体识别/seg_pos_ner_result.txt",
                "w", encoding="utf-8")
f = open("data/original_data/court_opinion.txt", "r", encoding="utf-8")
lines = f.readlines()
for line in lines:
    zipped = spn(line)
    for word, postag, netag in zipped:
        f_output.write(word+"\t"+postag+"\t"+netag+"\n")
    f_output.write("\n")
f_output.close()
f.close()

# 释放模型
postagger.release()
recognizer.release()
os.remove(temp_path)
