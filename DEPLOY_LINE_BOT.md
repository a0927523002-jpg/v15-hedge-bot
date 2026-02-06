# LINE Bot 部署到雲端（超詳細步驟）

用 **Render** 免費方案把 Bot 放上雲端，取得固定網址，就不用 ngrok、也不用一直開電腦。  
下面每一步都拆開寫，照著做即可。

---

## 第零步：先確認這兩件事

1. **電腦已安裝 Git**  
   - 若沒裝：到 https://git-scm.com/download/win 下載 Windows 版，安裝時照預設選項即可。  
   - 裝好後開**新的** PowerShell，輸入 `git --version`，有出現版本就代表成功。

2. **專案在正確的資料夾**  
   - 用 PowerShell 或 VS Code 終端機，切到專案目錄：  
     `cd D:\對沖程式`  
   - 之後所有 `git` 指令都在這個資料夾裡執行。

---

## 第一步：把程式推到 GitHub

### 1-1. 登入 GitHub 並建立新倉庫

1. 打開瀏覽器，到 **https://github.com**，登入（沒有帳號就註冊一個）。
2. 點右上角 **「+」** → 選 **「New repository」**。
3. 填寫：
   - **Repository name**：自己取一個英文名字，例如 `v15-hedge-bot`（不要空格、不要中文）。
   - **Description**：可留空。
   - **Public** 打勾。
   - **不要**勾「Add a README file」。
4. 點下方綠色 **「Create repository」**。  
5. 建立好後，畫面上會出現一個網址，長得像：  
   `https://github.com/你的帳號/v15-hedge-bot.git`  
   **先複製這個網址**，等一下會用到（以下叫「你的 repo 網址」）。

### 1-2. 在本機用 Git 上傳程式

在 **D:\對沖程式** 目錄下，打開 PowerShell 或 VS Code 的終端機，**依序**輸入下面指令（一行一行執行）：

```powershell
# 若這個資料夾從來沒用過 git，先初始化
git init
```

```powershell
# 把所有檔案加入準備上傳的名單（.env 不會被加入，因為在 .gitignore 裡）
git add .
```

```powershell
# 做一個「版本」叫 LINE Bot
git commit -m "LINE Bot"
```

```powershell
# 把目前分支取名為 main（Render 預設用 main）
git branch -M main
```

```powershell
# 告訴 git 你的程式要推到哪一個 GitHub 倉庫（把下面換成「你的 repo 網址」）
git remote add origin https://github.com/你的帳號/你的repo名稱.git
```

例如你的 repo 叫 `v15-hedge-bot`、帳號是 `wayne123`，就輸入：  
`git remote add origin https://github.com/wayne123/v15-hedge-bot.git`

```powershell
# 真正上傳到 GitHub（第一次可能會要你登入 GitHub）
git push -u origin main
```

- 若跳出要你登入，用瀏覽器或 Token 登入即可。  
- 成功的話，重新整理你的 GitHub 網頁，應該會看到 `line_bot.py`、`config.py` 等檔案。

---

## 第二步：在 Render 建立 Web Service

### 2-1. 登入 Render 並連到 GitHub

1. 打開 **https://render.com**，點 **「Get Started for Free」** 或 **「Sign In」**。
2. 選 **「Sign in with GitHub」**，授權 Render 讀取你的 GitHub。
3. 登入後會進到 **Dashboard**（儀表板）。

### 2-2. 建立一個新的 Web Service

1. 在 Dashboard 點藍色按鈕 **「New +」**。
2. 選 **「Web Service」**（不是 Background Worker、也不是 Static Site）。

### 2-3. 連到你的 GitHub 倉庫

1. 畫面上會寫 **「Connect a repository」**。
2. 若第一次用，點 **「Connect account」** 或 **「Configure account」**，選 **GitHub**，再選 **「Only select repositories」**，選你剛建立的那個 repo（例如 `v15-hedge-bot`），按 **「Save」**。
3. 回到 Render，在列表裡找到你的 repo（例如 `wayne123/v15-hedge-bot`），點右邊的 **「Connect」**。

### 2-4. 填寫 Web Service 設定

接下來會出現一頁表單，**一個一個填**：

| 欄位 | 要填什麼 | 說明 |
|------|----------|------|
| **Name** | 例如 `v15-line-bot` | 之後網址會變成 `https://v15-line-bot-xxxx.onrender.com`，可自訂英文。 |
| **Region** | 選 **Singapore** 或 **Oregon** | 離台灣近一點選 Singapore。 |
| **Branch** | `main` | 通常不用改，維持 main。 |
| **Runtime** | **Python 3** | 下拉選單選 Python 3。 |
| **Build Command** | 留空，或填 `pip install -r requirements.txt` | 沒填的話 Render 通常會自動偵測。 |
| **Start Command** | **一定要填**：<br>`gunicorn --bind 0.0.0.0:$PORT line_bot:app` | 複製貼上即可，不要改。 |

