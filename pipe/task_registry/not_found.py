import loguru

logger = loguru.logger


def not_found():
    logger.info("Function not found!")