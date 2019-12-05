import os
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

# ltp模型目录的路径，根据实际情况修改
LTP_DATA_DIR = '/home/zhangshiwei/ltp_data_v3.4.0/'
# 词性标注模型路径，模型名称为`pos.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
# 命名实体识别模型路径，模型名称为`ner.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')

# 这里是输入的文本
case_content = "被告人王呈心持刀故意非法剥夺他人生命行为构成故意杀人罪依法应予以处罚被告人王呈心系犯罪未遂依法可以比照既遂犯从轻或者减轻处罚到案后如实供述犯罪事实依法从轻处罚被告人患有精神活性物质所致精神障碍酌情从轻处罚对辩护人提出相关辩护意见予以采纳判决如下被告人王呈心犯故意杀人罪判处有期徒刑五年二被告人王呈心犯罪工具水果刀予以没收"

# 分词
model_path = "/home/zhangshiwei/下载/ltp-3.4.0/bin/examples"  # 填写ltp可执行文件路径
command1 = "cd " + model_path
command2 = "echo " + case_content
command3 = "./cws_cmdline --threads 24 --segmentor-lexicon dict"
command = command1 + "&&" + command2 + "|" + command3
f = os.popen(command)
words = f.read().strip().split("\t")

# 词性标注
postagger = Postagger()  # 初始化词性标注实例
postagger.load(pos_model_path)  # 加载模型
postags = postagger.postag(words)  # 词性标注

# 命名实体识别
recognizer = NamedEntityRecognizer()  # 初始化命名实体识别实例
recognizer.load(ner_model_path)  # 加载模型
netags = recognizer.recognize(words, postags)  # 命名实体识别

# 打印结果
for word, postag, netag in zip(words, postags, netags):
    print(word+"\t"+postag+"\t"+netag)

# 释放模型
postagger.release()
recognizer.release()
