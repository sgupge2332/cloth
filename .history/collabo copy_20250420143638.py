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
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    :root {
      --primary-color: #4e9f3d;
      --primary-light: #8fd694;
      --primary-dark: #2c7113;
      --accent-color: #f8b400;
      --bg-gradient-1: #d4fc79;
      --bg-gradient-2: #96e6a1;
    }

    * {
      box-sizing: border-box;
      transition: all 0.3s ease;
    }

    body {
      font-family: 'Noto Sans JP', sans-serif;
      margin: 0;
      padding: 20px;
      background: linear-gradient(135deg, var(--bg-gradient-1), var(--bg-gradient-2));
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .container {
      background: white;
      border-radius: 24px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
      width: 100%;
      max-width: 700px;
      overflow: hidden;
      animation: fadeIn 1s ease forwards;
    }

    @keyframes fadeIn {
      from { transform: translateY(40px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    header {
      background: var(--primary-color);
      color: white;
      padding: 25px;
      text-align: center;
      position: relative;
    }

    header h1 {
      margin: 0;
      font-size: 1.8em;
      font-weight: 700;
    }

    header .subtitle {
      margin-top: 5px;
      font-size: 1em;
      opacity: 0.9;
    }

    .header-icon {
      position: absolute;
      top: -15px;
      right: -15px;
      background: var(--accent-color);
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    .info-display {
      background: #f0f5f0;
      padding: 25px;
      text-align: center;
      font-size: 1.2em;
      font-weight: 600;
      color: #2c7113;
    }

    .info-display div {
      margin: 8px 0;
    }

    form {
      padding: 30px;
    }

    .form-group {
      margin-bottom: 22px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: #444;
      display: flex;
      align-items: center;
    }

    .icon {
      margin-right: 8px;
      color: var(--primary-color);
      width: 22px;
      text-align: center;
    }

    input, select, textarea {
      width: 100%;
      padding: 14px;
      border-radius: 12px;
      border: 2px solid #e0e0e0;
      font-size: 1em;
      font-family: 'Noto Sans JP', sans-serif;
    }

    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--primary-color);
      box-shadow: 0 0 0 3px rgba(78, 159, 61, 0.2);
    }

    button {
      background: var(--primary-color);
      color: white;
      font-size: 1.1em;
      font-weight: 700;
      border: none;
      border-radius: 12px;
      padding: 16px 30px;
      cursor: pointer;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 10px;
      box-shadow: 0 4px 12px rgba(78, 159, 61, 0.3);
    }

    button:hover {
      background: var(--primary-dark);
      transform: translateY(-2px);
      box-shadow: 0 6px 15px rgba(78, 159, 61, 0.4);
    }

    button i {
      margin-right: 10px;
      font-size: 1.2em;
    }

    ::placeholder {
      color: #aaa;
    }

    @media (max-width: 600px) {
      .input-row {
        flex-direction: column;
        gap: 10px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>今日のコーディネート提案</h1>
      <div class="subtitle">あなたにぴったりのファッションを提案します</div>
      <div class="header-icon">
        <i class="fas fa-tshirt"></i>
      </div>
    </header>

    <div class="info-display">
      <div id="datetimeDisplay">現在日時: 取得中...</div>
      <div id="locationDisplay">場所: 取得中...</div>
      <div id="temperatureDisplay">気温: 取得中...</div>
      <div id="weatherDisplay">天気: 取得中...</div>
    </div>

    <form action="/suggest" method="post">
      <div class="form-group">
        <label for="favorite_color"><i class="fas fa-palette icon"></i>好きな色</label>
        <input type="text" id="favorite_color" name="favorite_color" placeholder="例: 青、赤、モノトーン...">
      </div>

      <div class="form-group">
        <label for="owned_clothes"><i class="fas fa-shirt icon"></i>持っている服（カンマ区切り）</label>
        <textarea id="owned_clothes" name="owned_clothes" rows="3" placeholder="例: 青いジーンズ, 白いTシャツ, ベージュのジャケット"></textarea>
      </div>

      <div class="form-group">
        <label for="mood"><i class="fas fa-smile icon"></i>今日の気分</label>
        <input type="text" id="mood" name="mood" placeholder="例: 爽やか、カジュアル、クール...">
      </div>

      <button type="submit">
        <i class="fas fa-wand-magic-sparkles"></i>
        コーディネートを提案
      </button>
    </form>
  </div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      const formatted = now.toLocaleString('ja-JP', {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      });
      document.getElementById('datetimeDisplay').textContent = `現在日時: ${formatted}`;

      if (navigator.geolocation) {
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
                document.getElementById("locationDisplay").textContent = `場所: ${data.state} ${data.city}`;
                document.getElementById("temperatureDisplay").textContent = `気温: ${data.temp}℃`;
                const weatherMap = {
                  "晴": "晴れ",
                  "曇": "曇り",
                  "雨": "雨",
                  "雪": "雪"
                };
                for (const key in weatherMap) {
                  if (data.weather.includes(key)) {
                    document.getElementById("weatherDisplay").textContent = `天気: ${weatherMap[key]}`;
                    break;
                  }
                }
              }
            })
            .catch(err => {
              console.error("APIリクエストに失敗しました", err);
            });
          },
          error => {
            console.error("位置情報の取得に失敗しました。", error);
          }
        );
      }
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
