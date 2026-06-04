import logging
import json
from pathlib import Path


logger = logging.getLogger(__name__)

log_name = Path(__file__).stem



def load_json(filename: Path) -> dict:

    if not filename.exists():
        logger.info(f"El archivo {filename} no existe.")
        return {}

    with filename.open("r", encoding="utf-8") as f:
        return json.load(f)

