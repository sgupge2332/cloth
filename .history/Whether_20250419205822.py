import requests
import os  # ← これが必要！

API_KEY = os.getenv("WHETHER_API_KEY")  # 環境変数から取得

if not API_KEY:
    raise ValueError("環境変数 'WHETHER_API_KEY' が設定されていません！")

city = "Tokyo"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"

response = requests.get(url)
data = response.json()

# エラーハンドリング付きで表示
if "name" in data and "weather" in data:
    print(f"{data['name']}の天気：{data['weather'][0]['description']}")
    print(f"気温：{data['main']['temp']}℃")
else:
    print("エラーが発生しました：", data.get("message", "原因不明です"))
