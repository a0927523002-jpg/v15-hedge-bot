# -*- coding: utf-8 -*-
"""
V1.5 - LINE 機器人測試（B 計畫）
收到使用者文字訊息時回覆一句，確認 Webhook 與金鑰正常。
使用 linebot.v3 API，避免棄用警告。
"""
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent
from linebot.v3.webhooks.models import TextMessageContent

import config

# 若 .env 沒填 LINE 金鑰，先提醒
if not config.LINE_CHANNEL_ACCESS_TOKEN or not config.LINE_CHANNEL_SECRET:
    print("錯誤：請在 .env 填寫 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET")
    exit(1)

# 建立 Flask 與 LINE v3 客戶端
app = Flask(__name__)
configuration = Configuration(access_token=config.LINE_CHANNEL_ACCESS_TOKEN)
messaging_api = MessagingApi(configuration)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """使用者傳文字時，回覆一句確認訊息"""
    reply_text = f"收到！我是 V1.5 避險系統。你剛說：{event.message.text}"
    messaging_api.reply_message(
        ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=reply_text)])
    )


@app.route("/webhook", methods=["POST"])
def webhook():
    """LINE 平台會把使用者訊息 POST 到這個網址"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception:
        abort(400)
    return "OK"


@app.route("/", methods=["GET"])
def index():
    """方便確認伺服器有在跑"""
    return "V1.5 LINE Bot 運行中，Webhook 路徑：/webhook"


if __name__ == "__main__":
    # 本機測試用；對外需搭配 ngrok 並在 LINE 後台設 Webhook 為 https://xxx.ngrok.io/webhook
    import logging
    # 關掉 Flask 內建伺服器的紅字警告，本機測試用沒問題
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    print("LINE Bot 啟動，Webhook：http://localhost:5000/webhook")
    app.run(host="0.0.0.0", port=5000)
