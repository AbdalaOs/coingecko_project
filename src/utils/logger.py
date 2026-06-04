import logging
from pathlib import Path

def logger_settings(log_filename:str):
    """
    Logging message settings.
    """
    Path("logs").mkdir(exist_ok=True)

    log_path = Path("logs")/f"{log_filename}.log"

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - "
            "%(levelname)s - "
            "%(name)s - "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )