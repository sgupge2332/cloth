import requests

def check_open_cage_api(lat, lng, api_key):
    # OpenCage APIのURL
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={api_key}&language=ja"

    try:
        # APIリクエストを送信
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーチェック
        
        # JSONレスポンスを取得
        data = response.json()

        # レスポンスに結果が含まれているか確認
        if data['results']:
            place = data['results'][0]['components']
            print(f"場所: {place}")
            return True  # 正常にAPIが動作した
        else:
            print("結果が見つかりませんでした。")
            return False

    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return False

# テスト用の緯度経度（例：東京都庁）
latitude = 35.6895
longitude = 139.6917

# ここにOpenCageで取得した自分のAPIキーを入力
api_key = 'fc198e5b44bc454690c836ffb87ab541'

# APIチェックを実行
check_open_cage_api(latitude, longitude, api_key)
