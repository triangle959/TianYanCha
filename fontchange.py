#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/5/16 21:37
# @Filename :fontchange.py
from fontTools import unichr
from fontTools.ttLib import TTFont
import re
import requests

ocr = """
 .012345679易给将兴革酒报律工机连生五广风卷况产击老过江
其朝底息宫西场系着事片导规交初社应器术实先气类子活陈七定队围火州汉
见加青山军像运离结集音土白降诸天奇分科守罗受众构企局承至望话所落处
章干善来得观务问取六黄与臣统强具理決题重根龙照行太讲万考谈失说心主
干南较苏甚族送如支件各常益志曾单令案往原品房性字党严害都上谁出乐提
代派皇笑调则首客许费想新前夜法农任视古容影自群际平钱还研认纪推余做
保叫可四进起吃本对教利随越察里技差情争电点头百示夫变文异周很条今尽
反表信道意希回从府路要独而期转语拉么也能留存包领共始关面列装为现克
八亚让数明响黑比杀展整长目特式便求调病验满校个轻用标价言物既日阿答
命每何置组总作确神怎致约者业金开由宝儿只刻化飞攻线早必己河住感元引
未弟历思欲施断德切手流识边传跟""".replace('\n', '')
print(len(ocr))

def fontchange(str1):
    font = TTFont('tyc-num5-22.woff')  # 打开文件
    # font.saveXML('./tyc-num.xml')
    mappings = {}
    for k, v in font.getBestCmap().items():
        if v.startswith('uni'):
            # 形如 <map code="0xe040" name="uni45"/>  可直接转换得到结果
            mappings['{:x}'.format(k)] = unichr(int(v[3:], 16))
        else:
            mappings['{:x}'.format(k)] = v
    num_dict = {
        '5':'0',
        '9':'1',
        '7':'2',
        '4':'3',
        '1':'4',
        '6':'5',
        '2':'6',
        '0':'7',
        '8':'8',
        '3':'9'
    }
    list1 = []
    for i in str1:
        try:
            if i.isdigit():
                # new_str = new_str.join(num_dict[i])
                list1.append(''.join(num_dict[i]))
            else:
                key = re.search('.*u([0-9a-f]{4}).*', str(i.encode('unicode_escape'))).group(1)
                value = mappings[key]
                # 得到另一个映射
                id = font.getGlyphID(value)
                list1.append(''.join(ocr[id]))
        except Exception:
            list1.append(i)
    return ''.join(str(x) for x in list1)

