import xlrd
import os

f = open("data/train.txt", "a",encoding="utf-8")
excel = xlrd.open_workbook("data/part3.xlsx")
table = excel.sheets()[0]
for i in range(40000):
    if table.cell_value(i,0) != '':
        if table.cell_value(i,3) =='':
            new_list = table.row_values(i).append("O")
            print(type(new_list))
            f.writelines('\t'.join(new_list))
            f.write("\n")
        else:
            f.writelines('\t'.join(table.row_values(i)))
            f.write("\n")
    else:
        f.write("\n")
f.close()