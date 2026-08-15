import logging
from pathlib import Path

from src import logger
from src.config import config

def setup_logger():

    log_file = Path(config.LOGGING["log_file"])

    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, config.LOGGING["log_level"]),
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    return logging.getLogger("LLMWorkflow")

logger = setup_logger()