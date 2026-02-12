# -*- coding: utf-8 -*-

import logging
import sys

# /// Attempt to create a dedicated logger for Docker....
def get_logger(name: str = "app_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
