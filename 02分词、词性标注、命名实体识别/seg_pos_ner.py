import os
import pkuseg
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

"""使用pkuseg对文本进行分词，使用LTP进行词性标注和命名实体识别"""

LTP_DATA_DIR = "../../ltp_data_v3.4.0"  # ltp模型目录的路径，根据实际情况修改
input_file = "../01数据预处理/txt_files/truth.txt"
output_file = "seg_pos_ner_result.txt"

# LTP词性标注模型
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径
postagger = Postagger()  # 初始化词性标注实例
postagger.load(pos_model_path)  # 加载模型

# LTP命名实体识别模型
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径
recognizer = NamedEntityRecognizer()  # 初始化命名实体识别实例
recognizer.load(ner_model_path)  # 加载模型


def spn(text):
    """对文本进行分词、词性标注、命名实体识别"""
    # 使用pkuseg工具分词
    text = text.replace("。", "")  # 去除句号
    seg = pkuseg.pkuseg(model_name='customized_model', user_dict='dict')
    words = seg.cut(text)
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    return zip(words, postags, netags)


# 对文本进行分词、词性标注、命名实体识别
f_input = open(input_file, "r", encoding="utf-8")
f_output = open(output_file, "w", encoding="utf-8")
lines = f_input.readlines()
idx = 1
for line in lines:
    zipped = spn(line)
    for word, postag, netag in zipped:
        f_output.write(word + "\t" + postag + "\t" + netag + "\n")
    f_output.write("\n")
    print(str(idx) + " lines finished.")
    idx += 1

f_input.close()
f_output.close()

# 释放LTP模型
postagger.release()
recognizer.release()
