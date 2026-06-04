import logging
from datetime import datetime, UTC

from pathlib import Path

from config.config import BASE_URL, ENDPOINTS, HEADERS, COINS_IDS
from client.connection import get_response
from src.utils.logger import logger_settings
from src.utils.saver import save_json, save_checkpoint
from src.utils.loader import load_json
from src.utils.parse_dates import parse_datetime_to_unix

logger = logging.getLogger(__name__)

log_name = Path(__file__).stem




def get_params(check_path: Path, 
               coin: str, 
               dates: dict):

    exec_unix = dates["timestamp_unix"]

    if check_path.exists():

        logger.info(f"Loading extraction file {check_path}.")
        logger.info("Fetching hourly data from last checkpoint.")

        checkpoint = load_json(check_path)
        historic_unix = checkpoint["last_timestamp_unix"]
        
        logger.info(f"Historic data used: {checkpoint['last_timestamp_str']}")

    else: 

        logger.info(f"Last extraction file does not exists.")
        logger.info("Fetching hourly data from last 90 days.")

        historic_unix = dates["previous_unix"]
        
        logger.info(f"Historic data used: {dates['previous_str']}")


    #### Fetch INITIAL historic data (market data)
    # with hourly intervals
    EP = ENDPOINTS['range_hist'].format(coin_id= coin)
    params = {"vs_currency": "usd", 
                "from": historic_unix, 
                "to": exec_unix,
                "interval": "hourly"}

    return EP, params




def fetch_market_data(coin: str):

    check_path = Path(f"data/raw/checkpoint/{coin}/latest_data.json")

    # Parse dates from execution date and 90 days ago to unix format
    dates = parse_datetime_to_unix(datetime.now(UTC), 90)

    EP, params = get_params(check_path, coin, dates)

    try: 
        #### Fetch INITIAL historic data (market data)
        # with hourly intervals
        data = get_response(BASE_URL, EP, params, HEADERS)

        #### Saving raw data to json file
        filepath = Path(f"data/raw/historic/{coin}/hourly_interval")
        # YYYYMMDD_HHMM
        execution_date = dates["timestamp_str"]
        filename = f"{coin}_chart_data_{execution_date}.json"
        # Raw data file path and name
        save_json(data, filepath, filename)
        logger.info(f"Raw data saved to: {filepath}/{filename}")

        #### Create checkpoint
        # At last create checkpoint json with timestamp of last execution
        save_checkpoint(coin, data, execution_date)

    except Exception:
        logger.exception(f"Error fetching initial historical data for {coin}.")  
        raise     











def main():
    logger_settings(log_name)

    for coin in COINS_IDS:

        logger.info(f"Fetching raw market data for: {coin}.")

        fetch_market_data(coin)

        logger.info("Raw data fetching process completed.")







if __name__ == "__main__":
    main()