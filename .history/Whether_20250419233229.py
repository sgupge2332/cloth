import geocoder

# 緯度・経度の指定（例：熊本県玉名郡和水町あたり）
latlng = [33.2440302, 130.2959797]

# 逆ジオコーディングで住所情報を取得
g = geocoder.osm(latlng, method='reverse')

# 緯度経度
print("緯度経度:", g.latlng)

# 都道府県（state）
print("都道府県:", g.state)

# 市区町村（city）
print("市区町村:", g.city)

# 国（country）
print("国:", g.country)
