from pathlib import Path
import json
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)

log_name = Path(__file__).stem


def save_json(data: dict|list, filepath: Path = None, filename: str = None):
    # Validate path existance 
    # if it does not exists create it
    Path(filepath).mkdir(exist_ok=True, parents=True)
    # Save raw data from API to json file in desired path
    with (filepath / filename).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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


