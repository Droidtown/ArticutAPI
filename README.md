# Articut 中文斷詞暨詞性標記服務
## [依語法結構計算，而非統計方法的中文斷詞。]

### [Articut API Website](https://api.droidtown.co/)
### [Document](https://api.droidtown.co/ArticutAPI/document/)
### [![Articut Demo](https://img.youtube.com/vi/AnvdKmVLlcA/0.jpg)](https://youtu.be/AnvdKmVLlcA "Articut Demo")

## Benchmark
### 設計目標
名稱        | ArticutAPI          | MP_ArticutAPI   | WS_ArticutAPI | 
:----------:|:-------------------:|:-------------------:|:------------------:|
產品        | Online / Docker  | Docker                | Docker              |
技術        | HTTP Request    | MultiProcessing | WebSocket        |
特色        | 簡單易用             | 批次處理             | 即時處理            |
適用情景 | 任何                    | 文本分析             | 聊天機器人         |

### 處理速度
名稱         | ArticutAPI | MP_ArticutAPI | WS_ArticutAPI | 
:----------:|-------------:|-------------------:|-------------------:|
時間         |  0.1252 秒 |         0.1206 秒 |          0.0677 秒 |

### 大量文本
句數         | ArticutAPI  | MP_ArticutAPI | WS_ArticutAPI |
:----------:|--------------:|-------------------:|------------------:|
方法        |        parse() |  bulk_parse(20) |              parse() |
1K           |        155 秒 |                   8 秒 |                18 秒 |
2K           |        306 秒 |                 14 秒 |                35 秒 |
3K           |        455 秒 |                 17 秒 |                43 秒 |

- 測試平台爲 4 核心 CPU 並使用 4 個 Process。
- `MP_ArticutAPI`使用 bulk_parse(bulkSize=20) 方法。
- `WS_ArticutAPI`使用 parse() 方法。

----------------------

# ArticutAPI

## 安裝方法
```sh
pip3 install ArticutAPI
```

## 說明文件
函數說明請參閱 Docs/index.html

## 使用方法
### Articut CWS (Chinese word segmentation)
```
from ArticutAPI import Articut
from pprint import pprint
username = "" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
apikey   = "" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。
articut = Articut(username, apikey)
inputSTR = "會被大家盯上，才證明你有實力。"
resultDICT = articut.parse(inputSTR)
pprint(resultDICT)
```
### 回傳結果
```
{"exec_time": 0.06723856925964355,
 "level": "lv2",
 "msg": "Success!",
 
 "result_pos": ["<MODAL>會</MODAL><ACTION_lightVerb>被</ACTION_lightVerb><ENTITY_nouny>大家</ENTITY_nouny><ACTION_verb>盯上</ACTION_verb>",
                "，",
                "<MODAL>才</MODAL><ACTION_verb>證明</ACTION_verb><ENTITY_pronoun>你</ENTITY_pronoun><ACTION_verb>有</ACTION_verb><ENTITY_noun>實力</ENTITY_noun>",
                "。"],
 "result_segmentation": "會/被/大家/盯上/，/才/證明/你/有/實力/。/",
 "status": True,
 "version": "v118",
 "word_count_balance": 9985,
 "product": "https://api.droidtown.co/product/",
 "document": "https://api.droidtown.co/document/"
}
```

### 列出斷詞結果所有詞性標記的內容詞 ###
可以依需求找出「名詞」、「動詞」或是「形容詞」…等詞彙語意本身已經完整的詞彙。
```
inputSTR = "你計劃過地球人類補完計劃"
resultDICT = articut.parse(inputSTR, level="lv1")
pprint(resultDICT["result_pos"])

#列出所有的 content word.
contentWordLIST = articut.getContentWordLIST(resultDICT)
pprint(contentWordLIST)

#列出所有的 verb word. (動詞)
verbStemLIST = articut.getVerbStemLIST(resultDICT)
pprint(verbStemLIST)

#列出所有的 noun word. (名詞)
nounStemLIST = articut.getNounStemLIST(resultDICT)
pprint(nounStemLIST)

#列出所有的 location word. (地方名稱)
locationStemLIST = articut.getLocationStemLIST(resultDICT)
pprint(locationStemLIST)
```

### 回傳結果 ###
```
#resultDICT["result_pos"]
["<ENTITY_pronoun>你</ENTITY_pronoun><ACTION_verb>計劃</ACTION_verb><ASPECT>過</ASPECT><LOCATION>地球</LOCATION><ENTITY_oov>人類</ENTITY_oov><ACTION_verb>補完</ACTION_verb><ENTITY_nounHead>計劃</ENTITY_nounHead>"]

#列出所有的 content word.
[[(177, 179, "計劃"), (144, 145, "補"), (116, 118, "人類"), (47, 49, "計劃")]]

#列出所有的 verb word. (動詞)
[[(144, 146, "補完"), (47, 49, "計劃")]]

#列出所有的 noun word. (名詞)
[[(177, 179, "計劃"), (116, 118, "人類")]]

#列出所有的 location word. (地方名稱)
[[(91, 93, "地球")]]
```

