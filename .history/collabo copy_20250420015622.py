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
      --text-color: #333;
      --text-light: #666;
      --card-bg: #f9fbf7;
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
      color: var(--text-color);
    }
    
    .container {
      background: white;
      border-radius: 24px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
      width: 100%;
      max-width: 900px; /* 横幅を拡大 */
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
      padding: 30px;
      text-align: center;
      position: relative;
    }
    
    header h1 {
      margin: 0;
      font-size: 2em;
      font-weight: 700;
    }
    
    header .subtitle {
      margin-top: 8px;
      font-size: 1.1em;
      opacity: 0.9;
    }
    
    .header-icon {
      position: absolute;
      top: -20px;
      right: -20px;
      background: var(--accent-color);
      width: 80px;
      height: 80px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 36px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    form {
      padding: 40px;
    }
    
    .form-group {
      margin-bottom: 28px;
    }
    
    .info-section {
      background: var(--card-bg);
      border-radius: 20px;
      padding: 30px;
      margin-bottom: 40px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .info-section-title {
      color: var(--primary-dark);
      font-weight: 700;
      margin-bottom: 25px;
      font-size: 1.4em;
      display: flex;
      align-items: center;
    }
    
    .info-section-title i {
      margin-right: 12px;
      color: var(--primary-color);
      font-size: 1.2em;
    }
    
    .info-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr); /* 3列に変更 */
      gap: 20px;
    }
    
    .info-item {
      background: white;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
      transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .info-item:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* 特別な気温表示 */
    .info-item.temperature {
      grid-column: span 3;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 25px 20px;
    }
    
    .temp-display {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 10px;
    }
    
    .temp-value {
      font-size: 3.5em;
      font-weight: 700;
      color: var(--primary-dark);
      margin-right: 5px;
      line-height: 1;
    }
    
    .temp-unit {
      font-size: 1.8em;
      color: var(--primary-color);
      font-weight: 500;
      margin-top: -15px;
    }
    
    .info-label {
      font-size: 0.9em;
      color: var(--text-light);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
    }
    
    .info-label i {
      color: var(--primary-color);
      margin-right: 8px;
      width: 20px;
      text-align: center;
      font-size: 1.1em;
    }
    
    .info-value {
      font-size: 1.3em;
      font-weight: 500;
      color: var(--text-color);
      padding: 5px 0;
    }
    
    /* 日付と時間の大きな表示 */
    .info-item.date-time {
      grid-column: span 2;
      text-align: center;
      padding: 25px 20px;
    }
    
    .date-display {
      font-size: 1.6em;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--primary-dark);
    }
    
    .time-display {
      font-size: 2.2em;
      font-weight: 700;
      color: var(--text-color);
    }
    
    /* 地域と天気の表示 */
    .location-weather {
      padding: 25px 20px;
      text-align: center;
    }
    
    .weather-icon {
      font-size: 2.5em;
      margin: 10px 0;
      color: var(--accent-color);
    }
    
    label {
      display: block;
      margin-bottom: 10px;
      font-weight: 500;
      color: #444;
      display: flex;
      align-items: center;
      font-size: 1.1em;
    }
    
    .icon {
      margin-right: 10px;
      color: var(--primary-color);
      width: 24px;
      text-align: center;
    }
    
    input, select, textarea {
      width: 100%;
      padding: 16px;
      border-radius: 14px;
      border: 2px solid #e0e0e0;
      font-size: 1.05em;
      font-family: 'Noto Sans JP', sans-serif;
    }
    
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--primary-color);
      box-shadow: 0 0 0 3px rgba(78, 159, 61, 0.2);
    }
    
    .hidden-input {
      display: none;
    }
    
    button {
      background: var(--primary-color);
      color: white;
      font-size: 1.2em;
      font-weight: 700;
      border: none;
      border-radius: 14px;
      padding: 18px 30px;
      cursor: pointer;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 20px;
      box-shadow: 0 6px 15px rgba(78, 159, 61, 0.3);
    }
    
    button:hover {
      background: var(--primary-dark);
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(78, 159, 61, 0.4);
    }
    
    button i {
      margin-right: 12px;
      font-size: 1.3em;
    }
    
    ::placeholder {
      color: #aaa;
    }
    
    @media (max-width: 768px) {
      .info-grid {
        grid-template-columns: 1fr;
      }
      
      .info-item.date-time,
      .info-item.temperature {
        grid-column: span 1;
      }
      
      .container {
        max-width: 100%;
      }
      
      form {
        padding: 25px;
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
      <div class="info-section">
        <div class="info-section-title">
          <i class="fas fa-info-circle"></i>現在の情報
        </div>
        
        <div class="info-grid">
          <!-- 日付と時間の大きな表示 -->
          <div class="info-item date-time">
            <div class="info-label">
              <i class="fas fa-calendar-alt"></i>日付・時間
            </div>
            <div class="date-display" id="formatted-date">
              読み込み中...
            </div>
            <div class="time-display" id="formatted-time">
              --:--
            </div>
            <input type="datetime-local" id="datetime" name="datetime" class="hidden-input" required>
          </div>
          
          <!-- 地域と天気の表示 -->
          <div class="info-item location-weather">
            <div class="info-label">
              <i class="fas fa-map-marker-alt"></i>場所・天気
            </div>
            <div class="info-value" id="formatted-location">
              読み込み中...
            </div>
            <div class="weather-icon" id="weather-icon">
              <i class="fas fa-cloud-sun"></i>
            </div>
            <div class="info-value" id="formatted-weather">
              読み込み中...
            </div>
            <input type="text" id="location" name="location" class="hidden-input" required>
            <select id="weather" name="weather" class="hidden-input">
              <option value="晴れ">晴れ</option>
              <option value="曇り">曇り</option>
              <option value="雨">雨</option>
              <option value="雪">雪</option>
            </select>
          </div>
          
          <!-- 大きな気温表示 -->
          <div class="info-item temperature">
            <div class="info-label">
              <i class="fas fa-thermometer-half"></i>現在の気温
            </div>
            <div class="temp-display">
              <span class="temp-value" id="temp-value">--</span>
              <span class="temp-unit">℃</span>
            </div>
            <input type="number" id="temperature" name="temperature" class="hidden-input" required>
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
        <i class="fas fa-wand-magic-sparkles"></i>
        コーディネートを提案
      </button>
    </form>
  </div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {
      // 日付・時間処理
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      
      // hidden フィールドの設定
      document.getElementById('datetime').value = now.toISOString().slice(0, 16);
      
      // 表示用フォーマット
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        weekday: 'long'
      };
      const timeOptions = {
        hour: '2-digit',
        minute: '2-digit'
      };
      
      document.getElementById('formatted-date').textContent = now.toLocaleDateString('ja-JP', options);
      document.getElementById('formatted-time').textContent = now.toLocaleTimeString('ja-JP', timeOptions);
      
      // 位置情報取得＆API連携
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
                // 表示用の場所・天気・気温を設定
                document.getElementById("formatted-location").textContent = `${data.state} ${data.city}`;
                document.getElementById("temp-value").textContent = data.temp;
                
                // hidden フィールドにも設定
                document.getElementById("location").value = `${data.state} ${data.city}`;
                document.getElementById("temperature").value = data.temp;

                // 天気マッチングとアイコン設定
                const weatherDesc = data.weather;
                const weatherSelect = document.getElementById("weather");
                const weatherDisplay = document.getElementById("formatted-weather");
                const weatherIconContainer = document.getElementById("weather-icon");
                
                const weatherKeywords = {
                  "晴": "晴れ",
                  "曇": "曇り",
                  "雨": "雨",
                  "雪": "雪"
                };
                
                const weatherIcons = {
                  "晴れ": "sun",
                  "曇り": "cloud",
                  "雨": "cloud-rain",
                  "雪": "snowflake"
                };

                let matchedWeather = "晴れ"; // デフォルト値
                
                for (const key in weatherKeywords) {
                  if (weatherDesc.includes(key)) {
                    matchedWeather = weatherKeywords[key];
                    break;
                  }
                }
                
                weatherSelect.value = matchedWeather;
                weatherDisplay.textContent = matchedWeather;
                weatherIconContainer.innerHTML = `<i class="fas fa-${weatherIcons[matchedWeather]}"></i>`;
              }
            })
            .catch(err => {
              document.getElementById("formatted-location").textContent = "取得できませんでした";
              document.getElementById("temp-value").textContent = "--";
              document.getElementById("formatted-weather").textContent = "取得できませんでした";
              console.error("APIリクエストに失敗しました", err);
            });
          },
          error => {
            document.getElementById("formatted-location").textContent = "位置情報を許可してください";
            document.getElementById("temp-value").textContent = "--";
            document.getElementById("formatted-weather").textContent = "位置情報を許可してください";
            console.error("位置情報の取得に失敗しました。", error);
          }
        );
      } else {
        document.getElementById("formatted-location").textContent = "位置情報に対応していません";
        document.getElementById("temp-value").textContent = "--";
        document.getElementById("formatted-weather").textContent = "位置情報に対応していません";
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
