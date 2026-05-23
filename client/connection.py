import requests
import logging

from config.config import COINGECKO_API_KEY

logger = logging.getLogger(__name__)

def connect_to_api(endpoint: str, params: dict = {}) -> requests.response:
    """Test connection to CoinGecko API."""
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
        # raise for status will throw an error for bad responses (4xx or 5xx)
        response.raise_for_status()
        logger.info(f'Response status code: {response.status_code}')
        logger.info("Successfully connected to CoinGecko API.")
    except requests.RequestException as e:
        logger.error(f'Response status code: {response.status_code}')
        logger.error(f"Failed to connect to CoinGecko API: {e}")
        raise

    return response