### 取得 Articut 版本列表
```
resultDICT = articut.versions()
pprint(resultDICT)
```
### 回傳結果
```
{"msg": "Success!",
 "status": True,
 "versions": [{"level": ["lv1", "lv2"],
               "release_date": "2019-04-25",
               "version": "latest"},
              {"level": ["lv1", "lv2"],
               "release_date": "2019-04-25",
               "version": "v118"},
              {"level": ["lv1", "lv2"],
               "release_date": "2019-04-24",
               "version": "v117"},...
}
```

----------------------

## 進階用法
### 進階用法01 >> Articut Level :斷詞的深度。數字愈小，切得愈細 (預設: lv2)。
```
inputSTR = "小紅帽"
resultDICT = articut.parse(inputSTR, level="lv1")
pprint(resultDICT)
```
### 回傳結果 lv1 
極致斷詞，適合 NLU 或機器自動翻譯使用。呈現結果將句子中的每個元素都儘量細分出來。
```
{"exec_time": 0.04814624786376953,
 "level": "lv1",
 "msg": "Success!",
 "result_pos": ["<MODIFIER>小</MODIFIER><MODIFIER_color>紅</MODIFIER_color><ENTITY_nounHead>帽</ENTITY_nounHead>"],
 "result_segmentation": "小/紅/帽/",
 "status": True,
 "version": "v118",
 "word_count_balance": 9997,...}
```

### 回傳結果 lv2 
詞組斷詞，適合文本分析、特徵值計算、關鍵字擷取…等應用。呈現結果將以具意義的最小單位呈現。
```
{"exec_time": 0.04195523262023926,
 "level": "lv2",
 "msg": "Success!",
 "result_pos": ["<ENTITY_nouny>小紅帽</ENTITY_nouny>"],
 "result_segmentation": "小紅帽/",
 "status": True,
 "version": "v118",
 "word_count_balance": 9997,...}
```

