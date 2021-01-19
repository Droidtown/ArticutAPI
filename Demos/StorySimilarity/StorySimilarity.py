#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from Bio import pairwise2
#from Bio.pairwise2 import format_alignment

try:
    import sys
    sys.path.append("../..")
    from articutapi.ArticutAPI import Articut
except:
    from articutapi.ArticutAPI import Articut

username = ""
apikey = ""

articut = Articut(username=username, apikey=apikey)


def verbListExtraction(inputSTR):
    resultDICT = articut.parse(inputSTR) #呼叫 Articut 進行斷詞/POS/NER 處理
    verbLIST = articut.getVerbStemLIST(resultDICT) #取出每一句的動詞
    resultLIST = []
    for s in verbLIST:  #將每一句的動詞分別取出，略過標點符號
        if len(s) == 1:
            pass
        else:
            for v in s:
                resultLIST.append(v[-1])
    return ",".join(resultLIST) #將動詞列表黏合成單一字串後回傳


if __name__ == "__main__":
    text01 = """鑰匙不見了，進不了門，只好找人家來開鎖囉!
    好不容易等到鎖匠來了。可是來的人 是一位老人家。這個人年紀真的很大了。我就開玩笑的問:師傅，您年紀這麼大了，還這麼辛苦出來工作呀!你開鎖還行嗎?老人家聽到我這麼說，很不開心。
    他說：小伙子呀!這對我來說是小事一樁，我當年可是專門開保險箱的。
    我說:真的假的？還真是看不出來。
    師傅:我可是有兩把刷子的，不然怎麼會到去年才放我出來"""

    text02 = """那天鑰匙掉了，沒辦法進門，只好找人來開鎖。
    來的是一位老人家，年紀真的老大了。我開玩笑的問：師傅，您年紀這麼大了，開鎖還行嗎？老人家聽我這麼說不開心了。
    他說：我年輕時，可是專門開保險櫃的。
    我：真的假的？
    老人家：當然是真的！不然怎會到去年才放我出來"""

    text03 = """首先，銀行信用資源應該合理配置，不要過度流向不動產放款，避免銀行授信間接助長炒房、炒地，導致房價不合理上漲。
    央行指出，今年以來，銀行購置住宅貸款及建築貸款年增率快速上升，9 月底全體銀行不動產貸款占總放款比重為 35.8%，接近歷史高點之 37.9%。加上銀行辦理投資客購屋貸款，部分案件貸款成數偏高、貸款利率偏低、寬限期過長，餘屋貸款案件也有授信條件過於寬鬆的現象。央行認為，這些案件可能助長借款人進行高度財務槓桿操作，導致房價不合理上漲。
    第二，銀行應對借款人充分揭露貸款負擔資訊，並提醒對方留意財務規劃。像是首購族群購屋貸款條件，如高貸款成數、長天期貸款年限或較長寬限期等，都要清楚揭露相關貸款資訊，以維護借款人權益。
    第三，銀行應該善盡企業社會責任，引導資金投入實質投資，有助提高就業，增加國人所得。"""

    text04 = """一、銀行信用資源宜合理配置，勿過度流向不動產放款，避免銀行授信間接助長炒房、炒地，導致房價不合理上漲。
    二、銀行應對借款人充分揭露貸款負擔資訊，並提醒其注意財務規劃。
    三、銀行應善盡企業社會責任，引導資金投入實質投資，有助提高就業，增加國人所得。"""

    text05 = """央行籲銀行信用資源宜合理配置，勿過度流向不動產放款，避免銀行授信間接助長炒房、炒地，導致房價不合理上漲。
    央行說明，銀行辦理投資客購屋貸款，部分案件有貸款成數偏高、貸款利率偏低，及寬限期過長等現象，購地貸款案件，也有未確實規範其動工興建時程，借款人利用銀行資金進行養地、囤地之實，另餘屋貸款案件亦有授信條件過於寬鬆等現象。上述案件可能助長借款人進行高度財務槓桿操作，以致房價不合理上漲，不利房市健全發展及影響整體資源之合理配置。
    銀行應對借款人充分揭露貸款負擔資訊，並提醒其注意財務規劃，央行指出，對於首購族群購屋貸款條件，如高貸款成數、長天期貸款年限或較長寬限期等，務必清楚揭露相關貸款資訊，包括寬限期屆滿後每期還款金額變動、不同貸款年限須支付本息總額等資訊，以維護借款人權益，並有助其儘早辦理財務規劃。
    銀行應善盡企業社會責任，引導資金投入實質投資，有助提高就業，增加國人所得，央行強調，近年本國銀行對企業放款成長率不及購置住宅貸款成長率，但銀行資金多來自社會大眾存款，基於其掌握社會寶貴資源，業務經營除考量利潤外，也要善盡企業社會責任，勿使社會資源助長投資炒房、推升房價不合理上漲，以符社會大眾對銀行金融中介角色之期待。"""

    verbSeq01 = verbListExtraction(text01)  #將 text01 送入剛才的步驟處理，得到它的動詞序列
    verbSeq02 = verbListExtraction(text02)  #將 text02 送入剛才的步驟處理，得到它的動詞序列

    alignments = pairwise2.align.globalxx(verbSeq01, verbSeq02) #利用 biopython 比較兩個動詞序列

    baseLength = max((len(verbSeq01), len(verbSeq02)))/2 #計算兩個句子的比較分母。
    if alignments[0].score >= baseLength:
        baseLength = max((len(verbSeq01), len(verbSeq02)))

    print('兩文本的相似度：{}%'.format(round(alignments[0].score/baseLength*100,3))) #最後輸出兩文本的相似度