import requests

API_KEY = "bb7ebe41d034e03fedccbc8609940982"  # Replace with your actual API key
city = "Tokyo"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"

response = requests.get(url)
data = response.json()

print(f"{data['name']}の天気：{data['weather'][0]['description']}")
print(f"気温：{data['main']['temp']}℃")
