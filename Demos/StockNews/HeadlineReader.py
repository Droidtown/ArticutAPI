#!/usr/bin/env python3
# -*- coding:utf-8 -*-

try:
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut
except:
    from ArticutAPI import Articut
from pprint import pprint
import json

if __name__ == "__main__":

    try:
        #使用自己的斷詞額度。
        with open("../../account.info", "r") as f:
            userDICT = json.loads(f.read())
        username = userDICT["email"]
        apikey = userDICT["apikey"]
        atc = Articut(username=userDICT["email"], apikey=userDICT["apikey"])
    except:
        #使用公用的斷詞額度。(每小時 2000 字)
        atc = Articut()

downSample = '''台指選擇權盤後－年線保衛戰失利 外資續賣台股
台股期權盤後－華為拖累電子 台股摔破支撐
華為風暴持續擴大 三王領跌重挫148點 創波段新低
華為風暴 大跌退守10300點
美商禁令聲聲催，台股電子三王大跌，指數再破年線
跌148.85點
華為風暴擴大 一度破10300點
外資狂撤，台股欲振乏力
利空燒不盡，台股挫百點失年線
華為風暴！台股摜破前低，將往半年線測試
電子股恐慌殺盤出籠，可成慘破200元大關
貿易戰演變成科技戰 電子權值股成壓力蓋
華為風暴嚇趴！台積電狂殺3％，台股重挫逾140點
台股開盤10404點，跌53.22點
續跌危機未除 恐尋求半年線支撐
美中貿易戰延燒 牽動台股後市
不要亂猜底，小心被連環套
電子雙王獨撐 台股上檔遇壓收黑小跌（
年線持續下彎 台股技術面仍看空
新台幣貶不停 外資猛落跑 小心年線岌岌可危
中華電不賣華為新機；新台幣貶破31.5元
美擬封殺海康，安控股飆；聯茂、華通5G題材發酵
晶片事業重傷！安謀加入封殺華為
22日自營商、外資賣超4.32億元、111.21億元
外資賣壓不止，台股走勢偏空
上遇年線壓力 台股量縮整理
台股欲振乏力，三大法人賣超107.39億元
5/22集中市場三大法人合計賣超107.40億元
台積電獨木難撐，台股隨陸股衰尾
台積電帶著大立光小反彈 無助大盤光彩反攻
美國接連對中國出招，台股追價力不強，量縮收黑
短線反彈後，恐再下殺
今年高點已過
上市櫃企業Q1獲利年減近2成，4公司財報續難產
宏達電Q3營收 估衰退27～35%'''

riseSample = '''KD低檔黃金交叉，有利戰季線
台股量縮回穩，反彈契機不遠
台積賣超停止日，台股止跌時
台商回台投資將達5,500億，千載難逢的機會
貿易談判空窗，台股有望醞釀反彈
台積電強漲 大盤一度突破10500點
台積回神，反攻10500點
美給華為寬限期90天，台系華為供應鏈鬆口氣
台股開盤10481.1點，漲16.6點
金融傳產發威 台股破低後強彈收復年線
澳洲央行6月考慮降息；新興市場短空長多
上季GDP成長3.11% 全年有機會2.42%
毛利率攀升 聯發科Q3每股賺3.26元
聯亞Q3營收季增5成 矽光訂單看到明年2月
台達電工業自動化收成 電動車起飛
半月來新高 台幣升3.5分
神達車聯網收割 獲美政府車隊訂單
今年製造業景氣 上修至黃藍燈
蘋果iPhone 8明年推出 上看1.5億支
第四季SSD價漲10% 創見、威剛利多
華航聯手漢翔、空巴 搶A350維修商機
昇恆昌預購網站 年底業績衝億元
電源步入旺季 台達電、群電營收獲利增
觀光帶動成長 Q2 GDP3.84%
台股強彈 大漲214點
華映Q2虧轉盈 下半年挑戰百億
BDI逼近新高 散裝航運股紅通通
台股反彈 挑戰萬點動能仍強
全球生技類股 行情飆漲
晶華 今年EPS可望破4元
製藥一軍亮麗 百略獲利增近倍
掌握關鍵零組件 三星迅速崛起
外資券商加持 LED亮晶晶
月線連四紅 台股看好上萬點
11月份基金表現亞股滿堂彩
亞泰影像擴產後銷售動能強 Q2單季營收將超越去年同期'''