----------------------
### 進階用法 02 >> UserDefinedDictFile :使用者自定詞典。
[![Articut UserDefined Demo](http://i3.ytimg.com/vi/fOyyQyVkZ2k/hqdefault.jpg)](https://youtu.be/fOyyQyVkZ2k "Articut UserDefined Demo")

因為 Articut 只處理「語言知識」而不處理「百科知識」。
我們提供「使用者自定義」詞彙表的功能，使用 Dictionary 格式，請自行編寫。

UserDefinedFile.json
```
{"雷姆":["小老婆"],
 "艾蜜莉亞":["大老婆"],
 "初音未來": ["初音", "只是個軟體"],
 "李敏鎬": ["全民歐巴", "歐巴"]}
```

runArticut.py
```
from ArticutAPI import Articut
from pprint import pprint

articut = Articut()
userDefined = "./UserDefinedFile.json"
inputSTR = "我的最愛是小老婆，不是初音未來。"

# 使用自定義詞典
resultDICT = articut.parse(inputSTR, userDefinedDictFILE=userDefined)
pprint(resultDICT)

# 未使用自定義詞典
resultDICT = articut.parse(inputSTR)
pprint(resultDICT)
```

### 回傳結果
```
# 使用自定義詞典
{"result_pos": ["<ENTITY_pronoun>我</ENTITY_pronoun><FUNC_inner>的</FUNC_inner><ACTION_verb>最愛</ACTION_verb><AUX>是</AUX><UserDefined>小老婆</UserDefined>",
                "，",
                "<FUNC_negation>不</FUNC_negation><AUX>是</AUX><UserDefined>初音未來</UserDefined>",
                "。"],
 "result_segmentation": "我/的/最愛/是/小老婆/，/不/是/初音未來/。/",...}

# 未使用自定義詞典
{"result_pos": ["<ENTITY_pronoun>我</ENTITY_pronoun><FUNC_inner>的</FUNC_inner><ACTION_verb>最愛</ACTION_verb><AUX>是</AUX><ENTITY_nouny>小老婆</ENTITY_nouny>",
                "，",
                "<FUNC_negation>不</FUNC_negation><AUX>是</AUX><ENTITY_nouny>初音</ENTITY_nouny><TIME_justtime>未來</TIME_justtime>",
                "。"],
 "result_segmentation": "我/的/最愛/是/小老婆/，/不/是/初音/未來/。/",...}
```
----------------------
### 進階用法 03 - 調用資料觀光資訊資料庫
政府開放平台中存有「交通部觀光局蒐集各政府機關所發佈空間化觀光資訊」。Articut 可取用其中的資訊，並標記為 \<KNOWLEDGE_place>

**上傳內容 (JSON 格式)**
```
{
	"username": "test@email.com",
	"api_key": "anapikeyfordocthatdoesnwork@all",
	"input_str": "花蓮的原野牧場有一間餐廳",
	"version": "v137",
	"level": "lv1",
	"opendata_place": true
}
```

**回傳內容 (JSON 格式)**
```
{
	"exec_time": 0.013453006744384766,
	"level": "lv1",
	"msg": "Success!",
	"result_pos": ["<LOCATION>花蓮</LOCATION><FUNC_inner>的</FUNC_inner><KNOWLEDGE_place>原野牧場</KNOWLEDGE_place><ACTION_verb>有</ACTION_verb><ENTITY_classifier>一間</ENTITY_classifier><ENTITY_noun>餐廳</ENTITY_noun>"],
	"result_segmentation": "花蓮/的/原野牧場/有/一間/餐廳/",
	"status": True,
	"version": "v137",
	"word_count_balance": 99987
}
```
----------------------

### 進階用法 04 - 基於 TF-IDF 算法的關鍵詞抽取

* articut.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
	* sentence 為要提取關鍵詞的文本
	* topK 為提取幾個 TF-IDF 的關鍵詞，預設值為 20
	* withWeight 為是否返回關鍵詞權重值，預設值為 False
	* allowPOS 僅抽取指定詞性的詞，預設值為空，亦即全部抽取
* articut.analyse.TFIDF(idf\_path=None) 新建 TFIDF 物件，idf_path 為 IDF 語料庫路徑

使用範例：
<https://github.com/Droidtown/ArticutAPI/blob/master/ArticutAPI.py#L624>

---

### 進階用法 05 - 基於 TextRank 算法的關鍵詞抽取

* articut.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=())
	* sentence 為要提取關鍵詞的文本
	* topK 為提取幾個 TF-IDF 的關鍵詞，預設值為 20
	* withWeight 為是否返回關鍵詞權重值，預設值為 False
	* allowPOS 僅抽取指定詞性的詞，預設值為空，亦即全部抽取
* articut.analyse.TextRank() 新建 TextRank 物件

算法論文：[TextRank: Bringing Order into Texts](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)

### 基本思想：

1. 將待抽取關鍵詞的文本斷詞
2. 以固定的窗格大小 (預設值為 5，通過 span 屬性調整)，詞之間的共現關係，建構出不帶權圖
3. 計算途中節點的 PageRank

使用範例：
<https://github.com/Droidtown/ArticutAPI/blob/master/ArticutAPI.py#L629>

---

### 進階用法 06 - 使用 GraphQL 查詢斷詞結果
[![Watch the video](Screenshots/Articut-GraphQL.png)](https://youtu.be/0Ubx08WJ7rU)

### 使用 GraphiQL 工具

**環境需求**

```
Python 3.6.1
$ pip install graphene
$ pip install starlette
$ pip install jinja2
$ pip install uvicorn
```

執行 ArticutGraphQL.py 帶入 Articut 斷詞結果檔案路徑，並開啟瀏覽器輸入網址 http://0.0.0.0:8000/

```
$ python ArticutGraphQL.py articutResult.json
```

### 使用範例 01
![GraphiQL Example 01](Screenshots/GraphiQL_Example01.png)

### 使用範例 02
![GraphiQL Example 02](Screenshots/GraphiQL_Example02.png)

### 使用 Articut-GraphQL

安裝 graphene 模組

```
$ pip install graphene
```
### 使用範例 01
```
inputSTR = "地址：宜蘭縣宜蘭市縣政北七路六段55巷1號2樓"
result = articut.parse(inputSTR)
with open("articutResult.json", "w", encoding="utf-8") as resultFile:
    json.dump(result, resultFile, ensure_ascii=False)
	
graphQLResult = articut.graphQL.query(
    filePath="articutResult.json",
    query="""
	{
	  meta {
	    lang
	    description
	  }
	  doc {
	    text
	    tokens {
	      text
	      pos_
	      tag_
	      isStop
	      isEntity
	      isVerb
	      isTime
	      isClause
	      isKnowledge
	    }
	  }
	}""")
pprint(graphQLResult)
```

### 回傳結果
![Articut-GraphQL Example 01](Screenshots/Articut-GraphQL_Example01.png)

### 使用範例 02
```
inputSTR = "劉克襄在本次活動當中，分享了台北中山北路一日遊路線。他表示當初自己領著柯文哲一同探索了雙連市場與中山捷運站的小吃與商圈，還有商圈內的文創商店與日系雜物店鋪，都令柯文哲留下深刻的印象。劉克襄也認為，雙連市場內的魯肉飯、圓仔湯與切仔麵，還有九條通的日式店家、居酒屋等特色，也能讓人感受到台北舊城區不一樣的魅力。"
result = articut.parse(inputSTR)
with open("articutResult.json", "w", encoding="utf-8") as resultFile:
    json.dump(result, resultFile, ensure_ascii=False)
	
graphQLResult = articut.graphQL.query(
    filePath="articutResult.json",
    query="""
	{
	  meta {
	    lang
	    description
	  }
	  doc {
	    text
	    ents {
	      persons {
	        text
	        pos_
	        tag_
	      }
	    }
	  }
	}""")
pprint(graphQLResult)
```
	
### 回傳結果
![Articut-GraphQL 回傳結果2](Screenshots/Articut-GraphQL_Example02.png)

