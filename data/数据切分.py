with open("02分词、词性标注、命名实体识别/seg_pos_ner_result.txt", "r", encoding="utf-8") as f1:
    lines = f1.readlines()
    f2 = open("data/part3.txt", "w", encoding="utf-8")
    f2.writelines(lines[-20000:])
    f2.close()
