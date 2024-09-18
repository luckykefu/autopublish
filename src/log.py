# log.py
# --coding:utf-8--
# Time:2024-09-18 19:48:05
# Author:luckykefu
# Email:3124568493@qq.com
# Description: Provides colored logging functionality

import logging
from colorama import Fore, Style, init
from functools import lru_cache

# Initialize colorama
init(autoreset=True)

# Define colors for different levels
LEVEL_COLORS = {
    logging.DEBUG: Fore.BLUE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelno, Style.RESET_ALL)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


@lru_cache(maxsize=None)
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


if __name__ == "__main__":
    logger = get_logger("MyLogger")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    
