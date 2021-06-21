#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

class GenericNER:
    def __init__(self, locale=None):
        self.mainDishSTR = "([乳包味啡嗲奶心手排果柳棗椒油湯漿炒焿煎煙燒爐瓜皮盅盤米粄粉粑粥粽粿糊糍粑糕糖糬糰線羹翅翼肉肚肺肝膽腐腦腩腳腸胃腿胗芛薏花茄茶草莓菊菜蓮蔗蔥薑蒜薩薯蘆蕉蜜筍檳豆豉栗菇虱蚵蛋卵蝦蟹螺貝蟳血角酒酥醬趖銼鍋雜頭飩飯飴餃飩餅麵麩餐骨鬆鬚魚鯧鰻鮪鮭魽鯛鰾鱉龜雞鴨鵝牛豬羊兔鼠鴿豚鷄堡]|"
        self.sideDishSTR = "[丸冰圓塊卷捲粄條扒仔乾]|[俄德法美日義英西歐中台泰越韓粵港]式|星州|客家|花枝|鴛鴦|石斑|黑輪|伯勞|藥燉|愛玉|珍珠|熱狗|阿給|燒賣|料理|飲料|糖[水醋]|鳳梨|蜜餞|花生|[壽土吐]司|便當|飯盒|鍋貼|扁食|雲吞|刺身|山蘇|多士|咖哩|沙拉|沙母|沙公|海參|鴨賞|旗魚|燒賣|海鮮|河鮮|龍珠|鮟鱇|牛河|熊掌|糕渣|自助餐|沙威[馬瑪]|三明治|沙淇瑪|原住民|棺材板|官財板|地瓜球|綠豆椪|冰淇淋|佛跳牆|[洋和][菓果]子)"
        self.cookMethodSTR = "[煎煮燉炒炸蒸煨魯滷漬醃炊爆燒拌剝湯焢焗烘烤佐釀涮火]"
        self.cookModSTR = "([麻辣酸清]|酥[脆炸]|[蔥薑蒜]爆|[干乾紅]燒){1,2}"
        self.extenedLIST = [("串燒", "(<ACTION_verb>串燒</ACTION_verb>)"),
                            ("烤肉", "(<ACTION_verb>烤肉</ACTION_verb>)"),
                            ("切雞", "(<VerbP>切雞</VerbP>)"),
                            ("炒蛋", "(<VerbP>炒蛋</VerbP>)"),
                            ("煎蛋", "(<VerbP>煎蛋</VerbP>)"),
                            ("烘蛋", "(<VerbP>烘蛋</VerbP>)"),
                            ("炒蝦", "(<VerbP>炒蝦</VerbP>)"),
                            ("叉燒", "(<ENTITY_oov>叉</ENTITY_oov><ACTION_verb>燒</ACTION_verb>)"),
                            ("卷煎", "(<ENTITY_oov>卷</ENTITY_oov><ACTION_verb>煎</ACTION_verb>)"),
                            ("阿拜", "(<ENTITY_nouny>阿</ENTITY_nouny><ACTION_verb>拜</ACTION_verb>)"),
                            ("吉拿富", "(<MODIFIER>吉</MODIFIER><ACTION_verb>拿富</ACTION_verb>)"),
                            #<日式食物名：動詞在後>
                            ("手捲", "(<ENTITY_oov>手</ENTITY_oov><ACTION_verb>捲</ACTION_verb>)"),
                            ("犬首燒", "(<ENTITY_oov>犬首</ENTITY_oov><ACTION_verb>燒</ACTION_verb>)"),
                            ("銅鑼燒", "(<ENTITY_oov>銅鑼</ENTITY_oov><ACTION_verb>燒</ACTION_verb>)"),
                            ("大雕燒", "(<ENTITY_nouny>大雕</ENTITY_nouny><ACTION_verb>燒</ACTION_verb>)"),
                            ("貓掌燒", "(<ENTITY_oov>貓掌</ENTITY_oov><ACTION_verb>燒</ACTION_verb>)"),
                            ("關東煮", "(<ENTITY_noun>關東煮</ENTITY_noun>)"),
                            ("廣島燒", "(<ENTITY_noun>廣島燒</ENTITY_noun>)"),
                            ("大阪燒", "(<ENTITY_noun>大阪燒</ENTITY_noun>)"),
                            ("雞白湯拉麵", "(<ENTITY_oov>雞</ENTITY_oov><MODIFIER_color>白</MODIFIER_color><ENTITY_nounHead>湯拉麵</ENTITY_nounHead>)"),
                            ("漢堡排", "(<ENTITY_oov>漢堡</ENTITY_oov><ACTION_verb>排</ACTION_verb>)"),
                            #</日式食物名：動詞在後>
                            ("宮保", "(<ENTITY_oov>宮</ENTITY_oov><ACTION_verb>保</ACTION_verb>)"),
                            ("西多士", "(<ENTITY_oov>西</ENTITY_oov><ENTITY_nouny>多士</ENTITY_nouny>)"),
                            ("漢堡包", "(<ENTITY_oov>漢堡</ENTITY_oov><ACTION_verb>包</ACTION_verb>)"),
                            ("黑貓包", "(<ENTITY_nounHead>黑貓</ENTITY_nounHead><ACTION_verb>包</ACTION_verb>)"),
                            ("飯包", "(<ENTITY_oov>飯</ENTITY_oov><ACTION_verb>包</ACTION_verb>)"),
                            ("煎釀三寶", "(<ACTION_verb>煎釀</ACTION_verb><ENTITY_num>三</ENTITY_num><ENTITY_oov>寶</ENTITY_oov>)"),
                            ("乾炒牛河", "(<ACTION_verb>乾</ACTION_verb><ACTION_verb>炒</ACTION_verb><ENTITY_nouny>牛河</ENTITY_nouny>)"),
                            ("星州炒米", "(<ENTITY_oov>星洲</ENTITY_oov><VerbP>炒米</VerbP>)"),
                            ("醃腸熟肉", "(<VerbP>醃腸</VerbP><ENTITY_nouny>熟肉</ENTITY_nouny>)"),
                            ("三文治", "(<ENTITY_num>三</ENTITY_num><ENTITY_oov>文</ENTITY_oov><ACTION_verb>治</ACTION_verb>)"),
                            ("五柳枝魚", "(<ENTITY_num>五</ENTITY_num><ENTITY_nouny>柳枝魚</ENTITY_nouny>)"),
                            ("浮水虱目魚羹", "(<VerbP>浮水</VerbP><ENTITY_noun>虱目魚羹</ENTITY_noun>)"),
                            ("咕咾肉", "(<ENTITY_oov>咕咾</ENTITY_oov><ENTITY_nounHead>肉</ENTITY_nounHead>)"),
                            ("三杯中卷", "(<ENTITY_classifier>三杯</ENTITY_classifier><RANGE_locality>中</RANGE_locality><ENTITY_oov>卷</ENTITY_oov>)"),
                            ("三杯小卷", "(<ENTITY_classifier>三杯</ENTITY_classifier><ENTITY_nouny>小卷</ENTITY_nouny>)"),
                            ("五更腸旺", "(<TIME_justtime>五更</TIME_justtime><ENTITY_oov>腸旺</ENTITY_oov>)"),
                            ("下水湯", "(<ACTION_verb>下水</ACTION_verb><ENTITY_nouny>湯</ENTITY_nouny>)"),
                            ("西魯肉", "(<ENTITY_oov>西魯</ENTITY_oov><ENTITY_nounHead>肉</ENTITY_nounHead>)"),
                            ("九層塔", "(<ENTITY_classifier>九層</ENTITY_classifier><ENTITY_nouny>塔</ENTITY_nouny>)"),
                            ("青蛙下蛋", "(<ENTITY_nounHead>青蛙</ENTITY_nounHead><ACTION_verb>下蛋</ACTION_verb>)"),
                            ("春卷", "(<TIME_season>春</TIME_season><ENTITY_nouny>卷</ENTITY_nouny>)"),
                            ("黑白切", "(<MODIFIER_color>黑</MODIFIER_color><MODIFIER_color>白</MODIFIER_color><ACTION_verb>切</ACTION_verb>)"),
                            ("臘八粥", "(<ENTITY_oov>臘</ENTITY_oov><ENTITY_num>八</ENTITY_num><ENTITY_nounHead>粥</ENTITY_nounHead>)"),
                            ("八寶粥", "(<ENTITY_num>八</ENTITY_num><ENTITY_nouny>寶粥</ENTITY_nouny>)"),
                            ("八寶冬粉", "(<ENTITY_num>八</ENTITY_num><ENTITY_oov>寶冬粉</ENTITY_oov>)"),
                            ("五色冷盤", "(<ENTITY_num>五</ENTITY_num><ENTITY_oov>色</ENTITY_oov><ENTITY_nouny>冷盤</ENTITY_nouny>)"),
                            ("蒼蠅頭", "(<ENTITY_oov>蒼蠅頭</ENTITY_oov>)"),
                            ("炒餌塊", "(<ACTION_verb>炒</ACTION_verb><ENTITY_nouny>餌塊</ENTITY_nouny>)"),
                            ("餌絲", "(<ENTITY_oov>餌</ENTITY_oov><ENTITY_classifier>絲</ENTITY_classifier>)"),
                            ("大救駕", "(<MODIFIER>大</MODIFIER><ACTION_verb>救駕</ACTION_verb>)"),
                            ("螞蟻上樹", "(<ENTITY_oov>螞蟻</ENTITY_oov><ACTION_verb>上樹</ACTION_verb>)"),
                            ("韭菜盒子", "(<ENTITY_oov>韭菜</ENTITY_oov><ENTITY_noun>盒子</ENTITY_noun>)"),
                            ("黯然銷魂飯", "(<MODIFIER>黯然</MODIFIER><ENTITY_nounHead>銷魂飯</ENTITY_nounHead>)")
                            ]
        self.escapeTUPLE = ("原住民", "客家", "俄式", "德式", "法式", "美式", "日式", "義式", "英式", "西式", "歐式", "中式", "台式", "泰式", "越式", "韓式", "粵式", "港式", "星州", "大塊", "菜單", "味")

        self.foodPat = re.compile("{0}|(<ACTION_verb>[^<]*?{1}+?[^<]*?</ACTION_verb>)?(<MODIFIER>{2}</MODIFIER>)?(<KNOWLEDGE_chemical>酸</KNOWLEDGE_chemical>)?(<MODIFIER_color>[黑紅]</MODIFIER_color>)?(<ENTITY_classifier>三杯</ENTITY_classifier>)?((<ENTITY_nounHead>[^<]*?{3}+[^<民]*?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]*?{3}+[^<民]*?</ENTITY_nouny>)|(<ENTITY_noun>[^<]*?{3}+[^<民]*?</ENTITY_noun>)|(<ENTITY_oov>[^<]*?{3}+[^<民]*?</ENTITY_oov>|<VerbP>{1}{3}</VerbP>))".format("|".join([p[1] for p in self.extenedLIST]), self.cookMethodSTR, self.cookModSTR, self.mainDishSTR+self.sideDishSTR))
        self.foodPatWLoc = re.compile(r"""{0}|
        (<LOCATION>[^<]+?</LOCATION>)?
        ((<ENTITY_nounHead>[^<]*?({1})+[^<]*?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]*?({1})+[^<]*?</ENTITY_nouny>)|(<ENTITY_noun>[^<]*?({1})+[^<]*?</ENTITY_noun>)|(<ENTITY_oov>[^<]*?({1})+[^<]*?</ENTITY_oov>))?
        (<ACTION_verb>[^<]*?{2}+?[^<]*?</ACTION_verb>)?
        (<MODIFIER>{3}</MODIFIER>)?
        (<KNOWLEDGE_chemical>酸</KNOWLEDGE_chemical>)?
        (<MODIFIER_color>[黑紅]</MODIFIER_color>)?
        (<ENTITY_classifier>三杯</ENTITY_classifier>)?
        ((<ENTITY_nounHead>[^<]*?{4}+[^<民]*?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]*?{4}+[^<民]*?</ENTITY_nouny>)|(<ENTITY_noun>[^<]*?{4}+[^<民]*?</ENTITY_noun>)|(<ENTITY_oov>[^<民]*?{4}+[^<]*?</ENTITY_oov>))""".format("|".join([p[1] for p in self.extenedLIST]),
                                                                                                                                                                                                                           "|".join(self.escapeTUPLE[:-2]),
                                                                                                                                                                                                                           self.cookMethodSTR,
                                                                                                                                                                                                                           self.cookModSTR,
                                                                                                                                                                                                                           self.mainDishSTR+self.sideDishSTR), re.X)

        self.agePat         = None
        self.anglePat       = None
        self.capacityPat    = None
        self.fractionPat    = None
        self.frequencyPat   = None
        self.lengthPat      = None
        self.locationPat    = None
        self.measurePat     = None
        self.percentPat     = None
        self.ratePat        = None
        self.speedPat       = None
        self.temperaturePat = None
        self.weightPat      = None
        self.areaPat        = None
        self.datePat        = None
        self.timePat        = None
        self.durationPat    = None
        self.integerPat     = None
        self.decimalPat     = None
        self.ordinalPat     = None
        self.currencyPat = re.compile("(?<=<KNOWLEDGE_currency>)[^<]*?(?=</KNOWLEDGE_currency>)")
        self.currencyGreedyPat = re.compile("(?<=[元金幣圜圓比布索鎊盾銖令朗郎]</ENTITY_noun><ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
        self.currencyGreedyGapPat = re.compile("(?<=^<ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
        self.personPat      = None
        self.pronounPat     = None
        self.organizationPat = None
        self.wwwPat         = None

        self.stripPat = re.compile("</?[A-Za-z]+?_?[A-Za-z]*?>")
        self.stripPatNAIVE = re.compile("(?<=>).*?(?=<)")

    def _segIndexConverter(self, ArticutResultDICT, posIndexLIST):
        '''
        Convert posIndex to segIndex. Token can be crossed.
        Return list
        '''
        if type(posIndexLIST) is list and "result_pos" in ArticutResultDICT:
            pass
        else:
            return None
        try:
            for sentenceINDEX in range(0, len(ArticutResultDICT["result_pos"])):
                if len(ArticutResultDICT["result_pos"][sentenceINDEX]) == 1: # 略過標點符號
                    pass
                else:
                    sentenceSTR = self.stripPat.sub("", ArticutResultDICT["result_pos"][sentenceINDEX])
                    refINDEX = 0
                    for i in posIndexLIST[sentenceINDEX]:
                        startINDEX = sentenceSTR[refINDEX:].find(i[2])
                        endINDEX   = startINDEX + len(i[2])
                        i[0] = refINDEX + startINDEX
                        i[1] = refINDEX + endINDEX
                        refINDEX = i[1]
        except Exception:
            print("Invalid posIndexLIST format")
            return None
        return posIndexLIST

    def _segIndexConverterNAIVE(self, ArticutResultDICT, posIndexLIST):
        if type(posIndexLIST) is list and "result_pos" in ArticutResultDICT:
            pass
        else:
            return None

        segIndexLIST = []
        try:
            for i, posLIST in enumerate(posIndexLIST):
                if posLIST:
                    tmpLIST = []
                    for start, end, seg in posLIST:
                        posEndSTR = ArticutResultDICT["result_pos"][i][:start]
                        segEndSTR = "".join([x.group() for x in self.stripPatNAIVE.finditer(posEndSTR)])
                        tmpLIST.append([len(segEndSTR), len(segEndSTR)+len(seg), seg])
                    segIndexLIST.append(tmpLIST)
                else:
                    segIndexLIST.append(posLIST)
        except Exception:
            print("Invalid posIndexLIST format")
            return None
        return segIndexLIST

    def _getFood(self, ArticutResultDICT, withLocation=False, indexWithPOS=True):

        resultLIST = []
        if withLocation == False:
            self.pat = self.foodPat
        else:
            self.pat = self.foodPatWLoc

        for p in ArticutResultDICT["result_pos"]:
            if len(p) > 1:
                resultLIST.append([[f.start(), f.end(), self.stripPat.sub("", f.group(0))] for f in list(self.pat.finditer(p)) if self.stripPat.sub("", f.group(0)) not in self.escapeTUPLE])
            else:
                resultLIST.append([])

        for sentenceINDEX in range(0, len(resultLIST)):
            for foodINDEX in range(0, len(resultLIST[sentenceINDEX])-1):
                if resultLIST[sentenceINDEX][foodINDEX][0] != None:
                    if resultLIST[sentenceINDEX][foodINDEX][1] == resultLIST[sentenceINDEX][foodINDEX+1][0]:
                        resultLIST[sentenceINDEX][foodINDEX][1] = resultLIST[sentenceINDEX][foodINDEX+1][1]
                        resultLIST[sentenceINDEX][foodINDEX][2] = resultLIST[sentenceINDEX][foodINDEX][2] + resultLIST[sentenceINDEX][foodINDEX+1][2]

                        resultLIST[sentenceINDEX][foodINDEX+1][0] = None
                        try:
                            if resultLIST[sentenceINDEX][foodINDEX][1] == resultLIST[sentenceINDEX][foodINDEX+2][0]:
                                resultLIST[sentenceINDEX][foodINDEX][1] = resultLIST[sentenceINDEX][foodINDEX+2][1]
                                resultLIST[sentenceINDEX][foodINDEX][2] = resultLIST[sentenceINDEX][foodINDEX][2] + resultLIST[sentenceINDEX][foodINDEX+2][2]

                                resultLIST[sentenceINDEX][foodINDEX+2][0] = None
                        except:
                            pass
        resultLIST = [[food for food in sentence if food[0]!=None] for sentence in resultLIST]

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def _getMoney(self, ArticutResultDICT, greedyBOOL=False, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「金額」的字串
        此功能和 ArticutAPI 中的 getCurrencyLIST() 等效。
        '''
        if "result_pos" in ArticutResultDICT:
            pass
        else:
            return None
        currencyLIST = []
        for i, p in enumerate(ArticutResultDICT["result_pos"]):
            if len(p) > 1:
                currencyLIST.append([(c.start(), c.end(), c.group(0)) for c in list(self.currencyPat.finditer(p))])
                if greedyBOOL:
                    greedyLIST = []
                    try:
                        if ArticutResultDICT["result_pos"][i-1][-14:] == "</ENTITY_noun>" and ArticutResultDICT["result_pos"][i-1][-15] in "元金幣圜圓比布索鎊盾銖令朗郎":
                            greedyLIST = [(c.start(), c.end(), c.group(0)) for c in list(self.currencyGreedyGapPat.finditer(p))]
                    except:
                        pass
                    if greedyLIST:
                        greedyLIST.extend([(c.start(), c.end(), c.group(0)) for c in list(self.currencyGreedyPat.finditer(p))])
                    else:
                        greedyLIST = [(c.start(), c.end(), c.group(0)) for c in list(self.currencyGreedyPat.finditer(p))]
                    if greedyLIST:
                        currencyLIST[-1].extend(greedyLIST)
            else:
                currencyLIST.append([])
        if not indexWithPOS:
            currencyLIST = self._segIndexConverterNAIVE(ArticutResultDICT, currencyLIST)
        return currencyLIST

    def _getMSRA(self, ArticutResultDICT, msraPat, indexWithPOS=True):

        resultLIST = []
        resultAppend = resultLIST.append

        if "result_pos" in ArticutResultDICT:
            for p in ArticutResultDICT["result_pos"]:
                if len(p) > 1:
                    resultAppend([[f.start(), f.end(), self.stripPat.sub("", f.group(0))] for f in msraPat.finditer(p)])
                else:
                    resultAppend([])
            if not indexWithPOS:
                resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        elif type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend([])
                for p in x["result_pos"]:
                    if len(p) > 1:
                        resultLIST[i].append([[f.start(), f.end(), self.stripPat.sub("", f.group(0))] for f in msraPat.finditer(p)])
                    else:
                        resultLIST[i].append([])
                if not indexWithPOS:
                    resultLIST[i] = self._segIndexConverter(x, resultLIST[i])
        else:
            return None

        return resultLIST

    def mergeBulkResult(self, inputLIST):
        resultLIST = []
        resultExtend = resultLIST.extend
        for x in filter(None, inputLIST):
            try:
                if x["status"]:    # 只取成功的結果
                    resultExtend(x["result_list"])
            except:
                pass
        return resultLIST

    def getAge(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的「歲數」字串
        '''
        if self.agePat !=None:
            pass
        else:
            self.agePat = re.compile("<ENTITY_num>[^<]+?</ENTITY_num><ENTITY_noun>歲</ENTITY_noun>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.agePat, indexWithPOS)

        return resultLIST

    def getAngle(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「角度」的字串
        '''
        if self.anglePat !=None:
            pass
        else:
            self.anglePat = re.compile("(?<!燒</ACTION_verb>)(?<![溫氏]</ENTITY_nounHead>)(?<![溫氏]</ENTITY_nouny>)(?<![溫氏]</ENTITY_oov>)<ENTITY_measurement>[^<]+?[度°]</ENTITY_measurement>|<ENTITY_measurement>[^<]+?[度°]</ENTITY_measurement>(?=<ENTITY_nouny>角<)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.anglePat, indexWithPOS)

        return resultLIST

    def getArea(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「週邊地區」的字串
        '''
        if self.areaPat !=None:
            pass
        else:
            self.areaPat = re.compile("((<LOCATION>[^<]+?</LOCATION>)|(<KNOWLEDGE_addTW>[^<]+?</KNOWLEDGE_addTW>)|(<KNOWLEDGE_routeTW>[^<]+?</KNOWLEDGE_routeTW>)|(<KNOWLEDGE_place>[^<]+?</KNOWLEDGE_place>)|(<ENTITY_nounHead>[^<]+?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]+?</ENTITY_nouny>)|(<ENTITY_noun>[^<]+?</ENTITY_noun>)|(<ENTITY_oov>[^<]+?</ENTITY_oov>))(<RANGE_locality>[^<]+?</RANGE_locality>)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.areaPat, indexWithPOS)

        return resultLIST

    def getCapacity(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「容量」的字串
        '''
        if self.capacityPat !=None:
            pass
        else:
            self.capacityPat = re.compile("<ENTITY_measurement>[^<度°]+?([升勺合斗石GMBTcb]|加侖|品脫|(b[iy]tes?)|[Mm][Ll]|mol||oz)</ENTITY_measurement>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.capacityPat, indexWithPOS)

        return resultLIST

    def getDate(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「日期」的字串
        '''
        if self.datePat !=None:
            pass
        else:
            self.datePat = re.compile("(<TIME_year>[^<]+?</TIME_year>)?<TIME_month>[^<]+?</TIME_month><TIME_day>[^<]+?</TIME_day>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.datePat, indexWithPOS)

        return resultLIST

    def getDecimal(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「小數」的字串
        '''
        if self.decimalPat !=None:
            pass
        else:
            self.decimalPat = re.compile("<ENTITY_num>[^<.．點]*?[.．點][^<.．點]+?</ENTITY_num>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.decimalPat, indexWithPOS)

        return resultLIST

    def getDuration(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「時間區間」的字串
        '''
        if self.durationPat !=None:
            pass
        else:
            self.durationPat = re.compile("""(<TIME_justtime>[^<]+?</TIME_justtime>|<TIME_[^>]{3,6}>[^<]+?</TIME_[^>]{3,6}>)(<MODIFIER>一?直</MODIFIER>)?(<ACTION_verb>到</ACTION_verb>|<AUX>到</AUX>|<FUNC_inner>至</FUNC_inner>)(<TIME_justtime>[^<]+?</TIME_justtime>|<TIME_[^>]{3,6}>[^<]+?</TIME_[^>]{3,6}>)|
                                             (<TIME_justtime>[^<]+?分鐘</TIME_justtime>)|(<TIME_day>[^<星禮今明昨前後]+?天</TIME_day>)|(<TIME_week>[^<周週]+?([周週]|個星期|個禮拜)</TIME_week>)|(<TIME_month>[^<周週]+?個月</TIME_week>)|(<TIME_season>[^<]+?</TIME_season>)|(<TIME_year>[^<]+?</TIME_year>)|(<TIME_decade>[^<]+?</TIME_decade>)""", re.X)

        resultLIST = self._getMSRA(ArticutResultDICT, self.durationPat, indexWithPOS)

        return resultLIST

    def getFood(self, ArticutResultDICT, withLocation=False, indexWithPOS=True):
        resultLIST = []
        if "result_pos" in ArticutResultDICT:
            resultLIST = self._getFood(ArticutResultDICT, withLocation=withLocation, indexWithPOS=indexWithPOS)
        elif type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            resultLIST = [self._getFood(x, withLocation=withLocation, indexWithPOS=indexWithPOS) for x in ArticutResultLIST]
        else:
            return None

        return resultLIST

    def getFraction(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「分數」的字串
        '''
        if self.fractionPat !=None:
            pass
        else:
            self.fractionPat = re.compile("<ENTITY_measurement>[^<度°]+?(分之)[^<]+?</ENTITY_measurement>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.fractionPat, indexWithPOS)

        return resultLIST

    def getFrequency(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「頻率」的字串
        '''
        if self.frequencyPat !=None:
            pass
        else:
            self.frequencyPat = re.compile("(<ENTITY_measurement>[^<度°]+?((?<!馬)赫|[Hh]z)</ENTITY_measurement>)|((<QUANTIFIER>每</QUANTIFIER>)?(<TIME_justtime>[^<]+?</TIME_justtime>|<TIME_[^>]{3,6}>[^<]+?</TIME_[^>]{3,6}>))(<ENTITY_classifier>[^<]+?</ENTITY_classifier>|<ACTION_eventQuantifier>[^<]+?</ACTION_eventQuantifier>|<ENTITY_num>[^<]+?</ENTITY_num><ENTITY_nounHead>班</ENTITY_nounHead>)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.frequencyPat, indexWithPOS)

        return resultLIST

    def getInteger(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「整數」的字串
        '''
        if self.integerPat !=None:
            pass
        else:
            self.integerPat = re.compile("<ENTITY_num>[^<.．點]+?</ENTITY_num>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.integerPat, indexWithPOS)

        return resultLIST

    def getLength(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「長度」的字串
        '''
        if self.lengthPat !=None:
            pass
        else:
            self.lengthPat = re.compile("<ENTITY_measurement>[^<]+?(?<!方)(公分|光年|inch|[哩里碼吋呎尺米釐mM])</ENTITY_measurement>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.lengthPat, indexWithPOS)

        return resultLIST

    def getLocation(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「重量」的字串。
        此功能和 ArticutAPI 中的 getLoctionStemLIST() 等效。
        '''

        if self.locationPat != None:
            pass
        else:
            self.locationPat = re.compile("(?<=<LOCATION>)[^<]+?(?=</LOCATION>)|(?<=<KNOWLEDGE_addTW>)[^<]+?(?=</KNOWLEDGE_addTW>)|(?<=<KNOWLEDGE_routeTW>)[^<]+?(?=</KNOWLEDGE_routeTW>)")

        resultLIST = []
        resultAppend = resultLIST.append

        if "result_pos" in ArticutResultDICT:
            for p in ArticutResultDICT["result_pos"]:
                if len(p) > 1:
                    resultAppend([(l.start(), l.end(), l.group(0)) for l in self.locationPat.finditer(p)])
                else:
                    resultAppend([])
            if not indexWithPOS:
                resultLIST = self._segIndexConverterNAIVE(ArticutResultDICT, resultLIST)
        elif type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend([])
                for p in x["result_pos"]:
                    if len(p) > 1:
                        resultLIST[i].append([[f.start(), f.end(), self.stripPat.sub("", f.group(0))] for f in self.locationPat.finditer(p)])
                    else:
                        resultLIST[i].append([])
                if not indexWithPOS:
                    resultLIST[i] = self._segIndexConverterNAIVE(x, resultLIST[i])
        else:
            return None

        return resultLIST

    def getMeasure(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中為「測量值」的字串
        '''
        if self.measurePat !=None:
            pass
        else:
            self.measurePat = re.compile("<ENTITY_measurement>[^<]+?</ENTITY_measurement>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.measurePat, indexWithPOS)

        return resultLIST

    def getMoney(self, ArticutResultDICT, greedyBOOL=False, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「金額」的字串
        此功能和 ArticutAPI 中的 getCurrencyLIST() 等效。
        '''
        currencyLIST = []

        if "result_pos" in ArticutResultDICT:
            currencyLIST = self._getMoney(ArticutResultDICT, greedyBOOL=greedyBOOL, indexWithPOS=indexWithPOS)
        elif type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            currencyLIST = [self._getMoney(x, greedyBOOL=greedyBOOL, indexWithPOS=indexWithPOS) for x in ArticutResultLIST]
        else:
            return None

        return currencyLIST

    def getOrdinal(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「序數」的字串
        '''
        if self.ordinalPat !=None:
            pass
        else:
            self.ordinalPat = re.compile("<ENTITY_DetPhrase>第[^<]+?</ENTITY_DetPhrase>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.ordinalPat, indexWithPOS)

        return resultLIST

    def getPercent(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「百分比/千分比/萬分比」的字串
        '''
        if self.percentPat !=None:
            pass
        else:
            self.percentPat = re.compile("<ENTITY_measurement>[百千萬億兆]分之[^<]+?</ENTITY_measurement>|<ENTITY_measurement>[^<]+?[％%‰‱](左右|上下|[多餘])?</ENTITY_measurement>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.percentPat, indexWithPOS)

        return resultLIST

    def getPerson(self, ArticutResultDICT, includePronounBOOL=True, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「人名」的字串
        此功能和 ArticutAPI 中的 getPersonLIST() 等效。
        取出斷詞結果中的人名 (Person)
        若 includePronounBOOL 為 True，則連代名詞 (Pronoun) 一併回傳；若為 False，則只回傳人名。
        '''

        if self.personPat != None:
            pass
        else:
            self.personPat = re.compile("(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)")

        person_pronounPat = self.personPat

        if includePronounBOOL:
            person_pronounPat = re.compile(self.personPat.pattern+"|(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)")

        person_pronounLIST = []
        person_pronounAppend = person_pronounLIST.append

        if "result_pos" in ArticutResultDICT:
            for p in ArticutResultDICT["result_pos"]:
                if len(p)>1:
                    personLIST = [[pn.start(), pn.end(), pn.group(0)] for pn in person_pronounPat.finditer(p)]
                    person_pronounAppend(personLIST)
                else:
                    person_pronounAppend([])
            if not indexWithPOS:
                person_pronounLIST = self._segIndexConverterNAIVE(ArticutResultDICT, person_pronounLIST)

        elif type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                person_pronounAppend([])
                for p in x["result_pos"]:
                    if len(p)>1:
                        personLIST = [[pn.start(), pn.end(), pn.group(0)] for pn in person_pronounPat.finditer(p)]
                        person_pronounLIST[i].append(personLIST)
                    else:
                        person_pronounLIST[i].append([])
                if not indexWithPOS:
                    person_pronounLIST[i] = self._segIndexConverterNAIVE(x, person_pronounLIST[i])
        else:
            return None

        return person_pronounLIST

    def getRate(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「比例」的字串
        '''
        if self.ratePat !=None:
            pass
        else:
            self.ratePat = re.compile("(<ENTITY_measurement>[^<]+?倍</ENTITY_measurement>)|(<ENTITY_num>[^<]+?</ENTITY_num><ACTION_verb>比</ACTION_verb><ENTITY_num>[^<]+?</ENTITY_num>)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.ratePat, indexWithPOS)

        return resultLIST

    def getSpeed(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「速度」的字串
        '''
        if self.speedPat !=None:
            pass
        else:
            self.speedPat = re.compile("(<ENTITY_measurement>[^<]+?馬赫</ENTITY_measurement>)|(<ENTITY_nounHead>[時秒分]速</ENTITY_nounHead>|<ENTITY_nouny>[時秒分]速</ENTITY_nouny>|<ENTITY_noun>[時秒分]速</ENTITY_noun>|<ENTITY_oov>[時秒分]速</ENTITY_oov>)<ENTITY_measurement>[^<]+?(?<!方)(公分|光年|[哩里碼吋呎尺米mM])</ENTITY_measurement>|((((<QUANTIFIER>每</QUANTIFIER>)|(<MODIFIER>每秒</MODIFIER>)|(<ENTITY_num>[一1１]</ENTITY_num>))(<TIME_justtime>[^<]+?</TIME_justtime>|<TIME_[^>]{3,6}>[^<]+?</TIME_[^>]{3,6}>))<ENTITY_measurement>[^<]+?(?<!方)(公分|光年|[哩里碼吋呎尺米mM])</ENTITY_measurement>)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.speedPat, indexWithPOS)

        return resultLIST

    def getTemperature(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「溫度」的字串
        '''
        if self.temperaturePat !=None:
            pass
        else:
            self.temperaturePat = re.compile("((?<![^燒達到]</ACTION_verb>)|(?<=[溫氏]</ENTITY_nounHead>)|(?<=[溫氏]</ENTITY_nouny>)|(?<=[溫氏]</ENTITY_oov>))<ENTITY_measurement>[^<]+?[度℃℉]</ENTITY_measurement>")

        resultLIST = self._getMSRA(ArticutResultDICT, self.temperaturePat, indexWithPOS)

        return resultLIST

    def getTime(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「時間」的字串
        '''
        if self.timePat !=None:
            pass
        else:
            self.timePat = re.compile("(<TIME_justtime>[^<]+?</TIME_justtime>|<TIME_[^>]{3,6}>[^<]+?</TIME_[^>]{3,6}>)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.timePat, indexWithPOS)

        return resultLIST

    def getWeight(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「重量」的字串
        '''
        if self.weightPat !=None:
            pass
        else:
            self.weightPat = re.compile("(<ENTITY_measurement>[^<]+?([克斤噸頓磅兩錢]|[Kk]g|KG|盎斯)</ENTITY_measurement>)")

        resultLIST = self._getMSRA(ArticutResultDICT, self.weightPat, indexWithPOS)

        return resultLIST

    def getWWW(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的描述「URL 連結」的字串
        '''
        if self.wwwPat !=None:
            pass
        else:
            self.wwwPat = re.compile("<KNOWLEDGE_url>.+?(</KNOWLEDGE_url>){1}")

        resultLIST = self._getMSRA(ArticutResultDICT, self.wwwPat, indexWithPOS)

        return resultLIST


if __name__ == "__main__":
    from pprint import pprint

    gNER = GenericNER()

    testLIST = [{"result_list": [{"result_pos": ["<TIME_day>今晚</TIME_day><ACTION_verb>來</ACTION_verb><ACTION_verb>點</ACTION_verb><ENTITY_classifier>一道</ENTITY_classifier><ENTITY_nouny>法式</ENTITY_nouny><ACTION_verb>焗烤</ACTION_verb><ENTITY_nouny>龍蝦</ENTITY_nouny>"]},
                                 {"result_pos": ["<ENTITY_noun>藥燉</ENTITY_noun><ENTITY_noun>排骨</ENTITY_noun><ACTION_verb>加</ACTION_verb><ENTITY_noun>藥燉</ENTITY_noun><ENTITY_noun>土虱</ENTITY_noun>", "，", "<ENTITY_nouny>花生卷</ENTITY_nouny><ACTION_verb>加</ACTION_verb><ENTITY_noun>冰淇淋</ENTITY_noun>"]},
                                 {"result_pos": ['<TIME_year>今年</TIME_year><ENTITY_num>十</ENTITY_num><ENTITY_noun>歲</ENTITY_noun><FUNC_inner>的</FUNC_inner><ENTITY_person>彼德</ENTITY_person><ACTION_verb>有</ACTION_verb><ENTITY_classifier>一個</ENTITY_classifier><ENTITY_num>八</ENTITY_num><ENTITY_noun>歲</ENTITY_noun><FUNC_inner>的</FUNC_inner><ENTITY_pronoun>弟弟</ENTITY_pronoun><FUNC_conjunction>和</FUNC_conjunction><ENTITY_classifier>一個</ENTITY_classifier><ENTITY_num>十四</ENTITY_num><ENTITY_noun>歲</ENTITY_noun><FUNC_inner>的</FUNC_inner><ENTITY_pronoun>姐姐</ENTITY_pronoun>',
                                                 '，',
                                                 '<ENTITY_nouny>測試人</ENTITY_nouny><ENTITY_nounHead>名</ENTITY_nounHead><ENTITY_person>蔡英文</ENTITY_person><FUNC_conjunction>與</FUNC_conjunction><ENTITY_nouny>陳</ENTITY_nouny><FUNC_inner>時</FUNC_inner><LOCATION>中共</LOCATION><MODIFIER>同</MODIFIER><ACTION_verb>參與</ACTION_verb><ENTITY_nouny>會議</ENTITY_nouny>']},
                                 {'result_pos': ['<ENTITY_oov>容量</ENTITY_oov><ENTITY_measurement>1公升</ENTITY_measurement><FUNC_inner>的</FUNC_inner><ENTITY_nouny>牛奶紙盒</ENTITY_nouny><RANGE_locality>裡</RANGE_locality><MODIFIER>只</MODIFIER><MODAL>能</MODAL><ACTION_verb>裝</ACTION_verb>',
                                                 ' ',
                                                 '<ENTITY_measurement>995.5毫升</ENTITY_measurement><FUNC_inner>的</FUNC_inner><ENTITY_nouny>水</ENTITY_nouny>']}],
                 "status": True}]
    resultLIST = gNER.getFood(testLIST, indexWithPOS=False)
    pprint(resultLIST)

    #foodTestDICT = {"result_pos":["<ENTITY_noun>藥燉</ENTITY_noun><ENTITY_noun>排骨</ENTITY_noun><ACTION_verb>加</ACTION_verb><ENTITY_noun>藥燉</ENTITY_noun><ENTITY_noun>土虱</ENTITY_noun>", "，", "<ENTITY_nouny>花生卷</ENTITY_nouny><ACTION_verb>加</ACTION_verb><ENTITY_noun>冰淇淋</ENTITY_noun>"]}
    #foodLIST = gNER.getFood(foodTestDICT, withLocation=True)
    #print(foodLIST)

    #foodTestDICT = {"result_pos": ["<TIME_day>今晚</TIME_day><ACTION_verb>來</ACTION_verb><ACTION_verb>點</ACTION_verb><ENTITY_classifier>一道</ENTITY_classifier><ENTITY_nouny>法式</ENTITY_nouny><ACTION_verb>焗烤</ACTION_verb><ENTITY_nouny>龍蝦</ENTITY_nouny>"]}
    #foodLIST = gNER.getFood(foodTestDICT, withLocation=True)
    #print(foodLIST)



    #ageTestDICT = {"result_pos":["<ENTITY_num>六</ENTITY_num><ENTITY_noun>歲</ENTITY_noun>"]}
    #ageLIST = gNER.getAge(ageTestDICT, False)
    #print(ageLIST)