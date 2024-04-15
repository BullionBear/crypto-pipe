import time
from loguru import logger


def delay(second: float):
    logger.info(f"Sleep {second} seconds")
    time.sleep(second)
    return second

