import requests
import os  # 環境変数の取得に必要！

def check_open_cage_api(lat, lng):
    # 環境変数からAPIキーを取得
    api_key = os.getenv("GEO_API_KEY")
    if not api_key:
        print("環境変数 'GEO_API_KEY' が設定されていません。")
        return False

    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={api_key}&language=ja"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            place = data['results'][0]['components']
            print(f"場所情報: {place}")
            return True
        else:
            print("結果が見つかりませんでした。")
            return False

    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return False

# テスト用緯度経度
latitude = 34.6938
longitude = 135.5011

# APIチェックを実行
check_open_cage_api(latitude, longitude)
