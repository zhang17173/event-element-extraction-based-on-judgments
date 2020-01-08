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
        return searchObj01.group(1)
    elif searchObj02:
        return searchObj02.group(1)
    elif searchObj03:
        return searchObj03.group(1)
    else:
        return None


def damage(input):
    '''提取受伤情况，如：经鉴定戴某某因外伤致左眼眶下壁骨折和左侧上颌窦前壁骨折构成轻伤二级'''
    re_damage = re.compile(r'经.*?(鉴定|诊断).*?(轻微伤|[轻重]伤(.级)?)')
    searchObj = re_damage.search(input)
    if searchObj:
        return searchObj.group(2)
    else:
        return None

def death(input):
    '''提取死亡人数，如：致n人死亡'''
    re_death = re.compile(r'致.[0,8]死亡')
    searchObj = re_death.search(input)
    if searchObj:
        return searchObj.group()
    else:
        return None

def crime_stage(input):
    '''对故意杀人案件提取犯罪阶段'''
    re_crime_stage = re.compile(
        r'(属|属于|系|是|具有|构成|认定为|认定其为)(犯罪预备|犯罪中止|犯罪未遂|犯罪既遂|未遂|杀人未遂|故意杀人罪未遂)')
    searchObj = re_crime_stage.search(input)
    if searchObj:
        return searchObj.group(2)
    else:
        return None


def victim_fault(input):
    '''提取被害人是否有过错，如：被害人郭某酒后失控无端追打王某在案发起因上有一定过错责任'''
    re_victim_fault = re.compile(r"被害人.{1,30}过错")
    search_victim_fault = re_victim_fault.search(input)
    if search_victim_fault:
        return search_victim_fault.group()
    else:
        return None


def crime_name(input):
    '''提取罪名，如：被告人刘某某犯故意伤害罪'''
    re_crime_name = re.compile(r'被告人.*?犯(.*?罪)')
    searchObj = re_crime_name.search(input)
    if searchObj:
        return searchObj.group(1)
    else:
        return None


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

    sentence = []

    if search_death:
        sentence.append(search_death.group(1))
    if search_life_imprison:
        sentence.append(search_life_imprison.group(1))
    if search_fixed_time_imprison:
        sentence.append(search_fixed_time_imprison.group(1))
    if search_probation:
        sentence.append(search_probation.group(1))

    if sentence:
        return sentence
    else:
        return None


def limited_responsibility(input):
    '''是否为限定刑事责任能力'''
    re_limited_responsibility = re.compile(r'(系|为|是|属于|属|具有|有)限定刑事责任能力(人)?')
    searchObj = re_limited_responsibility.search(input)
    if searchObj:
        return searchObj.group()
    else:
        return None


def pedigree(input):
    '''前科记录：'''
    re_pedigree01 = re.compile(r'((有(多次)?前科(劣迹)?(情况)?)|系累犯)')
    re_pedigree02 = re.compile(r'(系(初犯)?(偶犯)?)|((无|没有)前科(劣迹)?(情况)?)')
    searchObj01 = re_pedigree01.search(input)
    searchObj02 = re_pedigree02.search(input)
    if searchObj01:
        return True
    elif searchObj02:
        return False
    else:
        return None


def extract_all(input):
    '''提取所有事件要素'''
    print(damage(input))
    print(crime_stage(input))
    print(contribute(input))
    print(pedigree(input))
    print(victim_fault(input))
    print(limited_responsibility(input))
    print(crime_name(input))
    print(sentence_result(input))

