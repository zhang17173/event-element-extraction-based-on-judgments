import os
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

# ltp模型目录的路径，根据实际情况修改
LTP_DATA_DIR = '/home/zhangshiwei/ltp_data_v3.4.0/'
# 词性标注模型路径，模型名称为`pos.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
# 命名实体识别模型路径，模型名称为`ner.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')


# 分词
cws_path = "/home/zhangshiwei/下载/ltp-3.4.0/bin/examples"  # 填写ltp可执行文件路径
input_path = "/home/zhangshiwei/event-element-extraction-based-on-judgments/data/truth.txt"  # 输入文件路径
temp_path = "/home/zhangshiwei/event-element-extraction-based-on-judgments/data/temp.txt"  # 临时文件路径
# 词性标注
postagger = Postagger()  # 初始化词性标注实例
postagger.load(pos_model_path)  # 加载模型
# 命名实体识别
recognizer = NamedEntityRecognizer()  # 初始化命名实体识别实例
recognizer.load(ner_model_path)  # 加载模型

# 按行读取案件
f1 = open(input_path, "r", encoding="utf-8")
f2 = open("data/seg_pos_ner_result.txt", "w", encoding="utf-8")
lines = f1.readlines()
for line in lines:
    f3 = open("data/temp.txt", "w", encoding="utf-8")
    f3.write(line)
    f3.close()
    command1 = "cd " + cws_path
    command2 = "./cws_cmdline --threads 24 --input " + \
        temp_path + " --segmentor-lexicon dict"
    command = command1 + "&&" + command2
    f = os.popen(command)
    words = f.read().strip("\n").split("\t")
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别

    for word, postag, netag in zip(words, postags, netags):
        f2.write(word + "\t" + postag + "\t" + netag + "\n")

    f2.write("\n")


# 释放模型
postagger.release()
recognizer.release()

f1.close()
f2.close()
