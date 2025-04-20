from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>位置情報と天気</title>
</head>
<body>
    <h1>位置情報と天気</h1>
    <p id="location"></p>
    <p id="weather"></p>
    <script>
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                document.getElementById("location").textContent = `緯度: ${lat}, 経度: ${lng}`;

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
                        document.getElementById("weather").textContent = 
                            `天気: ${data.weather}, 気温: ${data.temp}°C`;
                    } else {
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
    result = get_weather_info(lat, lng)
    return jsonify(result)

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
