import sys
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
for idx, (line1, line2, line3) in enumerate(zip(lines1, lines2, lines3)):
    elements["罪名"] = crime_name(line2)
    elements["犯罪阶段"] = crime_stage(line1)
    elements["是否限制刑事责任能力"] = limited_responsibility(line1)
    elements["是否有前科"] = pedigree(line1)
    elements["被害人是否有过错"] = victim_fault(line1)
    elements["受伤情况"] = damage(line3)
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
    #print(cn, cs, lr, pd, vf, dm, sr, positives, sep="\n")
    print(elements)
