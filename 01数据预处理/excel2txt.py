# 从excel中导出txt格式的案件信息

import xlrd


excel_file = "data/案件.xls"  # excel文件路径
wb = xlrd.open_workbook(excel_file)
sheet0 = wb.sheets()[0]  # 获取第一个工作表

truth = sheet0.col_values(21)[1:]  # 第21列代表审理查明
court_opinion = sheet0.col_values(27)[1:]  # 第27列代表法院意见
sentence = sheet0.col_values(29)[1:]  # 第29列代表判决结果

# 写入文本文件
f1 = open("data/truth.txt", 'w', encoding='utf-8')
f2 = open("data/court_opinion.txt", 'w', encoding='utf-8')
f3 = open("data/sentence.txt", 'w', encoding='utf-8')

for elem1, elem2, elem3 in list(zip(truth, court_opinion, sentence)):
    f1.write(elem1 + '\n')
    f2.write(elem2 + '\n')
    f3.write(elem3 + '\n')

f1.close()
f2.close()
f3.close()
