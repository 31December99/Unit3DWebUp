# -*- coding: utf-8 -*-

import logging
import sys

COLORS = {
    logging.DEBUG: "\033[36m",     # ->  cyano
    logging.INFO: "\033[32m",      # -> green
    logging.WARNING: "\033[33m",   # -> yellow
    logging.ERROR: "\033[31m",     # -> red
    logging.CRITICAL: "\033[41m",  # -> red background
}

RESET = "\033[0m"

class ColorFormatter(logging.Formatter):

    # Called by the handler
    def format(self, record):
        color = COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{RESET}"


# /// Attempt to create a dedicated logger for Docker....
def get_logger(name: str = "app_logger") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColorFormatter("[%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter) # Custom formatter
        logger.addHandler(handler)
    return logger


