import logging
from pythonjsonlogger import jsonlogger

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
