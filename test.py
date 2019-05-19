#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/5/19 13:13
# @Filename :test.py
import re

from fontTools import unichr
from fontTools.ttLib import TTFont

ocr = """
 .012456789吧界居价引存由己日久么远
美期响有愿当史书常决弟独越计写视杀生给标律拿喜
第记帝现投科间一容快据相县敌文空总内如虽仍着原
组父客四交较率义社结谓即系息者皇于易取营余护定
除图曾臣住处太左笑商术议置特至按尽还师准委强足
讲儿费们级黑希黄经保火兵兴区百士调连每线二甚深
万失又点右极工心让断校家改官诸它制你另单务卫告
更分非长与阳装飞往斯属食名精或直任道拉阿局头母
信安联语皆后切两观照导前提关里产应外去绝影小在
资色落统止最某技汉若之答服口院大同乃展治约几春
况因船怎边果国持亚奇情形办首收新干古便省元离职
题却进设列下全完步得整被倒员次白支司眼报以能好
动活何本案事比防明质集走证石注受陈种念衣英数车
威品传反众山算管似善许守红老重领样花想用围依风
了满世场主只増条""".replace('\n', '')
print(len(ocr))

font = TTFont('tyc-num5-19.woff')  # 打开文件
# font.saveXML('./tyc-num.xml')
mappings = {}
for k, v in font.getBestCmap().items():
    if v.startswith('uni'):
        # 形如 <map code="0xe040" name="uni45"/>  可直接转换得到结果
        mappings['{:x}'.format(k)] = unichr(int(v[3:], 16))
    else:
        mappings['{:x}'.format(k)] = v

i = '管'
print(type(i))
key = re.search('.*u([0-9a-f]{4}).*', str(i.encode('unicode_escape'))).group(1)
value = mappings[key]
# 得到另一个映射
id = font.getGlyphID(value)
print(ocr[id])
