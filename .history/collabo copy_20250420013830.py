from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>今日のコーディネート提案</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    body {
      font-family: 'Noto Sans JP', sans-serif;
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, #d4fc79, #96e6a1);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    h2 { text-align: center; color: #333; margin-bottom: 20px; }
    form {
      background: white;
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      width: 100%;
      max-width: 600px;
      animation: fadeInUp 1s ease forwards;
    }
    @keyframes fadeInUp {
      from { transform: translateY(30px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    label { display: block; margin-top: 15px; font-weight: bold; color: #444; }
    input, select, textarea {
      width: 100%;
      padding: 12px;
      margin-top: 8px;
      border-radius: 10px;
      border: 1px solid #ccc;
      font-size: 1em;
      box-sizing: border-box;
      transition: 0.3s;
    }
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: #66bb6a;
      box-shadow: 0 0 8px rgba(102, 187, 106, 0.5);
    }
    button {
      margin-top: 20px;
      padding: 14px 30px;
      background: #66bb6a;
      color: white;
      font-size: 1.1em;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: background 0.3s ease;
      width: 100%;
    }
    button:hover { background: #4caf50; }
    .icon { margin-right: 8px; color: #66bb6a; }
    ::placeholder { color: #aaa; }
  </style>
</head>
<body>
  <form action="/suggest" method="post">
    <h2><i class="fas fa-tshirt icon"></i>今日のコーディネート提案フォーム</h2>

    <label for="datetime"><i class="fas fa-calendar-alt icon"></i>現在日時:</label>
    <input type="datetime-local" id="datetime" name="datetime" required>

    <label for="location"><i class="fas fa-map-marker-alt icon"></i>場所:</label>
    <input type="text" id="location" name="location" placeholder="例: 東京" required>

    <label for="temperature"><i class="fas fa-thermometer-half icon"></i>気温（℃）:</label>
    <input type="number" id="temperature" name="temperature" required>

    <label for="weather"><i class="fas fa-cloud-sun icon"></i>天気:</label>
    <select id="weather" name="weather">
      <option value="晴れ">晴れ</option>
      <option value="曇り">曇り</option>
      <option value="雨">雨</option>
      <option value="雪">雪</option>
    </select>

    <label for="favorite_color"><i class="fas fa-palette icon"></i>好きな色:</label>
    <input type="text" id="favorite_color" name="favorite_color" placeholder="例: 青">

    <label for="owned_clothes"><i class="fas fa-shirt icon"></i>持っている服（カンマ区切り）:</label>
    <textarea id="owned_clothes" name="owned_clothes" rows="3" placeholder="例: 青いジーンズ, 白いTシャツ, ベージュのジャケット"></textarea>

    <label for="mood"><i class="fas fa-smile icon"></i>今日の気分:</label>
    <input type="text" id="mood" name="mood" placeholder="例: 青空のような爽やかな気分">

    <button type="submit"><i class="fas fa-magic icon"></i>コーディネートを提案して！</button>
  </form>

  <script>
    window.addEventListener('DOMContentLoaded', () => {
      // 日付・時間を自動入力
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      document.getElementById('datetime').value = now.toISOString().slice(0, 16);

      // 位置情報取得＆API連携
      navigator.geolocation.getCurrentPosition(
        position => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;

          fetch("/location", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ lat, lng })
          })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              // 場所・気温
              document.getElementById("location").value = `${data.state} ${data.city}`;
              document.getElementById("temperature").value = data.temp;

              // 天気マッチング
              const weatherDesc = data.weather;
              const weatherSelect = document.getElementById("weather");
              const weatherKeywords = {
                "晴": "晴れ",
                "曇": "曇り",
                "雨": "雨",
                "雪": "雪"
              };

              for (const key in weatherKeywords) {
                if (weatherDesc.includes(key)) {
                  weatherSelect.value = weatherKeywords[key];
                  break;
                }
              }
            }
          });
        },
        error => {
          console.error("位置情報の取得に失敗しました。", error);
        }
      );
    });
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(html)

@app.route("/location", methods=["POST"])
def location():
    data = request.json
    lat = data.get("lat")
    lng = data.get("lng")
    print(f"受け取った緯度: {lat}, 経度: {lng}")

    address_info = get_location_info(lat, lng)
    if not address_info["success"]:
        return jsonify({"success": False})

    weather_info = get_weather_info(lat, lng)
    if not weather_info["success"]:
        return jsonify({"success": False})

    return jsonify({
        "success": True,
        "state": address_info["state"],
        "city": address_info["city"],
        "weather": weather_info["weather"],
        "temp": weather_info["temp"]
    })

def get_location_info(lat, lng):
    api_key = os.getenv("GEO_API_KEY")
    if not api_key:
        print("環境変数 'GEO_API_KEY' が設定されていません。")
        return {"success": False}

    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={api_key}&language=ja"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            place = data['results'][0]['components']
            state = place.get('state', '不明')
            city = place.get('city') or place.get('town') or place.get('village') or '不明'
            print(f"都道府県: {state}, 市区町村: {city}")
            return {"success": True, "state": state, "city": city}
        else:
            return {"success": False}
    except requests.exceptions.RequestException as e:
        print(f"住所APIエラー: {e}")
        return {"success": False}

def get_weather_info(lat, lng):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("環境変数 'WEATHER_API_KEY' が設定されていません。")
        return {"success": False}

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric&lang=ja"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        print(f"天気: {weather}, 気温: {temp}℃")
        return {"success": True, "weather": weather, "temp": temp}
    except requests.exceptions.RequestException as e:
        print(f"天気APIエラー: {e}")
        return {"success": False}

if __name__ == "__main__":
    app.run(debug=True)
