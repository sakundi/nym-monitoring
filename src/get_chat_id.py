import requests

TELEGRAM_HTTP_API = ""

url = f"https://api.telegram.org/bot{TELEGRAM_HTTP_API}/getUpdates"

print(requests.get(url).json())
