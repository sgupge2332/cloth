import requests
import json
from pprint import pprint

url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
# xxxxxには取得したAPIキーを入れる
url = url.format(city_name = "Tokyo", API_key = "W")

jsondata = requests.get(url).json()
pprint(jsondata)
