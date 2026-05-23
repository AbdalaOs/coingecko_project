
import requests

from config.connection import get_headers


ep_catalog = {
    'server_status': '/ping', 
    'currencies': '/simple/supported_vs_currencies',
    'coins': '/coins/list',
    'coins_mrkt': '/coins/markets', 
    'historical': f'/coins/{id}/market_chart'}


BASE_URL = "https://api.coingecko.com/api/v3"

# endpoint = f"{BASE_URL}/coins/{coin_id}/market_chart"
EP = ep_catalog['coins']

endpoint = f'{BASE_URL}{EP}'





response = requests.get(endpoint, headers=get_headers())
response.raise_for_status()


data = response.json()

print(data)





