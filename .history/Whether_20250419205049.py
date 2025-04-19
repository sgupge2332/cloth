import requests

API_KEY = "86b53f095cc2dfdbed08c9517db81a68"  # Replace with your actual API key
city = "Tokyo"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"

response = requests.get(url)
data = response.json()

print(f"{data['name']}の天気：{data['weather'][0]['description']}")
print(f"気温：{data['main']['temp']}℃")
