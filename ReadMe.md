# ArticutAPI (文截斷詞)

### [Articut API Website](https://api.droidtown.co/)
### [Document](https://api.droidtown.co/document/)
### [![Articut Demo](https://img.youtube.com/vi/AnvdKmVLlcA/0.jpg)](https://youtu.be/AnvdKmVLlcA "Articut Demo")

----------------------

## 使用方法
### Articut CWS (Chinese word segmentation)
```
from ArticutAPI import Articut

inputSTR = "會被大家盯上，才證明你有實力。"
articut = Articut()

result = articut.parse(inputSTR)
print("articut.parse()\n", result)
```
### 回傳結果
```
articut.parse()
{'exec_time': 0.06723856925964355,
 'level': 'lv2',
 'msg': 'Success!',
 
 'result_pos': ['<MODAL>會</MODAL><ACTION_lightVerb>被</ACTION_lightVerb><ENTITY_nouny>大家</ENTITY_nouny><ACTION_verb>盯上</ACTION_verb>',
                '，',
                '<MODAL>才</MODAL><ACTION_verb>證明</ACTION_verb><ENTITY_pronoun>你</ENTITY_pronoun><ACTION_verb>有</ACTION_verb><ENTITY_noun>實力</ENTITY_noun>',
                '。'],
 'result_segmentation': '會/被/大家/盯上/，/才/證明/你/有/實力/。/',
 'status': True,
 'version': 'v118',
 'word_count_balance': 9985,
 'product': 'https://api.droidtown.co/product/',
 'document': 'https://api.droidtown.co/document/'
}
```

### 取得 Articut 版本列表
```
from ArticutAPI import Articut

articut = Articut()

result = articut.versions()
print("articut.versions()\n", result)
```
### 回傳結果
```
articut.versions()
{'msg': 'Success!',
 'status': True,
 'versions': [{'level': ['lv1', 'lv2'],
               'release_date': '2019-04-25',
               'version': 'latest'},
              {'level': ['lv1', 'lv2'],
               'release_date': '2019-04-25',
               'version': 'v118'},
              {'level': ['lv1', 'lv2'],
               'release_date': '2019-04-24',
               'version': 'v117'},...
}
```

----------------------

## 進階用法
### Articut Level (預設: lv2)
```
from pprint import pprint

inputSTR = "小紅帽"
articut = Articut()

result = articut.parse(inputSTR, level="lv1")
print(result)
```
### 回傳結果 lv1 
極致斷詞，適合 NLU 或機器自動翻譯使用。呈現結果將句子中的每個元素都儘量細分出來。
```
{'exec_time': 0.04814624786376953,
 'level': 'lv1',
 'msg': 'Success!',
 'result_pos': ['<MODIFIER>小</MODIFIER><MODIFIER_color>紅</MODIFIER_color><ENTITY_nounHead>帽</ENTITY_nounHead>'],
 'result_segmentation': '小/紅/帽/',
 'status': True,
 'version': 'v118',
 'word_count_balance': 9997,...}
```

### 回傳結果 lv2 
詞組斷詞，適合文本分析、特徵值計算、關鍵字擷取…等應用。呈現結果將以具意義的最小單位呈現。
```
{'exec_time': 0.04195523262023926,
 'level': 'lv2',
 'msg': 'Success!',
 'result_pos': ['<ENTITY_nouny>小紅帽</ENTITY_nouny>'],
 'result_segmentation': '小紅帽/',
 'status': True,
 'version': 'v118',
 'word_count_balance': 9997,...}
```
