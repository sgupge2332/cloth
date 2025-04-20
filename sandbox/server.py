from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

# 環境変数からAPIキーを取得
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEO_API_KEY = os.getenv("GEO_API_KEY")

@app.route("/")
def index():
    return render_template("input.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")

    # 天気情報を取得
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=ja"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    # 住所情報を取得
    geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={GEO_API_KEY}&language=ja"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    # 必要なデータを抽出
    weather = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    city = geo_data["results"][0]["components"].get("city", "不明")
    state = geo_data["results"][0]["components"].get("state", "不明")

    return jsonify({
        "weather": weather,
        "temp": temp,
        "city": city,
        "state": state
    })

if __name__ == "__main__":
    app.run(debug=True)