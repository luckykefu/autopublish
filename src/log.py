# log.py
# --coding:utf-8--
# Time:2024-09-17 22:32:08
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define colors for different levels
LEVEL_COLORS = {
    logging.DEBUG: Fore.BLUE,      # Debug messages in blue
    logging.INFO: Fore.GREEN,       # Info messages in green
    logging.WARNING: Fore.YELLOW,    # Warning messages in yellow
    logging.ERROR: Fore.RED,        # Error messages in red
    logging.CRITICAL: Fore.MAGENTA,  # Critical messages in magenta
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Get the color for the record
        color = LEVEL_COLORS.get(record.levelno, Style.RESET_ALL)
        # Set the log format
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Use the custom ColoredFormatter
    formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Clear duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    return logger

if __name__ == "__main__":
    logger = get_logger("MyLogger")

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
