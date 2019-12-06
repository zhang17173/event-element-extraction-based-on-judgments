import re


def damage(input):
    '''提取伤亡情况'''
    re_damage = re.compile(r'经.*?(鉴定|诊断).*?(轻微伤|[轻|重]伤(.级)?)')
    searchObj = re_damage.search(input)
    if searchObj:
        print("伤亡情况："+searchObj.group(2))
    else:
        print("未找到伤亡情况！！！")


def crime_stage(input):
    '''对故意杀人案件提取犯罪阶段'''
    re_crime_stage = re.compile(
        r'(属|属于|系|是|具有|构成|认定为|认定其为)(犯罪预备|犯罪中止|犯罪未遂|犯罪既遂|未遂|杀人未遂|故意杀人罪未遂)')
    searchObj = re_crime_stage.search(input)
    if searchObj:
        print("犯罪阶段："+searchObj.group(2))
    else:
        print("未查找到犯罪阶段！！！")


def victim_fault(input):
    '''提取被害人是否有过错'''
    re_victim_fault = re.compile(r"被害人.{1,10}过错")
    search_victim_fault = re_victim_fault.search(input)
    if search_victim_fault:
        print(search_victim_fault.group())
    else:
        print("未找到被害人过错")


def crime_name(input):
    '''提取罪名'''
    re_crime_name = re.compile(r'判决如下.*?被告人.*?犯(.*?罪)')
    searchObj = re_crime_name.search(input)
    if searchObj:
        print("认定罪名："+searchObj.group(1))
    else:
        print("未查找到罪名")


def sentence_result(input):
    '''提取判决结果'''
    re_death = re.compile(r'判处(死刑(缓期.年执行)?)')
    re_life_imprison = re.compile(r'判处(无期徒刑)')
    re_fixed_time_imprison = re.compile(r'判处(有期徒刑(.{0,2}年)?(.{0,2}月)?)')
    re_probation = re.compile(r'判处有期徒刑.*?(缓刑(.{0,2}年)?(.{0,2}月)?)')

    search_death = re_death.search(input)
    search_life_imprison = re_life_imprison.search(input)
    search_fixed_time_imprison = re_fixed_time_imprison.search(input)
    search_probation = re_probation.search(input)
    if search_death:
        print(search_death.group(1))
    if search_life_imprison:
        print(search_life_imprison.group(1))
    if search_fixed_time_imprison:
        print(search_fixed_time_imprison.group(1))
    if search_probation:
        print(search_probation.group(1))


def extract_all(input):
    '''提取所有事件要素'''
    damage(input)
    crime_stage(input)
    victim_fault(input)
    crime_name(input)
    sentence_result(input)


f = open("data/input.txt", "r", encoding="utf-8")
extract_all(f.read())
