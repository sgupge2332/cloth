import requests
import os
import geocoder

def get_current_latlng():
    g = geocoder.ip('me')
    return g.latlng if g.ok else None

def check_open_cage_api(lat, lng):
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
            print(f"都道府県: {place.get('state', '不明')}")
            print(f"市区町村: {place.get('city', place.get('town', place.get('village', '不明')))}")
            return True
        else:
            print("結果が見つかりませんでした。")
            return False

    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return False

# 現在地の緯度経度を取得
current_location = get_current_latlng()
if current_location:
    lat, lng = current_location
    check_open_cage_api(lat, lng)
else:
    print("現在地を取得できませんでした。")
