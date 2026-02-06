# -*- coding: utf-8 -*-
"""
V1.5 - Gemini API 測試腳本
執行後送一句話給 AI，印出回覆，確認金鑰與連線正常。
"""
from google import genai
import config

# 若 .env 沒填金鑰，先提醒
if not config.GEMINI_API_KEY:
    print("錯誤：請在 .env 填寫 GEMINI_API_KEY")
    exit(1)


def test_ai():
    # 用金鑰建立 Gemini 客戶端（新套件 google-genai）
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    try:
        # 使用 gemini-2.0-flash 送一句話，取得 AI 回覆
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="你好，我是 V1.5 避險系統，請跟我打聲招呼。",
        )
        print("--- AI 回覆成功 ---")
        print(response.text)
    except Exception as e:
        err_str = str(e)
        # 429 表示免費額度用完，給較清楚的說明
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
            print("【配額已用完】")
            print("  Gemini 免費方案本日/本分鐘額度已用完。")
            print("  請約 35 秒後再試，或到 Google AI Studio 查看用量與方案：")
            print("  https://ai.google.dev/gemini-api/docs/rate-limits")
        else:
            print(f"連線或 API 錯誤：{e}")
    finally:
        # 關閉客戶端，釋放連線資源
        client.close()


if __name__ == "__main__":
    test_ai()
