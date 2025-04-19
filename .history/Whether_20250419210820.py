import geocoder

g = geocoder.ip('me')  # 現在のIPアドレスの位置情報を取得

# 緯度経度
print("緯度経度:", g.latlng)

# 県（都道府県）の情報
print("県（都道府県）:", g.state)  # stateには都道府県名が入ります

# 都市（市区町村）の情報
print("都市:", g.city)

# 国の情報
print("国:", g.country)
