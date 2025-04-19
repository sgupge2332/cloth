import os
import google.generativeai as genai

# APIキーを環境変数から取得
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# モデル指定
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# ユーザー入力（仮）
date = "2025-04-18"
temperature = 20
weather = "晴れ"
location = "東京"
favorite_color = "青"
owned_clothes = ["青いジーンズ", "白いTシャツ", "ベージュのジャケット", "ネイビーのシャツ"]
mood = "青空のような爽やかな気分"

# プロンプト生成
prompt = f"""
今日の日付は{date}、場所は{location}、気温は{temperature}度、天気は{weather}です。
私の好きな色は{favorite_color}で、持っている服は次の通りです：{', '.join(owned_clothes)}。
今日は「{mood}」という気分です。
この情報をもとに、上下のコーディネートを提案してください。テキストで、丁寧に。
"""

# コンテンツ生成
response = model.generate_content(prompt)
print(response.text)
