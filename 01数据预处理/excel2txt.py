# -*- coding: utf-8 -*-

# 从excel中导出txt格式的案件信息
# 分别为辩护人意见、审理查明、法院意见和判决结果

import xlrd
import re
from data_preprocess import preprocess


excel_file = "../data/案件.xlsx"  # excel文件路径
wb = xlrd.open_workbook(excel_file)
sheet0 = wb.sheets()[0]  # 获取第一个工作表

records = sheet0.col_values(21)[1:]  # 第21列代表庭审过程
court_opinion = sheet0.col_values(27)[1:]  # 第27列代表法院意见
sentence = sheet0.col_values(29)[1:]  # 第29列代表判决结果


re_argument = re.compile(r"辩护人.*?(提出|认为|所提|辩解|要求|建议|辩护|辩称).*?。")
re_truth = re.compile(r"(公诉机关指控|检察院.{0,5}指控|经.*?查明).*?(上述事实|以上事实|上述案件事实|公诉机关认为|公诉机关认定|为证实|该院认为|检察院认为|被告人.*?异议)")
re_truth_1 = re.compile(r"(公诉机关指控|检察院.{0,5}指控|经.*?查明).*")
re_sentence = re.compile(r"判决如下.*?(被告人.*(年|月|处罚))")

# 写入文本文件
f1 = open("../data/argument.txt", "w", encoding='utf-8')   # 辩护人意见
f2 = open("../data/truth.txt", 'w', encoding='utf-8')  # 审理查明
f3 = open("../data/court_opinion.txt", 'w', encoding='utf-8')  # 法院意见
f4 = open("../data/sentence.txt", 'w', encoding='utf-8')  # 判决结果

for elem1, elem2, elem3 in list(zip(records, court_opinion, sentence)):
    # 预处理
    elem1 = preprocess(elem1)
    elem2 = preprocess(elem2)
    elem3 = preprocess(elem3)
    # 写入辩护人意见
    search_argument = re_argument.search(elem1)
    if search_argument:
        f1.write(search_argument.group() + '\n')
    else:
        f1.write("None\n")
    # 写入审理查明
    search_truth = re_truth.search(elem1)
    if search_truth:
        f2.write(search_truth.group() + '\r')
    else:
        search_truth_1 = re_truth_1.search(elem1)
        if search_truth_1:
            f2.write(search_truth_1.group() + '\r')
        else:
            f2.write("\r")
    # 写入法院意见
    f3.write(elem2 + '\n')
    # 写入判决结果
    search_sentence = re_sentence.search(elem3)
    if search_sentence:
        f4.write(search_sentence.group(1) + '\n')
    else:
        f4.write("None\n")


f1.close()
f2.close()
f3.close()
f4.close()
