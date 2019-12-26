import re


def contribute(input):
    '''提取立功情况'''
    re_contribute01 = re.compile(r'经查证属实((具有|属|有|为|是)立功(表现|情节)?)')
    re_contribute02 = re.compile(r'((具有|属|有|为|是)立功(表现|情节)?).*?予以采[信纳]')
    re_contribute03 = re.compile(r'鉴于.*?((属|属于|有)立功(表现|情节)?)')
    searchObj01 = re_contribute01.search(input)
    searchObj02 = re_contribute02.search(input)
    searchObj03 = re_contribute03.search(input)
    if searchObj01:
        print(searchObj01.group(1))
    elif searchObj02:
        print(searchObj02.group(1))
    elif searchObj03:
        print(searchObj03.group(1))
    else:
        print("未找到立功情况!!!")


def damage(input):
    '''提取伤亡情况，如：经鉴定戴某某因外伤致左眼眶下壁骨折和左侧上颌窦前壁骨折构成轻伤二级'''
    re_damage = re.compile(r'经.*?(鉴定|诊断).*?(轻微伤|[轻重]伤(.级)?)')
    searchObj = re_damage.search(input)
    if searchObj:
        print(searchObj.group(2))
    else:
        print("未找到伤亡情况!!!")


def crime_stage(input):
    '''对故意杀人案件提取犯罪阶段'''
    re_crime_stage = re.compile(
        r'(属|属于|系|是|具有|构成|认定为|认定其为)(犯罪预备|犯罪中止|犯罪未遂|犯罪既遂|未遂|杀人未遂|故意杀人罪未遂)')
    searchObj = re_crime_stage.search(input)
    if searchObj:
        print(searchObj.group(2))
    else:
        print("未查找到犯罪阶段!!!")


def victim_fault(input):
    '''提取被害人是否有过错，如：被害人郭某酒后失控无端追打王某在案发起因上有一定过错责任'''
    re_victim_fault = re.compile(r"被害人.{1,30}过错")
    search_victim_fault = re_victim_fault.search(input)
    if search_victim_fault:
        print(search_victim_fault.group())
    else:
        print("未找到被害人过错")


def crime_name(input):
    '''提取罪名，如：被告人刘某某犯故意伤害罪'''
    re_crime_name = re.compile(r'被告人.*?犯(.*?罪)')
    searchObj = re_crime_name.search(input)
    if searchObj:
        print(searchObj.group(1))
    else:
        print("未查找到罪名!!!")


def sentence_result(input):
    '''提取判决结果，如：判处拘役五个月'''
    re_death = re.compile(r'判处(死刑(缓期.年执行)?)')
    re_life_imprison = re.compile(r'判处(无期徒刑)')
    re_fixed_time_imprison = re.compile(r'判处((有期徒刑|拘役)(.{0,2}年)?(.{0,2}月)?)')
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


def limited_responsibility(input):
    '''是否为限定刑事责任能力'''
    re_limited_responsibility = re.compile(r'(系|为|是|属于|属|具有|有)限定刑事责任能力(人)?')
    searchObj = re_limited_responsibility.search(input)
    if searchObj:
        print(searchObj.group())
    else:
        print("未找到是否限定刑事责任能力情况！！！")


def pedigree(input):
    '''前科记录：'''
    re_pedigree01 = re.compile(r'([有|无|没有|其](多次)?前科(劣迹)?(情况)?)')
    re_pedigree02 = re.compile(r'系[初犯|累犯](偶犯)?')
    searchObj01 = re_pedigree01.search(input)
    searchObj02 = re_pedigree02.search(input)
    if searchObj01:
        print(searchObj01.group())
    elif searchObj02:
        print(searchObj02.group())
    else:
        print("未找到前科情况！！！")


def extract_all(input):
    '''提取所有事件要素'''
    contribute(input)
    damage(input)
    crime_stage(input)
    victim_fault(input)
    crime_name(input)
    sentence_result(input)


f = open("data/new_input.txt", "r", encoding="utf-8")
extract_all(f.read())
