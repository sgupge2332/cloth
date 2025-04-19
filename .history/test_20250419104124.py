import os
import google.generativeai as genai

# 環境変数からAPIキーを取得
api_key = os.getenv("GEMINI_API_KEY")

# APIキーが取得できていない場合のエラーハンドリング
if not api_key:
    raise ValueError("GEMINI_API_KEY 環境変数が設定されていません")

genai.configure(api_key=api_key)

# モデルの一覧を取得
models = genai.list_models()

for model in models:
    print(model.name)
