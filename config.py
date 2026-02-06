# -*- coding: utf-8 -*-
"""
V1.5 全天候避險系統 - 設定檔
敏感金鑰從 .env 讀取，其餘為 MA / 風控 / 交易時段參數
"""
import os

# 從專案目錄載入 .env（金鑰不寫在程式碼裡）
from dotenv import load_dotenv
load_dotenv()

# ========== API 金鑰（由 .env 提供，程式碼中不寫死） ==========
# 群益證券 Shioaji API
SHIOAJI_ACCOUNT = os.getenv("SHIOAJI_ACCOUNT", "")
SHIOAJI_PASSWORD = os.getenv("SHIOAJI_PASSWORD", "")
SHIOAJI_CA_PASSWORD = os.getenv("SHIOAJI_CA_PASSWORD", "")

# Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")


# ========== 技術指標參數 ==========
# 移動平均線週期 (用於日盤/夜盤判斷)
MA_PERIOD = 5


# ========== 風控參數 ==========
# 日盤：每日最多試錯次數
DAY_MAX_PROBES = 2

# 夜盤 (含盲區 15:00~17:25)：合計最多試錯次數
NIGHT_MAX_PROBES = 1

# OCO 安全鎖 (點數)
OCO_STOP_LOSS_POINTS = 50   # 停損：進場價 + 50 點
OCO_TAKE_PROFIT_POINTS = 300  # 停利：進場價 - 300 點


# ========== 交易時段參數 (精確時間字串，避免 API 報錯) ==========
# 日盤時段 (微台指、台積電期皆可交易)
DAY_SESSION_START = "08:45"
DAY_SESSION_END = "13:45"

# 微台指(TM) 夜盤時段 (避險主要戰場)
TM_NIGHT_START = "15:00"
TM_NIGHT_END = "05:00"   # 跨日，到次日 05:00

# 台積電期(QFF) 夜盤時段 (核心持倉)
QFF_NIGHT_START = "17:25"
QFF_NIGHT_END = "05:00"  # 跨日，到次日 05:00

# 時差盲區：微台指已開、台積電期尚未開 (此段禁止查 QFF 報價)
GAP_PERIOD_START = "15:00"
GAP_PERIOD_END = "17:25"

# 換日結算點 (重置每日計數器用)
RESET_TIME = "05:00"
