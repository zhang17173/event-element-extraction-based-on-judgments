import sys
import csv
import glob
sys.path.append("/home/yxr/event-element-extraction-based-on-judgments/04判决结果预测")
from utils import *
from rules import *

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