### 2-5. 加入 LINE 金鑰（Environment 變數）

1. 在同一頁往下捲，找到 **「Environment」** 或 **「Environment Variables」**。
2. 點 **「Add Environment Variable」** 或 **「+ Add」**。
3. 新增**兩個**變數（Key 和 Value 分開填）：

   **第一個：**
   - **Key**：`LINE_CHANNEL_ACCESS_TOKEN`
   - **Value**：貼上你的 LINE Channel Access Token（在 LINE Developers 後台複製）。

   **第二個：**
   - **Key**：`LINE_CHANNEL_SECRET`
   - **Value**：貼上你的 LINE Channel Secret。

4. 若還有 **「Add Environment Variable」** 再點一次，確認兩個都加完。

### 2-6. 建立服務並等它跑起來

1. 表單最下方點 **「Create Web Service」**。
2. 畫面會開始 **建置（Build）** 和 **部署（Deploy）**，會看到 log 在跑。
3. 等幾分鐘，直到最上面狀態變成 **「Live」**（綠色）或 **「Your service is live」**。
4. 畫面上方會出現你的網址，例如：  
   `https://v15-line-bot-xxxx.onrender.com`  
   **把這個網址複製起來**，下一步要填到 LINE。

---

## 第三步：到 LINE 後台填 Webhook 網址

### 3-1. 打開 LINE Developers 並選你的 Channel

1. 打開 **https://developers.line.biz/**，登入。
2. 若你已經有建立 **Provider** 和 **Channel**，在首頁點進你的 **Provider**，再點你的 **Channel**（Messaging API 那種）。
3. 若還沒建過：點 **「Create a new provider」**，再 **「Create a Messaging API channel」**，照畫面填 Bot 名稱等，建立好後會進到該 Channel。

### 3-2. 找到 Messaging API 設定

1. 在 Channel 頁面，上方會有幾個分頁：**「Basic settings」**、**「Messaging API」** 等。
2. 點 **「Messaging API」** 分頁。

### 3-3. 填 Webhook URL

1. 在 **「Messaging API」** 頁面往下捲，找到 **「Webhook URL」** 這一區。
2. 在 **Webhook URL** 的輸入框填：  
   `https://你的Render網址/webhook`  
   例如你 Render 網址是 `https://v15-line-bot-xxxx.onrender.com`，就填：  
   `https://v15-line-bot-xxxx.onrender.com/webhook`  
   **結尾一定要有 /webhook**。
3. 填完後點旁邊的 **「Update」** 或 **「Verify」**。
4. 若成功，**Verify** 按鈕旁會出現綠勾或「Success」。

### 3-4. 用手機測試

1. 用手機 LINE 搜尋你的 Bot 名稱，或掃 Channel 的 QR Code 加好友。
2. 傳任意一句話給 Bot。
3. 若成功，Bot 會回覆：**「收到！我是 V1.5 避險系統。你剛說：xxx」**。

---

## 第四步：之後要注意的事

- **免費方案**：約 15 分鐘沒有人傳訊息，Render 會讓服務休眠；下次有人傳訊息時可能要等幾秒才會回覆，屬正常。
- **金鑰安全**：LINE 的 Token 和 Secret 只在 Render 的 Environment 裡填，不要寫進程式碼、也不要推上 GitHub。
- **本機測試**：想在本機跑仍可執行 `python line_bot.py`，本機不需要裝 gunicorn。

---

## 常見問題速查

| 狀況 | 可能原因 | 怎麼做 |
|------|----------|--------|
| Render 建置失敗、紅字錯誤 | 缺少套件或 Python 版本 | 確認專案裡有 `requirements.txt`、`Procfile`，Start Command 有填 gunicorn 那行。 |
| LINE Verify 失敗 | 網址填錯或 Bot 還沒 Live | 確認 Webhook URL 是 `https://xxx.onrender.com/webhook`，且 Render 狀態是 Live。 |
| 傳訊息沒回覆 | 服務休眠或金鑰填錯 | 等幾秒再傳一次；到 Render 的 Environment 檢查 Token、Secret 是否和 LINE 後台一致。 |

若某一步畫面長得跟上面寫的不一樣，可以把畫面描述或截圖貼給協助你的人，比較好對照。
