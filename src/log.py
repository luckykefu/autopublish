# log.py
# --coding:utf-8--
# Time:2024-09-19 05:25:29
# Author:luckykefu
# Email:3124568493@qq.com
# Description: Provides colored logging functionality with enhanced features

import logging
from colorama import Fore, Style, init
from functools import lru_cache

# Initialize colorama
init(autoreset=True)

# Define colors for different levels
LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelno, Style.RESET_ALL)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


@lru_cache(maxsize=None)
def get_logger(name, log_file=None):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if log_file is provided)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
                )
            )
            logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    
