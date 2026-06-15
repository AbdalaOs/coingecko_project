import logging
from datetime import datetime, UTC

from pathlib import Path

from config.config import BASE_URL, ENDPOINTS, HEADERS, COINS_IDS
from client.connection import get_response
from src.utils.logger import logger_settings
from src.utils.saver import save_json
from src.utils.parse_dates import parse_datetime_to_unix

logger = logging.getLogger(__name__)

log_name = Path(__file__).stem




def fetch_OHLC_data(coin: str):


    # Parse dates from execution date and 90 days ago to unix format
    dates = parse_datetime_to_unix(datetime.now(UTC), 90)

    EP = ENDPOINTS['OHLC'].format(coin_id= coin)
    params = {"vs_currency": "usd", 
                "days": 30}


    try: 
        #### Fetch INITIAL historic data (market data)
        # with hourly intervals
        data = get_response(BASE_URL, EP, params, HEADERS)

        #### Saving raw data to json file
        filepath = Path(f"data/raw/OHLC/{coin}")
        # YYYYMMDD_HHMM
        execution_date = dates["timestamp_str"]
        filename = f"{coin}_OHLC_data_{execution_date}.json"
        # Raw data file path and name
        save_json(data, filepath, filename)
        logger.info(f"Raw data saved to: {filepath}/{filename}")


    except Exception:
        logger.exception(f"Error fetching OHLC data for {coin}.")  
        raise     




def run_OHLC_data():

    for coin in COINS_IDS:

        logger.info(f"Fetching raw OHLC data for: {coin}.")

        fetch_OHLC_data(coin)

    logger.info("Raw OHLC data fetching process completed.")







def main():
    logger_settings(log_name)

    run_OHLC_data()







if __name__ == "__main__":
    main()