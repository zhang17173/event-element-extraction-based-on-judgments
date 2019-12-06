# 从excel中导出txt格式的案件信息

import xlrd
import re


excel_file = "data/案件.xlsx"  # excel文件路径
wb = xlrd.open_workbook(excel_file)
sheet0 = wb.sheets()[0]  # 获取第一个工作表

records = sheet0.col_values(21)[1:]  # 第21列代表庭审过程
court_opinion = sheet0.col_values(27)[1:]  # 第27列代表法院意见
sentence = sheet0.col_values(29)[1:]  # 第29列代表判决结果

# 写入文本文件
f1 = open("data/argument.txt", "w", encoding='utf-8')   # 辩护人意见
f2 = open("data/truth.txt", 'w', encoding='utf-8')  # 审理查明
f3 = open("data/court_opinion.txt", 'w', encoding='utf-8')  # 法院意见
f4 = open("data/sentence.txt", 'w', encoding='utf-8')  # 判决结果

re_argument = re.compile(r"辩护人.{0,5}辩护意见.*?。")
re_truth = re.compile(r"(公诉机关指控|检察院指控|审理查明).*?上述事实")

for elem1, elem2, elem3 in list(zip(records, court_opinion, sentence)):
    search_argument = re_argument.search(elem1)
    if search_argument:
        f1.write(search_argument.group() + '\n')
    else:
        f1.write("None\n")

    search_truth = re_truth.search(elem1)
    if search_truth:
        f2.write(search_truth.group() + '\n')
    else:
        f2.write("None\n")

    f3.write(elem2 + '\n')
    f4.write(elem3+'\n')


f1.close()
f2.close()
f3.close()
f4.close()