def signalMaker():
    #建議可以將做完的漲跌訊號 (downSignal/riseSignal) 另行儲存，
    #這麼一來，只要 downSample/riseSample 沒有更新，就不需要每次都要重新計算。

    downSignal = []
    riseSignal = []

    result = atc.parse(downSample, level="lv2")
    #確認仍有字數可使用
    if result["status"] == False:
        print(result["msg"])
        return None
    else:
        #將下跌新聞的標題中，每一則動詞收集起來，做為 downSignal 的下跌訊號。
        verbLIST = atc.getVerbStemLIST(result)
        for v in verbLIST:
            if len(v) == 0:
                pass
            else:
                for i in v:
                    if "negation" in result["result_pos"][0][i[0]-22:i[0]]: #再檢查動詞前是否為「否定」表示。e.g., 不/看好。那麼「看好」應該被歸類到 riseSignal。
                        riseSignal.append(i[-1])
                    else:
                        downSignal.append(i[-1])
        downSignal = set(downSignal)


    result = atc.parse(riseSample, level="lv2")
    if result["status"] == False:
        print(result["msg"])
        return None
    else:
        #將下跌新聞的標題中，每一則動詞收集起來，做為 riseSignal 的上漲訊號。
        verbLIST = atc.getVerbStemLIST(result)
        for v in verbLIST:
            if len(v) == 0:
                pass
            else:
                for i in v:
                    if "negation" in result["result_pos"][0][i[0]-22:i[0]]: #再檢查動詞前是否為「否定」表示。e.g., 不會/下跌。那麼「下跌」應該被歸類到 downSignal。
                        downSignal.append(i[-1])
                    else:
                        riseSignal.append(i[-1])
        riseSignal = set(riseSignal)

        #把 downSignal 和 riseSignal 中重覆的動詞清除。它可能是「中性」或是無關漲跌的動詞。
        downSignal = downSignal - riseSignal.intersection(downSignal)
        riseSignal = riseSignal - riseSignal.intersection(downSignal)
    return (downSignal, riseSignal)

if __name__== "__main__":
    downSignal, riseSignal = signalMaker()
    if None in (downSignal, riseSignal):
        print("Cannot proceed!")
    else:
        testSTR = "產業供應鏈分散效應看好東協布局" #測試用句。注意到這一句並沒有在前述學習的 downSample/riseSample 中。
        testResult = atc.parse(testSTR, level="lv2")
        testVerbLIST = atc.getVerbStemLIST(testResult)
        resultLIST = []
        for tv in testVerbLIST:
            if len(tv) == 0:
                pass
            else:
                for v in tv:
                    if v[-1] in downSignal:
                        if "negation" in testResult["result_pos"][0][v[0]-22:v[0]]: #確認是否有「否定詞」出現在 downSignal 中。如果有的話，那就是上漲囉！
                            resultLIST.append("這句新聞標題…應該是看漲↗")
                        else:
                            resultLIST.append("這句新聞標題…應該是看跌↘")
                    elif v[-1] in riseSignal:
                        if "negation" in testResult["result_pos"][0][v[0]-22:v[0]]: #確認是否有「否定詞」出現在 riseSignal 中。如果有的話，那就是下跌囉！
                            resultLIST.append("這句新聞標題…應該是看跌↘")
                        else:
                            resultLIST.append("這句新聞標題…應該是看漲↗")
                    else:
                        pass
        resultSET = set(resultLIST)
        if len(resultSET) == 1:
            print(list(resultSET)[0])
        else:
            print("這句新聞標題…應該是看跌↘")