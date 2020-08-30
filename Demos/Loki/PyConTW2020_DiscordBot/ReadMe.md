# 快速上手

### 1 建立 Discord Bot 環境
1. 把 template.env 檔案打開，在 [Discord Developer Portal](https://discord.com/developers/application)中取得的 Bot Token 取代 **{DISCORD_BOT_TOKEN}** (包括左右兩個大括號也一起取代掉)。注意等號前後不留空格。

2. 完成後，檔案另存為 .env 。(注意！在 Linux/Mac 下，以「點」開頭的檔案預設是隱藏檔。)

### 2 建立 Loki Bot
1. 在畫面右上角登入 [卓騰 API 網站](https://api.droidtown.co/), 在畫面下方的「加值應用」點擊 [Loki]，進入 Loki 控制台。

2. 在 Loki 控制台中新建一個專案，並進入專案。

3. 在專案中建立一個意圖，並依序點擊 [瀏覽] > 選擇 GetVenueAddress.ref 檔 > [讀取]。完成後，在畫面最上面點擊左邊的「房子」圖示，回到專案頁。這裡有 Loki 的專案 KEY。

4. 將 PyConTW2020_InfoBot.py 中的 USERNAME 填入你的 Droidtown 使用者帳號 (email)；LOKI_KEY 則填入你產生的 Loki 專案的 API Key

### 3 執行
    python3 DT_InfoBot.py