import logging

def get_logger(name="app"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s — %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
