import sys
import csv
import numpy as np
import glob
sys.path.append("/home/yxr/event-element-extraction-based-on-judgments/04判决结果预测")
from utils import *
from rules import *

def patterns_weight(csv_file, new_csv_file):

    """
    给特征加权，然后将16个特征变为6个特征，以缓解数据的稀疏性
    :param csv_file: 源文件，16个特征
    :param new_csv_file:加权合并之后的文件，6个特征
    :return:
    """
    f1 = np.loadtxt(csv_file, delimiter=',', dtype=np.int)
    new_csv_list = []
    for i in range(len(f1)):
        origin_patterns = f1[i]
        temp_dict = dict()

        # 伤亡=死亡*100+伤情*75
        temp_dict["01伤亡情况"] = origin_patterns[0] * 100 + (
                    origin_patterns[1] * 0.2 + origin_patterns[2] * 0.3 + origin_patterns[3] * 0.8) * 75

        # 罪名=(故意伤害:1)+ (故意杀人:2)
        temp_dict["02罪名"] = 2 if origin_patterns[4] == "2" else 1

        # 犯罪阶段=(故意伤害罪：0)+（预备：1）+（未遂：2）+（中止：2）+（既遂：3）
        temp_dict["03犯罪阶段"] = int(origin_patterns[5])

        # 积极因素=（投案：-10）+（如实供述：-10）+（自首：-20）+（认罪：-10)+（赔偿：-20）+（谅解：-20）+（立功：-30）+（被害人过错：-20）
        temp_dict["04积极因素"] = int(origin_patterns[6]) * (-10) + int(origin_patterns[7]) * (-10) + int(
            origin_patterns[8]) * (-20) + int(origin_patterns[9]) * (-10)
        + int(origin_patterns[10]) * (-20) + int(origin_patterns[11]) * (-20) + int(origin_patterns[12]) * (-30) + int(
            origin_patterns[15]) * (-20)

        # 限定刑事责任=（限定刑事责任：-1）
        temp_dict["05限定刑事责任"] = int(origin_patterns[13]) * (-1)

        # 前科=（前科：50）+（无：-10）+（默认：0）
        if origin_patterns[14] == "1":
            temp_dict["06前科"] = 50
        elif origin_patterns[14] == "0":
            temp_dict["06前科"] = -10
        else:
            temp_dict["06前科"] = 0

        temp_dict["判决结果"] = origin_patterns[-1]
        new_csv_list.append(temp_dict)

    # 将新特征写回文件
    headers = ["01伤亡情况", "02罪名", "03犯罪阶段", "04积极因素", "05限定刑事责任", "06前科", "判决结果"]
    with open(new_csv_file, "w", newline="")as f2:
        f_csv = csv.DictWriter(f2, headers)
        # f_csv.writeheader()
        f_csv.writerows(new_csv_list)


complete_data = "/home/yxr/event-element-extraction-based-on-judgments/data/original_data/cases.txt"
court_opinion = "/home/yxr/event-element-extraction-based-on-judgments/data/original_data/court_opinion.txt"
sentence = "/home/yxr/event-element-extraction-based-on-judgments/data/original_data/sentence.txt"
truth = "/home/yxr/event-element-extraction-based-on-judgments/data/original_data/truth.txt"
crf_result = "/home/yxr/event-element-extraction-based-on-judgments/data/crf_result/单个案件/"

f1 = open(court_opinion, "r", encoding="utf-8")
f2 = open(sentence, "r", encoding="utf-8")
f3 = open(truth, "r", encoding="utf-8")
lines1 = f1.readlines()
lines2 = f2.readlines()
lines3 = f3.readlines()
elements = dict() #用来存储所有要素
patterns = dict() #用来存储所有特征
headers = [
    '01死亡人数',
    "02轻微伤人数",
    "03轻伤人数",
    "04重伤人数",
    "05罪名",
    "06犯罪阶段",
    "07是否投案",
    "08是否如实供述",
    "09是否自首",
    "10是否认罪",
    "11是否赔偿",
    "12是否取得谅解",
    "13是否立功",
    "14是否限制刑事责任能力",
    "15是否有前科",
    "16被害人是否有过错",
    "判决结果"
]
rows = []
for idx, (line1, line2, line3) in enumerate(zip(lines1, lines2, lines3)):
    elements["罪名"] = crime_name(line2)
    elements["犯罪阶段"] = crime_stage(line1)
    elements["是否限制刑事责任能力"] = limited_responsibility(line1)
    elements["是否有前科"] = pedigree(line1)
    elements["是否立功"] = contribute(line1)
    elements["被害人是否有过错"] = victim_fault(line1)
    elements["受伤情况"] = damage(line1)
    elements["死亡情况"] = death(line1)
    elements["判决结果"] = sentence_result(line2)

    """
    cn = crime_name(line2)
    cs = crime_stage(line1)
    lr = limited_responsibility(line1)
    pd = pedigree(line1)
    vf = victim_fault(line1)
    dm = damage(line1)
    sr = sentence_result(line2)
    """
    positives = get_event_elements(crf_result+str(idx+1)+".txt")
    elements.update(positives)
    patterns = get_patterns(elements)
    print(patterns)
    rows.append(patterns)

# 写回数据
with open("/home/yxr/event-element-extraction-based-on-judgments/data/data_16.csv", "w", newline='') as f:
    f_csv = csv.DictWriter(f, headers)
    # f_csv.writeheader()
    f_csv.writerows(rows)

patterns_weight("/home/yxr/event-element-extraction-based-on-judgments/data/data_16.csv","/home/yxr/event-element-extraction-based-on-judgments/data/data_6.csv")



