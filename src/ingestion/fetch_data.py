import logging
from datetime import datetime
import json
import os
from dotenv import load_dotenv

import requests
import pandas as pd

from config.config import BASE_URL, endpoint, params, coin_id, vs_currency, days
from client.connection import connect_to_api


logger = logging.getLogger(__name__)


# def fetch_data(response: requests.response):
    
#     data = response.json()
    
#     # Create DataFrames for each metric
#     prices_df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
#     market_caps_df = pd.DataFrame(data["market_caps"], columns=["timestamp", "market_cap"])
#     volumes_df = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
    
#     # Merge all metrics on timestamp
#     df = prices_df.merge(market_caps_df, on="timestamp").merge(volumes_df, on="timestamp")
    
#     # Convert UNIX timestamp (milliseconds) to datetime
#     df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
#     df.set_index("timestamp", inplace=True)

#     return df


def fetch_raw_data(response: requests.response, filename: str):

    data = response.json()

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)








def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[
                                logging.FileHandler("logs/ingestion.log"),
                                logging.StreamHandler()
                                ]
                        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'data/raw/raw_{coin_id}_price_from_{days}_days_{timestamp}.json'

    # API Test connection
    logger.info("Testing connection to CoinGecko API ...")
    response = connect_to_api(endpoint, params)

    logger.info("Starting raw data fetching process ...")
    fetch_raw_data(response, filename)

    logger.info("Raw data fetching process completed.")






if __name__ == "__main__":
    main()