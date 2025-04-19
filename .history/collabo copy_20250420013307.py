from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>位置情報と天気</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f2f2f2;
        }
        .form-box {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            max-width: 400px;
            margin: auto;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .form-box h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }
        .value {
            background-color: #f9f9f9;
            padding: 8px 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="form-box">
        <h1>現在地と天気情報</h1>
        <div class="form-group">
            <div class="label">位置情報:</div>
            <div class="value" id="location">取得中...</div>
        </div>
        <div class="form-group">
            <div class="label">住所:</div>
            <div class="value" id="address">取得中...</div>
        </div>
        <div class="form-group">
            <div class="label">天気:</div>
            <div class="value" id="weather">取得中...</div>
        </div>
    </div>

    <script>
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                document.getElementById("location").textContent = `緯度: ${lat.toFixed(4)}, 経度: ${lng.toFixed(4)}`;

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
                        document.getElementById("address").textContent = 
                            `都道府県: ${data.state}, 市区町村: ${data.city}`;
                        document.getElementById("weather").textContent = 
                            `天気: ${data.weather}, 気温: ${data.temp}°C`;
                    } else {
                        document.getElementById("address").textContent = "住所情報を取得できませんでした。";
                        document.getElementById("weather").textContent = "天気情報を取得できませんでした。";
                    }
                });
            },
            error => {
                document.getElementById("location").textContent = "位置情報取得に失敗しました。";
                console.error(error);
            }
        );
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
