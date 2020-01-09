import re


def remove_duplicate_elements(l):
    """
    去除列表中重复元素，同时保持相对顺序不变
    :param l: 可能包含重复元素的列表
    :return: 去除重复元素的新列表
    """
    new_list = []
    for elem in l:
        if elem not in new_list:
            new_list.append(elem)
    return new_list


def find_element(l, *ss):
    """
    查找列表l的元素中是否包含s
    :param l:列表
    :param ss:一个或多个字符串
    """

    for s in ss:
        for element in l:
            if ("否" in element) or ("不" in element) or ("没有" in element):
                return "0"
            elif s in element:
                return "1"
    return "0"


def text2num(text):
    num = 0
    # 将text序列连接成字符串
    text = "".join(text)
    digit = {
        '一': 1,
        '二': 2,
        '两': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9}
    if text:
        idx_q, idx_b, idx_s = text.find('千'), text.find('百'), text.find('十')
        if idx_q != -1:
            num += digit[text[idx_q - 1:idx_q]] * 1000
        if idx_b != -1:
            num += digit[text[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的处理
            num += digit.get(text[idx_s - 1:idx_s], 1) * 10
        if text[-1] in digit:
            num += digit[text[-1]]
    return num


def per_num(text):
    string = re.findall(r"\d+", text)
    if len(string) == 0:
        r1 = re.compile(u'[一二两三四五六七八九十]{1,}')
        r2 = r1.findall(text)
        if len(r2) == 0:
            num = 1
        else:
            num = text2num(r2)
    else:
        num = string[0]
    return num

def extract_death_number(content):
    # 提取出死亡数字
    # 死亡人数、重伤人数、轻伤人数提取
    if content == None:
        return 0
    r1 = re.compile(u'[1234567890一二两三四五六七八九十 ]*人( )*死亡') #致几人死亡
    r2 = re.search(r1, content)
    if r2 is None:
        r3 = re.compile(u'致.{0,8}人( )*死亡') #致受害人死亡
        r4 = re.search(r3, content)
        if r4 is None:
            num1 = 0
        else:
            num1 = 1
    else:
        text = r2.group()
        num1 = per_num(text)
    return num1

def extract_seg(content):
    if content == None:
        return 0, 0, 0
    # 轻微伤人数、轻伤人数、重伤人数提取
    r1 = re.compile(u'[1234567890一二两三四五六七八九十 ]*人( )*轻微伤')
    r2 = re.search(r1, content)
    if r2 is None:
        r11 = re.compile(u'致.{0,8}人( )*轻微伤')  # 致受害人轻微伤/致人轻微伤
        r22 = re.search(r11, content)
        if r22 is None:
            num1 = 0
        else:
            num1 = 1
    else:
        text = r2.group()
        num1 = per_num(text)
    # 轻伤人数
    r3 = re.compile(u'[1234567890一二两三四五六七八九十 ]*人( )*轻伤')
    r4 = re.search(r3, content)
    if r4 is None:
        r33 = re.compile(u'致.{0,8}人( )*轻伤')  # 致受害人轻伤/致人轻伤
        r44 = re.search(r33, content)
        if r44 is None:
            num2 = 0
        else:
            num2 = 1
    else:
        text = r4.group()
        num2 = per_num(text)
    # 重伤人数
    r5 = re.compile(u'[1234567890一二两三四五六七八九十 ]*人( )*重伤')
    r6 = re.search(r5, content)
    if r6 is None:
        r55 = re.compile(u'致.{0,8}人( )*重伤')  # 致受害人重伤/致人重伤
        r66 = re.search(r55, content)
        if r66 is None:
            num3 = 0
        else:
            num3 = 1
    else:
        text = r6.group()
        num3 = per_num(text)
    return num1, num2, num3


def sentence_result_number(content):
    '''提取出判决结果，单位为月份'''
    if content == None:
        return 0
    r1 = re.compile(u'(有期徒刑|拘役)[一二三四五六七八九十又年零两]{1,}(个月|年)')
    r2 = re.search(r1, content[0])
    if r2 is None:
        num = 0
    else:
        text = r2.group()
        r3 = re.compile(u'[一二三四五六七八九十两]{1,}')
        r4 = r3.findall(text)
        if len(r4) > 1:
            num1 = text2num(r4[0])
            num2 = text2num(r4[1])
            num = 12 * num1 + num2
        elif text.find(u"年") != -1:
            num = 12 * text2num(r4)
        else:
            num = text2num(r4)
    return num

def get_event_elements(case_file):
    """
    将案件中属于同一事件要素的词语合并，最终返回完整的事件要素
    :param case_file: 记录单个案件的文本文件
    :return event_elements: 返回一个字典，键为事件要素类型，值为对应的事件要素组成的list
    """
    words = []  # 保存所有属于事件要素的单词
    element_types = []  # 保存上述单词对应的事件要素类型

    with open(case_file, "r", encoding='utf-8') as f1:
        rows = []
        # 将文本转换成list，方便后续处理
        for line in f1.readlines():
            rows.append(line.strip("\n").split("\t"))

        for index, row in enumerate(rows):
            if "S" in row[-1]:
                # S出现在最后一个位置，说明这是一个单独的事件要素，将其加入words列表
                words.append(row[0])
                element_types.append(row[-1][-1])

            elif "B" in row[-1]:
                # 处理由多个单词组成的事件要素
                words.append(row[0])
                element_types.append(row[-1][-1])
                j = index + 1
                while "I" in rows[j][-1] or "E" in rows[j][-1]:
                    words[-1] += rows[j][0]
                    j += 1
                    if j == len(rows):
                        break

        # 将事件要素进行分类（将words列表中的元素按照类别分成6类）
        T = []  # 投案
        G = []  # 如实供述
        Z = []  # 自首
        R = []  # 认罪
        P = []  # 赔偿
        Q = []  # 取得谅解

        for i in range(len(element_types)):
            if element_types[i] == "T":
                T.append(words[i])
            elif element_types[i] == "G":
                G.append(words[i])
            elif element_types[i] == "Z":
                Z.append(words[i])
            elif element_types[i] == "R":
                R.append(words[i])
            elif element_types[i] == "P":
                P.append(words[i])
            elif element_types[i] == "Q":
                Q.append(words[i])

        # 整理抽取结果
        event_elements = dict()  # 用字典存储各类事件要素
        event_elements["投案"] = remove_duplicate_elements(T)
        event_elements["如实供述"] = remove_duplicate_elements(G)
        event_elements["自首"] = remove_duplicate_elements(Z)
        event_elements["认罪"] = remove_duplicate_elements(R)
        event_elements["赔偿"] = remove_duplicate_elements(P)
        event_elements["取得谅解"] = remove_duplicate_elements(Q)

        # 打印出完整的事件要素
        # for key, value in event_elements.items():
        #     print(key, value)

        return event_elements

def get_crime_stage(content):
    """
        得到犯罪阶段

    """
    if content == None:
        return "0"
    r1 = re.compile(u'预备')
    r2 = re.search(r1, content)
    if r2 != None:
        return "1"
    else:
        r3 = re.compile(u'(未遂|中止)')
        r4 = re.search(r3, content)
        if r4 != None:
            return "2"
        else:
            r5 = re.compile(u'既遂')
            r6 = re.search(r5, content)
            if r6 != None:
                return "3"
            else:
                return "0"

def judge_T_F(content):
    """
    事件要素值为False or True 的转化为数值
    """
    if(content == None):
        return "-1"  #这里主要针对没有主动提到前科问题
    elif (content == True):
        return "1"
    else :
        return "0"


def get_patterns(event_elements):
    """
    将提取出的事件要素转换成特征
    :param event_elements: 字典形式的事件要素
    :return patterns: 字典形式的特征
    """
    patterns = dict()

    # 从事件要素中的"死亡情况"提取出特征：01死亡人数
    patterns["01死亡人数"] = extract_death_number(event_elements["死亡情况"])

    # 从事件要素中的"受伤情况"提取出三个特征：02轻微伤人数、03轻伤人数、04重伤人数
    patterns["02轻微伤人数"], patterns["03轻伤人数"], patterns["04重伤人数"] = extract_seg(event_elements["受伤情况"])

    # 从事件要素中的"罪名"提取出特征：05罪名
    if event_elements["罪名"] == "故意伤害罪":
        patterns["05罪名"] = "1"
    elif event_elements["罪名"] == "故意杀人罪":
        patterns["05罪名"] = "2" # 故意杀人罪
    else:
        patterns["05罪名"] = "0"

    # 从事件要素中的"犯罪阶段"提取出特征：06犯罪阶段
    if (patterns["05罪名"] == 1) or (event_elements["犯罪阶段"] == None):
        patterns["06犯罪阶段"] = "0"
    else:
        patterns["06犯罪阶段"] = get_crime_stage(event_elements["犯罪阶段"])

    patterns["07是否投案"] = find_element(event_elements["投案"], "拨打110报警电话", "自动投案", "主动投案",  "主动要求他人帮忙报案")
    patterns["08是否如实供述"] = find_element(event_elements["如实供述"], "如实供述", "系坦白", "系坦白", "具有坦白情节", "主动供述", "主动交代")

    if patterns["07是否投案"] == "1" and patterns["08是否如实供述"] == "1":
        patterns["09是否自首"] = "1"
    else:
        patterns["09是否自首"] = find_element(event_elements["自首"], "是自首", "属自首", "构成自首", "具有自首情节")

    patterns["10是否认罪"] = find_element(event_elements["认罪"], "自愿认罪认罚",  "自愿认罪",  "认罪认罚",  "认罪态度较好")
    patterns["11是否赔偿"] = find_element(event_elements["赔偿"], "赔偿")
    patterns["12是否取得谅解"] = find_element(event_elements["取得谅解"], "谅解")

    patterns["13是否立功"] = judge_T_F(event_elements["是否立功"])
    patterns["14是否限制刑事责任能力"] = judge_T_F(event_elements["是否限制刑事责任能力"])
    patterns["15是否有前科"] = judge_T_F(event_elements["是否有前科"])
    patterns["16被害人是否有过错"] = judge_T_F(event_elements["被害人是否有过错"])

    patterns["判决结果"] = sentence_result_number(event_elements["判决结果"])

    return patterns