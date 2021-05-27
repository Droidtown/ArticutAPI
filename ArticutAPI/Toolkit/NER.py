#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

class GenericNER:
    def __init__(self, locale=None):
        self.mainDishSTR = "([乳包味啡嗲奶心手排果柳棗椒油湯漿炒焿煎煙燒爐瓜皮盅盤米粄粉粑粥粽粿糊糍粑糕糖糬糰線羹翅翼肉肚肺肝膽腐腦腩腳腸胃腿胗芛薏花茄茶草莓菊菜蓮蔗蔥薑蒜薩薯蘆蕉蜜筍檳豆豉栗菇虱蚵蛋卵蝦蟹螺貝蟳血角酒酥醬趖銼鍋雜頭飩飯飴餃飩餅麵餐骨鬆鬚魚鯧鰻鮪鮭魽鯛鰾鱉龜雞鴨鵝牛豬羊兔鼠鴿豚鷄堡]|"
        self.sideDishSTR = "[丸冰圓塊卷捲粄條扒仔乾]|[俄德法美日義英西歐中台泰越韓粵港]式|星州|客家|花枝|鴛鴦|石斑|黑輪|伯勞|藥燉|愛玉|珍珠|熱狗|阿給|燒賣|料理|飲料|糖[水醋]|鳳梨|蜜餞|花生|[壽土吐]司|便當|飯盒|鍋貼|扁食|雲吞|刺身|山蘇|多士|咖哩|沙拉|沙母|沙公|海參|鴨賞|旗魚|燒賣|海鮮|河鮮|龍珠|鮟鱇|牛河|熊掌|糕渣|自助餐|沙威[馬瑪]|三明治|沙淇瑪|原住民|棺材板|官財板|地瓜球|綠豆椪|冰淇淋|佛跳牆|[洋和][菓果]子)"
        self.cookMethodSTR = "[煎煮炒炸蒸煨魯滷漬醃炊爆燒拌剝湯焢焗烘烤佐釀]"
        self.cookModSTR = "([麻辣酸清]|酥[脆炸]|[蔥薑蒜]爆|[干乾紅]燒){1,2}"
        self.extenedLIST = [("串燒", "(<ACTION_verb>串燒</ACTION_verb>)"),
                            ("烤肉", "(<ACTION_verb>烤肉</ACTION_verb>)"),
                            ("切雞", "(<VerbP>切雞</VerbP>)"),
                            ("炒蛋", "(<VerbP>炒蛋</VerbP>)"),
                            ("煎蛋", "(<VerbP>煎蛋</VerbP>)"),
                            ("烘蛋", "(<VerbP>烘蛋</VerbP>)"),
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
        self.escapeTUPLE = ("原住民", "客家", "俄式", "德式", "法式", "美式", "日式", "義式", "英式", "西式", "歐式", "中式", "台式", "泰式", "越式", "韓式", "粵式", "港式", "星州", "大塊", "味")

        self.foodPat = re.compile("{0}|(<ACTION_verb>[^<]*?{1}+?[^<]*?</ACTION_verb>)?(<MODIFIER>{2}</MODIFIER>)?(<KNOWLEDGE_chemical>酸</KNOWLEDGE_chemical>)?(<MODIFIER_color>[黑紅]</MODIFIER_color>)?(<ENTITY_classifier>三杯</ENTITY_classifier>)?((<ENTITY_nounHead>[^<]*?{3}+[^<]*?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]*?{3}+[^<]*?</ENTITY_nouny>)|(<ENTITY_noun>[^<]*?{3}+[^<]*?</ENTITY_noun>)|(<ENTITY_oov>[^<]*?{3}+[^<]*?</ENTITY_oov>))".format("|".join([p[1] for p in self.extenedLIST]), self.cookMethodSTR, self.cookModSTR, self.mainDishSTR+self.sideDishSTR))
        self.foodPatWLoc = re.compile(r"""{0}|
        (<LOCATION>[^<]+?</LOCATION>)?
        ((<ENTITY_nounHead>[^<]*?({1})+[^<]*?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]*?({1})+[^<]*?</ENTITY_nouny>)|(<ENTITY_noun>[^<]*?({1})+[^<]*?</ENTITY_noun>)|(<ENTITY_oov>[^<]*?({1})+[^<]*?</ENTITY_oov>))?
        (<ACTION_verb>[^<]*?{2}+?[^<]*?</ACTION_verb>)?
        (<MODIFIER>{3}</MODIFIER>)?
        (<KNOWLEDGE_chemical>酸</KNOWLEDGE_chemical>)?
        (<MODIFIER_color>[黑紅]</MODIFIER_color>)?
        (<ENTITY_classifier>三杯</ENTITY_classifier>)?
        ((<ENTITY_nounHead>[^<]*?{4}+[^<]*?</ENTITY_nounHead>)|(<ENTITY_nouny>[^<]*?{4}+[^<]*?</ENTITY_nouny>)|(<ENTITY_noun>[^<]*?{4}+[^<]*?</ENTITY_noun>)|(<ENTITY_oov>[^<]*?{4}+[^<]*?</ENTITY_oov>))""".format("|".join([p[1] for p in self.extenedLIST]),
                                                                                                                                                                                                            "|".join(self.escapeTUPLE[:-2]),
                                                                                                                                                                                                            self.cookMethodSTR,
                                                                                                                                                                                                            self.cookModSTR,
                                                                                                                                                                                                            self.mainDishSTR+self.sideDishSTR), re.X)

        self.agePat     = None
        self.measurePat =None

        self.stripPat = re.compile("</?[A-Za-z]+?_?[A-Za-z]*?>")

    def _segIndexConverter(self, ArticutResultDICT, posIndexLIST):
        '''
        Convert posIndex to segIndex
        Return list
        '''
        if type(posIndexLIST) is list and "result_pos" in ArticutResultDICT:
            pass
        else:
            return None
        try:
            for sentenceINDEX in range(0, len(ArticutResultDICT["result_pos"])):
                if len(ArticutResultDICT["result_pos"][sentenceINDEX]) == 1: #略過標點符號
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

    def getFood(self, ArticutResultDICT, withLocation=False, indexWithPOS=True):
        if "result_pos" in ArticutResultDICT:
            pass
        else:
            return None

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

    def getAGE(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的「歲數」字串
        '''
        if self.agePat !=None:
            pass
        else:
            self.agePat = re.compile("<ENTITY_num>[^<]+?</ENTITY_num><ENTITY_noun>歲</ENTITY_noun>")

        if "result_pos" in ArticutResultDICT:
            pass
        else:
            return None

        resultLIST = []
        for p in ArticutResultDICT["result_pos"]:
            if len(p) > 1:
                resultLIST.append([[f.start(), f.end(), self.stripPat.sub("", f.group(0))] for f in list(self.agePat.finditer(p)) if self.stripPat.sub("", f.group(0)) not in self.escapeTUPLE])
            else:
                resultLIST.append([])
        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getMEASURE(self, ArticutResultDICT, indexWithPOS=True):
        '''
        依 MSRA (微軟亞洲研究院, Microsoft Research Lab Asia) NER 標準取出文本中的「測量值」字串
        '''
        if self.measurePat !=None:
            pass
        else:
            self.measurePat = re.compile("<ENTITY_measurement>[^<]+?</ENTITY_measurement>")

        if "result_pos" in ArticutResultDICT:
            pass
        else:
            return None



if __name__ == "__main__":
    gNER = GenericNER()

    foodTestDICT = {"result_pos":["<ENTITY_noun>藥燉</ENTITY_noun><ENTITY_noun>土虱</ENTITY_noun><ACTION_verb>加</ACTION_verb><ENTITY_noun>藥燉</ENTITY_noun><ENTITY_noun>土虱</ENTITY_noun>", "，", "<ENTITY_nouny>花生卷</ENTITY_nouny><ACTION_verb>加</ACTION_verb><ENTITY_noun>冰淇淋</ENTITY_noun>"]}
    foodLIST = gNER.getFood(foodTestDICT, withLocation=True)
    print(foodLIST)

    foodTestDICT = {'result_pos': ['<TIME_day>今晚</TIME_day><ACTION_verb>來</ACTION_verb><ACTION_verb>點</ACTION_verb><ENTITY_classifier>一道</ENTITY_classifier><ENTITY_nouny>法式</ENTITY_nouny><ACTION_verb>焗烤</ACTION_verb><ENTITY_nouny>龍蝦</ENTITY_nouny>']}
    foodLIST = gNER.getFood(foodTestDICT, withLocation=True)
    print(foodLIST)

    ageTestDICT = {"result_pos":["<ENTITY_num>六</ENTITY_num><ENTITY_noun>歲</ENTITY_noun>"]}
    ageLIST = gNER.getAGE(ageTestDICT)
    print(ageLIST)