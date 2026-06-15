import logging
from pathlib import Path
import pandas as pd
from datetime import datetime, UTC

from src.utils.logger import logger_settings
from src.utils.loader import load_json 
from src.utils.saver import save_df_to_parquet

logger = logging.getLogger(__name__)

log_name = Path(__file__).stem


coin = "bitcoin"
execution_date = "20260608_1731"

hist_path = Path(f"data/raw/historic/{coin}/hourly_interval")

filename = f"{coin}_chart_data_{execution_date}.json"



###################### CHART MARKET RAW DATA ##########################



def chart_data_to_df(data: dict) -> pd.DataFrame:

    df_final = None

    for k in data.keys():
        raw_df = pd.DataFrame(data[k], columns=["unix_ts", k])

        if df_final is None: 
            df_final = raw_df
        else:
            df_final = df_final.merge(raw_df, how='left', on='unix_ts')

    return df_final

def validations(df: pd.DataFrame): 
    # Validations

    # Count of nulls in every column of the dataframe
    null_counts = df.isnull().sum()

    for col, count in null_counts.items():
        if count > 0:
            logger.warning(
                f"Column '{col}' contains {count} null values"
            )


    # Searching for duplicated rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        logger.warning(f"Found {duplicates} duplicate rows")
        duplicates = df[df.duplicated(keep=False)]["utc_timestamp"]

        logger.warning(f"{duplicates}")


def clean_chart_data(filename: Path, ):

    data = load_json(filename)

    df = chart_data_to_df(data)

    validations(df)

    # timestamp conversion to UTC
    df['utc_timestamp'] = pd.to_datetime(df["unix_ts"], unit="ms")

    # Save to parquet
    processed_path = Path(f"data/processed/{coin}")
    prqt_name = f"{coin}_clean_chart_data_{execution_date}.parquet"

    save_df_to_parquet(df, processed_path, prqt_name)














if __name__ == "__main__":
    logger_settings(log_name)

    print("au yea")
    