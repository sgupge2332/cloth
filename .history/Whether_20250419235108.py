import requests
import os

def get_weather(lat, lon):
    # 環境変数からAPIキーを取得
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("環境変数 'WEATHER_API_KEY' が設定されていません。")
        return

    # APIのURL（metricは摂氏表示、lang=jaで日本語）
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ja"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        city = data["name"]

        print(f"場所: {city}")
        print(f"天気: {weather}")
        print(f"気温: {temperature}℃")

    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")

# テスト用：大阪（緯度・経度）
get_weather(34.6937, 135.5023)
