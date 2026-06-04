
import logging
from datetime import datetime, timedelta, UTC
import json

import pandas as pd
from pathlib import Path

from config.config import BASE_URL, ENDPOINTS, HEADERS
from client.connection import get_response
from src.utils.logger import logger_settings

logger = logging.getLogger(__name__)

log_name = Path(__file__).stem


from src.utils.saver import save_json



############## NO BORRAR ##################

# # DATETIME TO UNIX:
# dt = datetime(2025, 5, 31)

# unix_ts = int(dt.timestamp())

# print(unix_ts)

# # STRING TO UNIX:
# date_str = "2025-05-31"

# unix_ts = int(datetime.strptime(date_str,"%Y-%m-%d").timestamp())

# print(unix_ts)

# # UNIX TO DATETIME
# ts = 1748649600

# dt = datetime.fromtimestamp(ts, tz=UTC)

# print(dt)
############################################


print("-----------------PRUEBAS-----------------")


def parse_datetime_to_unix(timestamp: datetime, days: int | None = None) -> dict: 
    
    parsed_dates = {
        "timestamp_str": timestamp.strftime("%Y%m%d_%H%M"), 
        "timestamp_unix": int(timestamp.timestamp())
        }

    if days is not None: 
        previous_date = timestamp-timedelta(days=days)
        # Rest x days from timestamp and convert to string
        parsed_dates["previous_str"] = previous_date.strftime("%Y%m%d_%H%M")
        # Convert x previous days date to unix
        parsed_dates["previous_unix"] = int(previous_date.timestamp())

    return parsed_dates


def load_json(filename: Path) -> dict:

    if not filename.exists():
        logger.info(f"El archivo {filename} no existe.")
        return {}

    with filename.open("r", encoding="utf-8") as f:
        return json.load(f)




def save_checkpoint(coin: str, 
                      data: dict|list,
                      execution_date: str):
    
    # Get last timestamp from extracted data
    ts_unix = max(row[0] for row in data["prices"])
    ts_str = datetime.fromtimestamp(ts_unix/1000, tz=UTC).strftime("%Y%m%d_%H%M")

    checkpoint =  {"coin": coin,
                    "last_execution": execution_date,
                    "last_timestamp_str": ts_str,
                    "last_timestamp_unix": ts_unix
                    }
    
    check_path = Path(f"data/raw/checkpoint/{coin}")
    check_file = "latest_data.json"

    save_json(checkpoint, check_path, check_file)
    logger.info(f"Checkpoint file created in: {check_path}/{check_file}")






def parse_params(check_path: Path, coin: str, dates: dict):

    exec_unix = dates["timestamp_unix"]

    if check_path.exists():

        logger.info(f"Checkpoint file {check_path} exists.")
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




def fetching_data(coin: str):

    check_path = Path(f"data/raw/checkpoint/{coin}/latest_data.json")

    # Parse dates from execution date and 90 days ago to unix format
    dates = parse_datetime_to_unix(datetime.now(UTC), 90)

    EP, params = parse_params(check_path, coin, dates)

    try: 
        #### Fetch INITIAL historic data (market data)
        # with hourly intervals
        data = get_response(BASE_URL, EP, params, HEADERS)

        #### Saving raw data to json file
        # Raw data file path and name
        filepath = Path(f"data/raw/historic/{coin}/hourly_interval")
        # YYYYMMDD_HHMM
        execution_date = dates["timestamp_str"]
        filename = f"{coin}_chart_data_{execution_date}.json"

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

    fetching_data("bitcoin")






if __name__ == "__main__":
    main()
