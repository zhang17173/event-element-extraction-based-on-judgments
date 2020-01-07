import shutil
import os

# 将整个文本切割成单个的案件

source_file = "/home/zhang17173/event-element-extraction-based-on-judgments/data/crf_result/positive_by_crf.txt"
target_folder = "/home/zhang17173/event-element-extraction-based-on-judgments/data/crf_result/单个案件"

if os.path.exists(target_folder):
    shutil.rmtree(target_folder)
os.mkdir(target_folder)

with open(source_file, "r", encoding="utf-8") as f1:
    cases = f1.readlines()
    num = 1
    file_name = '/home/zhang17173/event-element-extraction-based-on-judgments/data/crf_result/单个案件/' + str(num) + '.txt'
    for i in range(len(cases)):
        f2 = open(file_name, "a", encoding='utf-8')
        if cases[i] == '\n':
            num += 1
            file_name = '/home/zhang17173/event-element-extraction-based-on-judgments/data/crf_result/单个案件/' + str(num) + '.txt'
        else:
            f2.writelines(cases[i])
        f2.close()
