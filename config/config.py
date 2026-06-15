import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"
ENDPOINTS = {
    'server_status': '/ping', 
    'currencies': '/simple/supported_vs_currencies',
    'coins': '/coins/list',
    'coins_mrkt': '/coins/markets', 
    'historical': '/coins/{coin_id}/market_chart',
    'range_hist': '/coins/{coin_id}/market_chart/range',
    'OHLC': '/coins/{coin_id}/ohlc'
    }
HEADERS = {
    "accept": "application/json",
    "x-cg-demo-api-key": COINGECKO_API_KEY
    }

# LIST OF COINS TO RETRIEVE DATA AND ANALYZE
COINS_IDS = ["bitcoin", "ethereum", "solana", "ripple", "dogecoin"]
