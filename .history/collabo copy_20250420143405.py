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
    :root {
      --primary-color: #4e9f3d;
      --primary-light: #8fd694;
      --primary-dark: #2c7113;
      --accent-color: #f8b400;
      --bg-gradient-1: #f0fdf4;
      --bg-gradient-2: #d4fbe8;
    }

    * {
      box-sizing: border-box;
      transition: all 0.3s ease;
    }

    body {
      font-family: 'Noto Sans JP', sans-serif;
      margin: 0;
      padding: 20px;
      background: linear-gradient(120deg, var(--bg-gradient-1), var(--bg-gradient-2));
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .container {
      background: white;
      border-radius: 30px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
      max-width: 800px;
      width: 100%;
      overflow: hidden;
      animation: fadeIn 0.8s ease;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    header {
      background: var(--primary-color);
      color: white;
      padding: 40px 20px 60px;
      text-align: center;
      position: relative;
    }

    header h1 {
      margin: 0;
      font-size: 2em;
    }

    .subtitle {
      font-size: 1.1em;
      opacity: 0.9;
      margin-top: 8px;
    }

    .header-icon {
      position: absolute;
      bottom: -30px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--accent-color);
      width: 80px;
      height: 80px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 36px;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }

    form {
      padding: 50px 30px 30px;
    }

    .auto-input-section {
      background: #f7fcf5;
      border: 3px dashed var(--primary-light);
      border-radius: 20px;
      padding: 30px;
      margin-bottom: 30px;
    }

    .input-row {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }

    .form-group {
      flex: 1 1 45%;
      display: flex;
      flex-direction: column;
    }

    label {
      font-weight: 700;
      color: #333;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      font-size: 1.1em;
    }

    label .icon {
      margin-right: 10px;
      color: var(--primary-color);
      font-size: 1.2em;
    }

    input,
    select,
    textarea {
      font-size: 1.1em;
      padding: 16px;
      border-radius: 14px;
      border: 2px solid #ddd;
      background: #fff;
      font-family: 'Noto Sans JP', sans-serif;
    }

    input:focus,
    select:focus,
    textarea:focus {
      border-color: var(--primary-color);
      box-shadow: 0 0 0 4px rgba(78, 159, 61, 0.2);
      outline: none;
    }

    textarea {
      resize: vertical;
    }

    button {
      background: var(--primary-color);
      color: white;
      font-weight: bold;
      font-size: 1.2em;
      padding: 18px;
      border: none;
      border-radius: 14px;
      cursor: pointer;
      width: 100%;
      margin-top: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 8px 20px rgba(78, 159, 61, 0.3);
    }

    button i {
      margin-right: 12px;
    }

    button:hover {
      background: var(--primary-dark);
      transform: scale(1.02);
    }

    @media (max-width: 600px) {
      .form-group {
        flex: 1 1 100%;
      }

      header h1 {
        font-size: 1.6em;
      }

      .header-icon {
        width: 60px;
        height: 60px;
        font-size: 28px;
        bottom: -20px;
      }

      form {
        padding: 60px 20px 20px;
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

    <form action="/suggest" method="post">
      <div class="auto-input-section">
        <div class="input-row">
          <div class="form-group">
            <label for="datetime"><i class="fas fa-calendar-alt icon"></i>現在日時</label>
            <input type="datetime-local" id="datetime" name="datetime" required>
          </div>

          <div class="form-group">
            <label for="location"><i class="fas fa-map-marker-alt icon"></i>場所</label>
            <input type="text" id="location" name="location" placeholder="例: 東京" required>
          </div>

          <div class="form-group">
            <label for="temperature"><i class="fas fa-thermometer-half icon"></i>気温（℃）</label>
            <input type="number" id="temperature" name="temperature" required>
          </div>

          <div class="form-group">
            <label for="weather"><i class="fas fa-cloud-sun icon"></i>天気</label>
            <select id="weather" name="weather">
              <option value="晴れ">晴れ</option>
              <option value="曇り">曇り</option>
              <option value="雨">雨</option>
              <option value="雪">雪</option>
            </select>
          </div>
        </div>
      </div>

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
        <i class="fas fa-wand-magic-sparkles"></i>コーディネートを提案
      </button>
    </form>
  </div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      document.getElementById('datetime').value = now.toISOString().slice(0, 16);

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
                document.getElementById("location").value = `${data.state} ${data.city}`;
                document.getElementById("temperature").value = data.temp;

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
