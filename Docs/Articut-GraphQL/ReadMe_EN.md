[English ReadMe](README_EN.md)
------------------------------

# Articut-GraphQL (類 spaCy 中文)

Articut-GraphQL 是現今完成度最高，可操作中文文本的 類 spaCy 工具。不需要訓練模型，只要把經過 Articut 中文斷詞處理後的結果載入 Articut-GraphQL 即可開始使用。

## 線上操作

即將登場

### 特性
以 `曾正元在新竹的交通大學讀書` 這個句子為例，純粹 spaCy 做訓練，以及只用 Articut-GraphQL 的 `Doc` 各種屬性如下:

![attributes_of_doc](https://github.com/Droidtown/ArticutAPI/tree/master/Screenshots/attributes_of_doc.gif)

### NER

Articut-GraphQL 可辨識 [人名]、[人稱代名詞]、[地名]、[台灣道路名稱]、 [台灣地址]、[URL]…等「命名實體」(Named Entity)

![ner_of_doc](https://github.com/Droidtown/ArticutAPI/tree/master/Screenshots/ner_of_doc.png)

## 開始使用



### 系统要求

Python 3.5+

### 安装
`git clone git@github.com:Droidtown/ArticutAPI.git`

### 指定文本
以 "articutResult.json" 為例。其內容應為經過 Articut 斷詞處理後的結果，另存成 .json 格式。

**`filepath: "articutResult.json"`**

### 指定句法規則
目前僅支援「繁體中文」，故只能填寫大寫的 "TW"

**`model:"TW"`**

### 開始操作



## 授權

MIT License - 詳參 [LICENSE.md](https://github.com/Droidtown/ArticutAPI/blob/master/LICENSE)