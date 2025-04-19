import os
import google.generativeai as genai

# APIキーを環境変数から取得
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Gemini 1.5 Pro モデルで生成
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

response = model.generate_content("こんにちは、自己紹介してください！")
print(response.text)
