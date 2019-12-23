import os
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

# ltp模型目录的路径，根据实际情况修改
LTP_DATA_DIR = "/home/zhang17173/ltp_data_v3.4.0"

# 使用编译好的LTP可执行程序进行分词，而不是直接调用pyltp的接口
cws_path = "/home/zhang17173/ltp-3.4.0/bin/examples"  # 填写ltp可执行文件目录路径
input_path = "data/original_data/court_opinion.txt"  # 输入文件路径
output_path = "02分词、词性标注、命名实体识别/seg_pos_ner_result.txt"   # 输出文件路径
temp_path = "/home/zhang17173/event-element-extraction-based-on-judgments/02分词、词性标注、命名实体识别/temp.txt"  # 临时文件路径

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径
postagger = Postagger()  # 初始化词性标注实例
postagger.load(pos_model_path)  # 加载模型

# 命名实体识别
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径
recognizer = NamedEntityRecognizer()  # 初始化命名实体识别实例
recognizer.load(ner_model_path)  # 加载模型

# 按行读取案件，进行分词、词性标注、命名实体识别处理
f1 = open(input_path, "r", encoding="utf-8")
f2 = open(output_path, "w", encoding="utf-8")

lines = f1.readlines()
for idx, line in enumerate(lines):
    # 创建临时文件用以分词
    f3 = open(temp_path, "w", encoding="utf-8")
    f3.write(line)
    f3.close()
    # 执行分词
    print("正在为第%d句话分词..." % (idx+1))
    command1 = "cd " + cws_path
    command2 = "./cws_cmdline --threads 24 --input " + \
        temp_path + " --segmentor-lexicon dict"
    f = os.popen(command1 + "&&" + command2)
    # 分词、词性标注、命名实体识别
    words = f.read().strip("\n").split("\t")
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    # 写入结果
    for word, postag, netag in zip(words, postags, netags):
        f2.write(word + "\t" + postag + "\t" + netag + "\t" + "O" + "\n")
    f2.write("\n")

# 释放模型
postagger.release()
recognizer.release()

f1.close()
f2.close()
os.remove(temp_path)
