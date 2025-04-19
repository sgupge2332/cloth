import geocoder

g = geocoder.ip('me')  # 現在のIPアドレスの位置情報を取得
print(g.latlng)  # 緯度経度
