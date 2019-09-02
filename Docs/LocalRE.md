# Articut Address
-----------------
## 地址的格式
地址，是一串的字符，內含國家、省份、城市或鄉村、街道、門牌號碼、屋邨、大廈等建築物名稱，或者再加樓層數目、房間編號等。一個有效的地址應該是**獨一無二**的，才能讓郵差等物流從業員派送郵件，或者上門收件。 

羅斯福路四段，指的是地理上的`區域`，而不是一個`地址`，因為光是看到「羅斯福路四段」並無法得知正確的所在位置。
```
X 台北市大安區羅斯福路四段
```

羅斯福路四段1號，指的是地理上的`絕對位置`，並可正確的知道所在位置。
```
O 台北市大安區羅斯福路四段1號
```

## 台灣地址規則
|   行政區名稱    |                  |        |   街道名稱   |     |     |    | 門牌 |    |    |
|:-------------:|:----------------:|:------:|:-----------:|:---:|:---:|:--:|:----:|:--:|:--:|
| `直轄市、縣、市` | 鄉、鎮、縣轄市、區 | 村、里 | `大道、路、街` | 段 | 巷 | 弄 | `號` | 樓 | 室 |

註1：非灰底文字視地區道路及建築物狀況，不一定有此層級之名稱。
註2：部分偏遠地區無明確之路名，則在鄰之下劃定次分區，依次分區中之建築物編號。

-----------------

## 開始使用
```python3
inputSTR = "7-11的新店位於台北市信義區忠孝東路四段559巷24號"
result = articut.parse(inputSTR)
```

### 斷詞結果
```txt
7-11/的/新店/位於/台北市信義區忠孝東路四段559巷24號/
```

### 標記結果
```json
["<ENTITY_oov>7-11</ENTITY_oov><FUNC_inner>的</FUNC_inner><ENTITY_nouny>新店</ENTITY_nouny><ACTION_verb>位於</ACTION_verb><KNOWLEDGE_addTW>台北市信義區忠孝東路四段559巷24號</KNOWLEDGE_addTW>"]
```

### 列出所有的台灣地址

```python3
addTWLIST = articut.getAddTWLIST(result)
```
擷取 `<KNOWLEDGE_addTW>`...`<KNOWLEDGE_addTW>` 的結果。
```json
[[(132, 151, "台北市信義區忠孝東路四段559巷24號")]]
```

### 分段地址
```python3
##localRE: 市
cityResult = articut.localRE.getAddressCity(result)
[[(132, 135, "台北市")]]

##localRE: 區
districtResult = articut.localRE.getAddressDistrict(result)
[[(135, 138, "信義區")]]

##localRE: 路
roadResult = articut.localRE.getAddressRoad(result)
[[(138, 142, "忠孝東路")]]

##localRE: 段
sectionResult = articut.localRE.getAddressSection(result)
[[(142, 144, "四段")]]

##localRE: 巷、弄
alleyResult = articut.localRE.getAddressAlley(result)
[[(144, 148, '559巷')]]

##localRE: 號
numberResult = articut.localRE.getAddressNumber(result)
[[(148, 151, "24號")]]
```
