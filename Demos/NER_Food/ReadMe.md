# NER (命名實體辨識) 工具：美食篇

NE (命名實體，也就是叫得出名字的「東西」)，有時候會是兩個詞、三個詞甚至多個詞構成。比如說「台北市立體育館」就至少是由「台北/市立/體育館」等三個詞彙構成的一個實體。這對 NLP 任務而言，困難的地方就在決定「哪些相鄰的詞，可以構成一個命名實體？」

還好，這個問題對 Articut 而言並不困難，因此我們多做了 ArticutAPI 的 NER 工具包！目前已經先行完成了「美食辨識」了！

先做美食的原因，是因為現代 NLP 有許多工作是在分析評價內文。而最常出現評價的地方，就是餐廳食物的評論了。如果沒有做好 NER 的話，像以下的例子：

![兩個詞彙構成一個美食命名實體](https://www.droidtown.co/static/public_img/2word_cuisine.png) 

兩個詞彙還不算太複雜的，何況兩個都是可能的食材時。在中文裡，我們也很常見到三個詞彙構成的美食命名實體，而且這三個詞彙的意義還不太相同：

![三個詞彙構成一個美食命名實體](https://www.droidtown.co/static/public_img/3word_cuisine.png) 

三個詞彙裡，有一個表示地方風格，名詞做為形容詞用，另一個做為烹煮方法的動詞，還有一個才是食材。

過去有許多利用統計機率模型或是機器學習模型的研究論文，在這裡，我們直接利用 ArticutAPI 的 NER 工具包就可以了。它有兩個選項，一方面可以擷取出「只有食物名稱」的命名實體，另一方面，也可以擷取出「有地方風格詞彙 + 食物名稱」的命名實體。示範如下：

```python
from ArticutAPI import Articut

username = "" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
apikey   = "" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。
articut = Articut(username, apikey)

inputSTR = "今天晚上特別點了一道法式焗烤龍蝦來慶祝疫情結束！"
resultDICT = articut.parse(inputSTR)

foodLIST = articut.NER.getFood(resultDICT)
#如此一來就能取得 [焗烤龍蝦] 的美食名稱命名實體了

foodLocLIST = articut.NER.getFood(resultDICT, withLocation=True)
#如此一來，就能取得 [法式焗烤龍蝦] 的這樣既含有地方風格詞彙，又有美食名稱的命名實體囉！
```

以圖表示如下：

![美食命名實體](https://www.droidtown.co/static/public_img/NER.getFood.png) 

只取出 [牛肉麵]，因為預設是不計入美食詞彙前的地方特色詞彙。如果要加入地方詞彙特色，請把參數調整為 True：

![地方風格 + 美食命名實體](https://www.droidtown.co/static/public_img/NER.getFoodLoc.png) 

就這樣。透過 ArticutAPI 的 NER 工具，就能輕鬆地取出文本中的美食命名實體囉！
