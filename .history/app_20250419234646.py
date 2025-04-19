from flask import Flask, request, render_template_string

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
    <script>
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                document.getElementById("location").textContent = `緯度: ${lat}, 経度: ${lng}`;

                // PythonサーバーへPOST送信
                fetch("/location", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ lat, lng })
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
    # ここにOpenCage呼び出しなどを追加して処理する
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
