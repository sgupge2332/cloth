from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>位置情報取得</title>
</head>
<body>
    <h1>位置情報を取得中...</h1>
    <p id="location"></p>
    <p id="address"></p>
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
                        document.getElementById("address").textContent = 
                            `都道府県: ${data.state}, 市区町村: ${data.city}`;
                    } else {
                        document.getElementById("address").textContent = "住所情報を取得できませんでした。";
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
    
    result = get_location_info(lat, lng)
    return result, 200

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
        print(f"APIリクエストエラー: {e}")
        return {"success": False}

if __name__ == "__main__":
    app.run(debug=True)
