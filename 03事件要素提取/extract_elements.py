import sys
sys.path.append(
    "/home/zhang17173/event-element-extraction-based-on-judgments/04判决结果预测")
from rules import *
from utils import *

complete_data = "data/original_data/cases.txt"
court_opinion = "data/original_data/court_opinion.txt"
sentence = "data/original_data/sentence.txt"
crf_result = "data/crf_result/单个案件/"

f1 = open(court_opinion, "r", encoding="utf-8")
f2 = open(sentence, "r", encoding="utf-8")
lines1 = f1.readlines()
lines2 = f2.readlines()
for idx, (line1, line2) in enumerate(zip(lines1, lines2)):
    cn = crime_name(line2)
    cs = crime_stage(line1)
    lr = limited_responsibility(line1)
    pd = pedigree(line1)
    vf = victim_fault(line1)
    dm = damage(line1)
    sr = sentence_result(line2)
    positive = get_event_elements(crf_result+str(idx+1)+".txt")
    print(cn,cs,lr,pd,vf,dm,sr,positive, sep="\n")
