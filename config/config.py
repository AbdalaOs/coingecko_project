import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = os.getenv("BASE_URL")


# Pending of reviewing how to automatize/efficientize the parse of the endpoint

coin_id = "bitcoin"
vs_currency = "usd"
days = 30

endpoint = f"{BASE_URL}/coins/{coin_id}/market_chart"
params = {
    "vs_currency": vs_currency,
    "days": days
    }
