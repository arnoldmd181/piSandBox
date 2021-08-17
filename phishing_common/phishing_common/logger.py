import logging
import time
import sys
import os

LOGGER_NAME = "phishing-models"


def initialize_logging(log_level="DEBUG", log_file=None, **_):
    # Root logger to WARNING
    logging.getLogger().setLevel(logging.ERROR)
    logger = logging.getLogger(LOGGER_NAME)
    if log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        log_level = logging.getLevelName(log_level)
    else:
        log_level = logging.DEBUG
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s: %(message)s')
    logging.Formatter.converter = time.gmtime

    # log_file
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.mkdir(log_dir)
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False
