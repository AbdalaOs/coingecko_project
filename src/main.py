import logging
from pathlib import Path

from src.utils.logger import logger_settings
from src.ingestion.market_chart import run_market_data
from src.ingestion.OHLC import run_OHLC_data


logger = logging.getLogger(__name__)

log_name = Path(__file__).stem





def main():
    logger_settings(log_name)
    
    # Fetch market chart data 
    # with hourly intervals
    run_market_data()

    # Fetch OHLC data 
    # wiht 4 hours interval data
    run_OHLC_data()






if __name__ == "__main__":
    main()