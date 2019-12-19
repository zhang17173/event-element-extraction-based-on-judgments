import xlrd


f = open("data/test.txt", "w", encoding="utf-8")
excel = xlrd.open_workbook("data/part3.xlsx")
table = excel.sheets()[0]
for i in range(40000):
    if table.cell_value(i, 0) != '':
        if table.cell_value(i, 3) == '':
            new_list = table.row_values(i)[:3]
            new_list.append("O")
            f.writelines('\t'.join(new_list))
            f.write("\n")
        else:
            f.writelines('\t'.join(table.row_values(i)))
            f.write("\n")
    else:
        f.write("\n")
f.close()
